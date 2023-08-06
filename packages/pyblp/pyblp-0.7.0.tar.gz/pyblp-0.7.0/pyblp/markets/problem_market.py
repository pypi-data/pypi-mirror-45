"""Market-level BLP problem functionality."""

import functools
from typing import List, Tuple

import numpy as np

from .market import Market
from .. import exceptions, options
from ..configurations.iteration import ContractionResults, Iteration
from ..utilities.basics import Array, Bounds, Error


class ProblemMarket(Market):
    """A market underlying the BLP problem."""

    def solve_demand(
            self, initial_delta: Array, iteration: Iteration, fp_type: str, compute_jacobian: bool) -> (
            Tuple[Array, Array, List[Error], bool, int, int]):
        """Compute the mean utility for this market that equates market shares to observed values by solving a fixed
        point problem. Then, if compute_jacobian is True, compute the Jacobian of xi (equivalently, of delta) with
        respect to theta. If necessary, replace null elements in delta with their last values before computing its
        Jacobian.
        """
        errors: List[Error] = []

        # configure NumPy to identify floating point errors
        with np.errstate(divide='call', over='call', under='ignore', invalid='call'):
            np.seterrcall(lambda *_: errors.append(exceptions.DeltaFloatingPointError()))

            # compute delta either with a closed-form solution or by solving a fixed point problem
            if self.K2 == 0:
                converged = True
                iterations = evaluations = 0
                log_shares = np.log(self.products.shares)
                log_outside_share = np.log(1 - self.products.shares.sum())
                delta = log_shares - log_outside_share
                if self.H > 0:
                    log_group_shares = np.log(self.groups.expand(self.groups.sum(self.products.shares)))
                    delta -= self.rho * (log_shares - log_group_shares)
            elif 'linear' in fp_type:
                # set up components common to both types of linear contraction
                log_shares = np.log(self.products.shares)
                compute_probabilities = functools.partial(self.compute_probabilities, safe='safe' in fp_type)

                # define the linear contraction
                if self.H == 0:
                    def contraction(x: Array) -> ContractionResults:
                        """Compute the next linear delta and optionally its Jacobian."""
                        probabilities = compute_probabilities(x)[0]
                        shares = probabilities @ self.agents.weights
                        x = x + log_shares - np.log(shares)
                        if not iteration._compute_jacobian:
                            return x, None, None
                        weighted_probabilities = self.agents.weights * probabilities.T
                        jacobian = (probabilities @ weighted_probabilities) / shares
                        return x, None, jacobian
                else:
                    # pre-compute additional components for the nested contraction
                    dampener = 1 - self.rho
                    rho_membership = self.rho * self.get_membership_matrix()

                    # define the nested contraction
                    def contraction(x: Array) -> ContractionResults:
                        """Compute the next linear delta and optionally its Jacobian under nesting."""
                        probabilities, conditionals = compute_probabilities(x)
                        shares = probabilities @ self.agents.weights
                        x = x + (log_shares - np.log(shares)) * dampener
                        if not iteration._compute_jacobian:
                            return x, None, None
                        weighted_probabilities = self.agents.weights * probabilities.T
                        probabilities_part = dampener * (probabilities @ weighted_probabilities)
                        conditionals_part = rho_membership * (conditionals @ weighted_probabilities)
                        jacobian = (probabilities_part + conditionals_part) / shares
                        return x, None, jacobian

                # solve the linear fixed point problem
                delta, converged, iterations, evaluations = iteration._iterate(initial_delta, contraction)
            else:
                assert 'nonlinear' in fp_type

                # set up components common to both types of linear contraction
                if 'safe' in fp_type:
                    utility_reduction = np.max(self.mu, axis=0, keepdims=True)
                    exp_mu = np.exp(self.mu - utility_reduction)
                    compute_probabilities = functools.partial(
                        self.compute_probabilities, mu=exp_mu, utility_reduction=utility_reduction, linear=False
                    )
                else:
                    exp_mu = np.exp(self.mu)
                    compute_probabilities = functools.partial(self.compute_probabilities, mu=exp_mu, linear=False)

                # define the nonlinear contraction
                if self.H == 0:
                    def contraction(x: Array) -> ContractionResults:
                        """Compute the next exponentiated delta and optionally its Jacobian."""
                        probability_ratios = compute_probabilities(x, numerator=exp_mu)[0]
                        share_ratios = probability_ratios @ self.agents.weights
                        x0, x = x, self.products.shares / share_ratios
                        if not iteration._compute_jacobian:
                            return x, None, None
                        shares = x0 * share_ratios
                        probabilities = x0 * probability_ratios
                        weighted_probabilities = self.agents.weights * probabilities.T
                        jacobian = x / x0.T * (probabilities @ weighted_probabilities) / shares
                        return x, None, jacobian
                else:
                    # pre-compute additional components for the nested contraction
                    dampener = 1 - self.rho
                    rho_membership = self.rho * self.get_membership_matrix()

                    # define the nested contraction
                    def contraction(x: Array) -> ContractionResults:
                        """Compute the next exponentiated delta and optionally its Jacobian under nesting."""
                        probabilities, conditionals = compute_probabilities(x)
                        shares = probabilities @ self.agents.weights
                        x0, x = x, x * (self.products.shares / shares)**dampener
                        if not iteration._compute_jacobian:
                            return x, None, None
                        weighted_probabilities = self.agents.weights * probabilities.T
                        probabilities_part = dampener * (probabilities @ weighted_probabilities)
                        conditionals_part = rho_membership * (conditionals @ weighted_probabilities)
                        jacobian = x / x0.T * (probabilities_part + conditionals_part) / shares
                        return x, None, jacobian

                # solve the nonlinear fixed point problem
                exp_delta, converged, iterations, evaluations = iteration._iterate(np.exp(initial_delta), contraction)
                delta = np.log(exp_delta)

        # check for convergence
        if not converged:
            errors.append(exceptions.DeltaConvergenceError())

        # if the gradient is to be computed, replace invalid values in delta with the last computed values before
        #   computing its Jacobian
        xi_jacobian = np.full((self.J, self.parameters.P), np.nan, options.dtype)
        if compute_jacobian:
            valid_delta = delta.copy()
            bad_delta_index = ~np.isfinite(delta)
            valid_delta[bad_delta_index] = initial_delta[bad_delta_index]
            xi_jacobian, jacobian_errors = self.compute_xi_by_theta_jacobian(valid_delta)
            errors.extend(jacobian_errors)
        return delta, xi_jacobian, errors, converged, iterations, evaluations

    def solve_supply(
            self, initial_tilde_costs: Array, xi_jacobian: Array, costs_type: str, costs_bounds: Bounds,
            compute_jacobian: bool) -> Tuple[Array, Array, Array, List[Error]]:
        """Compute transformed marginal costs for this market. Then, if compute_jacobian is True, compute the Jacobian
        of omega (equivalently, of transformed marginal costs) with respect to theta. If necessary, replace null
        elements in transformed marginal costs with their last values before computing their Jacobian.
        """
        errors: List[Error] = []

        # configure NumPy to identify floating point errors
        with np.errstate(divide='call', over='call', under='ignore', invalid='call'):
            np.seterrcall(lambda *_: errors.append(exceptions.CostsFloatingPointError()))

            # compute marginal costs
            eta, eta_errors = self.compute_eta()
            errors.extend(eta_errors)
            costs = self.products.prices - eta

            # clip marginal costs that are outside of acceptable bounds
            clipped_costs = (costs < costs_bounds[0]) | (costs > costs_bounds[1])
            if clipped_costs.any():
                costs = np.clip(costs, *costs_bounds)

            # take the log of marginal costs under a log-linear specification
            if costs_type == 'linear':
                tilde_costs = costs
            else:
                assert costs_type == 'log'
                if np.any(costs <= 0):
                    errors.append(exceptions.NonpositiveCostsError())
                with np.errstate(all='ignore'):
                    tilde_costs = np.log(costs)

        # if the gradient is to be computed, replace invalid transformed marginal costs with their last computed
        #   values before computing their Jacobian, which is zero for clipped marginal costs
        omega_jacobian = np.full((self.J, self.parameters.P), np.nan, options.dtype)
        if compute_jacobian:
            valid_tilde_costs = tilde_costs.copy()
            bad_tilde_costs_index = ~np.isfinite(tilde_costs)
            valid_tilde_costs[bad_tilde_costs_index] = initial_tilde_costs[bad_tilde_costs_index]
            omega_jacobian, jacobian_errors = self.compute_omega_by_theta_jacobian(
                valid_tilde_costs, xi_jacobian, costs_type
            )
            errors.extend(jacobian_errors)
            omega_jacobian[clipped_costs.flat] = 0
        return tilde_costs, omega_jacobian, clipped_costs, errors
