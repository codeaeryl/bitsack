"""
Upper bound calculation using numpy-accelerated prefix sums and suffix minimums.
Runtime queries still use bisect on Python lists for fast scalar access.
"""
import bisect
import numpy as np


class BoundCalculator:
    """
    Preprocessing: O(n) using numpy vectorized cumsum and cummin.
    Per-query: O(log n) using bisect on Python lists.
    """

    __slots__ = ('_n', '_kapasitas_w', '_prefix_weight', '_prefix_profit',
                 '_suffix_min_weight', '_ratios')

    def __init__(self, weights, profits, ratios, kapasitas_w):
        n = len(weights)
        self._n = n
        self._kapasitas_w = kapasitas_w
        self._ratios = ratios

        # Prefix sums via numpy cumsum
        w_np = np.array(weights)
        p_np = np.array(profits)

        pw = np.empty(n + 1)
        pw[0] = 0.0
        np.cumsum(w_np, out=pw[1:])

        pp = np.empty(n + 1)
        pp[0] = 0.0
        np.cumsum(p_np, out=pp[1:])

        # Convert to Python lists for fast bisect lookups
        self._prefix_weight = pw.tolist()
        self._prefix_profit = pp.tolist()

        # Suffix minimum weights via numpy reverse accumulate
        smw = [float('inf')] * (n + 1)
        if n > 0:
            reversed_cummin = np.minimum.accumulate(w_np[::-1])[::-1]
            smw[:n] = reversed_cummin.tolist()
        self._suffix_min_weight = smw

    def calculate(self, index, current_weight, current_profit):
        """
        Calculate the fractional upper bound starting from `index`.
        Uses bisect on Python list for O(log n) binary search.
        """
        if current_weight >= self._kapasitas_w:
            return 0.0

        remaining = self._kapasitas_w - current_weight
        target = self._prefix_weight[index] + remaining

        j = bisect.bisect_right(self._prefix_weight, target, index, self._n + 1) - 1

        bound = current_profit + (self._prefix_profit[j] - self._prefix_profit[index])

        if j < self._n:
            weight_taken = self._prefix_weight[j] - self._prefix_weight[index]
            leftover = remaining - weight_taken
            bound += leftover * self._ratios[j]

        return bound
