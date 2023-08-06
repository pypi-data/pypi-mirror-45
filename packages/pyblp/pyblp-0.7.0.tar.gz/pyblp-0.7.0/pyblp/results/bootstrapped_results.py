"""Economy-level structuring of bootstrapped BLP problem results."""

import itertools
import time
from typing import Any, Callable, Dict, Hashable, List, Optional, Sequence, Tuple

import numpy as np

from .problem_results import ProblemResults
from .results import Results
from .. import exceptions, options
from ..markets.results_market import ResultsMarket
from ..utilities.basics import Array, Error, TableFormatter, format_seconds, generate_items, output, output_progress


class BootstrappedResults(Results):
    r"""Bootstrapped results of a solved problem.

    This class has all of the same methods as :class:`ProblemResults` except for :meth:`ProblemResults.bootstrap` and
    :meth:`ProblemResults.compute_optimal_instruments`. The only other difference is that methods return arrays with an
    extra first dimension along which bootstrapped results are stacked (these stacked results can be used to construct,
    for example, confidence intervals for post-estimation outputs). Similarly, arrays of data (except for firm IDs and
    ownership matrices) passed as arguments to methods should have an extra first dimension of size
    :attr:`BootstrappedResults.draws`.

    Attributes
    ----------
    problem_results : `ProblemResults`
        :class:`ProblemResults` that was used to compute these bootstrapped results.
    bootstrapped_sigma : `ndarray`
        Bootstrapped Cholesky decomposition of the covariance matrix for unobserved taste heterogeneity, :math:`\Sigma`.
    bootstrapped_pi : `ndarray`
        Bootstrapped parameters that measures how agent tastes vary with demographics, :math:`\Pi`.
    bootstrapped_rho : `ndarray`
        Bootstrapped parameters that measure within nesting group correlations, :math:`\rho`.
    bootstrapped_beta : `ndarray`
        Bootstrapped demand-side linear parameters, :math:`\beta`.
    bootstrapped_gamma : `ndarray`
        Bootstrapped supply-side linear parameters, :math:`\gamma`.
    bootstrapped_prices : `ndarray`
        Bootstrapped prices, :math:`p`. If a supply side was not estimated, these are unchanged prices. Otherwise, they
        are equilibrium prices implied by each draw.
    bootstrapped_shares : `ndarray`
        Bootstrapped marketshares, :math:`s`, implied by each draw.
    bootstrapped_delta : `ndarray`
        Bootstrapped mean utility, :math:`\delta`, implied by each draw.
    bootstrapped_costs : `ndarray`
        Bootstrapped marginal costs, :math:`c`, implied by each draw.
    computation_time : `float`
        Number of seconds it took to compute the bootstrapped results.
    draws : `int`
        Number of bootstrap draws.
    fp_converged : `ndarray`
        Flags for convergence of the iteration routine used to compute equilibrium prices in each market. Rows are in
        the same order as :attr:`Problem.unique_market_ids` and column indices correspond to draws.
    fp_iterations : `ndarray`
        Number of major iterations completed by the iteration routine used to compute equilibrium prices in each market
        for each draw. Rows are in the same order as :attr:`Problem.unique_market_ids` and column indices correspond to
        draws.
    contraction_evaluations : `ndarray`
        Number of times the contraction used to compute equilibrium prices was evaluated in each market for each draw.
        Rows are in the same order as :attr:`Problem.unique_market_ids` and column indices correspond to draws.

    Examples
    --------
        - :doc:`Tutorial </tutorial>`

    """

    problem_results: ProblemResults
    bootstrapped_sigma: Array
    bootstrapped_pi: Array
    bootstrapped_rho: Array
    bootstrapped_beta: Array
    bootstrapped_gamma: Array
    bootstrapped_prices: Array
    bootstrapped_shares: Array
    bootstrapped_delta: Array
    bootstrapped_costs: Array
    computation_time: float
    draws: int
    fp_converged: Array
    fp_iterations: Array
    contraction_evaluations: Array

    def __init__(
            self, problem_results: ProblemResults, bootstrapped_sigma: Array, bootstrapped_pi: Array,
            bootstrapped_rho: Array, bootstrapped_beta: Array, bootstrapped_gamma: Array, bootstrapped_prices: Array,
            bootstrapped_shares: Array, bootstrapped_delta: Array, bootstrapped_costs: Array, start_time: float,
            end_time: float, draws: int, converged_mappings: List[Dict[Hashable, bool]],
            iteration_mappings: List[Dict[Hashable, int]], evaluation_mappings: List[Dict[Hashable, int]]) -> None:
        """Structure bootstrapped problem results."""
        super().__init__(problem_results.problem, problem_results._parameters)
        self.problem_results = problem_results
        self.bootstrapped_sigma = bootstrapped_sigma
        self.bootstrapped_pi = bootstrapped_pi
        self.bootstrapped_rho = bootstrapped_rho
        self.bootstrapped_beta = bootstrapped_beta
        self.bootstrapped_gamma = bootstrapped_gamma
        self.bootstrapped_prices = bootstrapped_prices
        self.bootstrapped_shares = bootstrapped_shares
        self.bootstrapped_delta = bootstrapped_delta
        self.bootstrapped_costs = bootstrapped_costs
        self.computation_time = end_time - start_time
        self.draws = draws
        self.fp_converged = np.array(
            [[m[t] if m else True for m in converged_mappings] for t in problem_results.problem.unique_market_ids],
            dtype=np.int
        )
        self.fp_iterations = np.array(
            [[m[t] if m else 0 for m in iteration_mappings] for t in problem_results.problem.unique_market_ids],
            dtype=np.int
        )
        self.contraction_evaluations = np.array(
            [[m[t] if m else 0 for m in evaluation_mappings] for t in problem_results.problem.unique_market_ids],
            dtype=np.int
        )

    def __str__(self) -> str:
        """Format bootstrapped problem results as a string."""
        header = [("Computation", "Time"), ("Bootstrap", "Draws")]
        values = [format_seconds(self.computation_time), self.draws]
        if self.fp_iterations.sum() > 0 or self.contraction_evaluations.sum() > 0:
            header.extend([("Total Fixed Point", "Iterations"), ("Total Contraction", "Evaluations")])
            values.extend([self.fp_iterations.sum(), self.contraction_evaluations.sum()])
        widths = [max(len(k1), len(k2)) for k1, k2 in header]
        formatter = TableFormatter(widths)
        return "\n".join([
            "Bootstrapped Problem Results Summary:",
            formatter.line(),
            formatter([k[0] for k in header]),
            formatter([k[1] for k in header], underline=True),
            formatter(values),
            formatter.line()
        ])

    def _coerce_matrices(self, matrices: Any) -> Array:
        """Coerce array-like stacked matrix tensors into a stacked matrix tensor and validate it."""
        matrices = np.atleast_3d(np.asarray(matrices, options.dtype))
        if matrices.shape != (self.draws, self.problem.N, self.problem._max_J):
            raise ValueError(f"matrices must be {self.draws} by {self.problem.N} by {self.problem._max_J}.")
        return matrices

    def _coerce_optional_costs(self, costs: Optional[Any]) -> Array:
        """Coerce optional array-like costs into a column vector tensor and validate it."""
        if costs is not None:
            costs = np.atleast_3d(np.asarray(costs, options.dtype))
            if costs.shape != (self.draws, self.problem.N, 1):
                raise ValueError(f"costs must be None or {self.draws} by {self.problem.N}.")
        return costs

    def _coerce_optional_prices(self, prices: Optional[Any]) -> Array:
        """Coerce optional array-like prices into a column vector tensor and validate it."""
        if prices is not None:
            prices = np.atleast_3d(np.asarray(prices, options.dtype))
            if prices.shape != (self.draws, self.problem.N, 1):
                raise ValueError(f"prices must be None or {self.draws} by {self.problem.N}.")
        return prices

    def _coerce_optional_shares(self, shares: Optional[Any]) -> Array:
        """Coerce optional array-like shares into a column vector tensor and validate it."""
        if shares is not None:
            shares = np.atleast_3d(np.asarray(shares, options.dtype))
            if shares.shape != (self.draws, self.problem.N, 1):
                raise ValueError(f"shares must be None or {self.draws} by {self.problem.N}.")
        return shares

    def _combine_arrays(
            self, compute_market_results: Callable, fixed_args: Sequence = (), market_args: Sequence = ()) -> Array:
        """Compute an array for each market and stack them into a single tensor. An array for a single market is
        computed by passing fixed_args (identical for all markets) and market_args (matrices with as many rows as there
        are products that are restricted to the market) to compute_market_results, a ResultsMarket method that returns
        the output for the market and a set of any errors encountered during computation.
        """
        errors: List[Error] = []

        # keep track of how long it takes to compute the arrays
        start_time = time.time()

        # define a factory for computing bootstrapped arrays in markets
        def market_factory(pair: Tuple[int, Hashable]) -> tuple:
            """Build a market with bootstrapped data along with arguments used to compute arrays."""
            c, s = pair
            data_override_cs = {
                'prices': self.bootstrapped_prices[c, self.problem._product_market_indices[s]],
                'shares': self.bootstrapped_shares[c, self.problem._product_market_indices[s]]
            }
            market_js = ResultsMarket(
                self.problem, s, self._parameters, self.bootstrapped_sigma[c], self.bootstrapped_pi[c],
                self.bootstrapped_rho[c], self.bootstrapped_beta[c], self.bootstrapped_delta[c], data_override_cs
            )
            args_cs: List[Optional[Array]] = []
            for market_arg in market_args:
                if market_arg is None:
                    args_cs.append(market_arg)
                elif len(market_arg.shape) == 2:
                    args_cs.append(market_arg[self.problem._product_market_indices[s]])
                else:
                    assert len(market_arg.shape) == 3
                    args_cs.append(market_arg[c, self.problem._product_market_indices[s][0]])
            return (market_js, *fixed_args, *args_cs)

        # construct a mapping from draws and market IDs to market-specific arrays and compute the full matrix size
        matrix_mapping: Dict[Tuple[int, Hashable], Array] = {}
        pairs = itertools.product(range(self.draws), self.problem.unique_market_ids)
        generator = output_progress(
            generate_items(pairs, market_factory, compute_market_results), self.draws * self.problem.T, start_time
        )
        for (d, t), (array_dt, errors_dt) in generator:
            matrix_mapping[(d, t)] = np.c_[array_dt]
            errors.extend(errors_dt)

        # output a warning about any errors
        if errors:
            output("")
            output(exceptions.MultipleErrors(errors))
            output("")

        # determine the number of rows and columns
        row_count = sum(matrix_mapping[(0, t)].shape[0] for t in self.problem.unique_market_ids)
        column_count = max(matrix_mapping[(0, t)].shape[1] for t in self.problem.unique_market_ids)

        # preserve the original product order or the sorted market order when stacking the arrays
        combined = np.full((self.draws, row_count, column_count), np.nan, options.dtype)
        for (d, t), matrix_dt in matrix_mapping.items():
            if row_count == self.problem.N:
                combined[d, self.problem._product_market_indices[t], :matrix_dt.shape[1]] = matrix_dt
            else:
                combined[d, self.problem.unique_market_ids == t, :matrix_dt.shape[1]] = matrix_dt

        # output how long it took to compute the arrays
        end_time = time.time()
        output(f"Finished after {format_seconds(end_time - start_time)}.")
        output("")
        return combined
