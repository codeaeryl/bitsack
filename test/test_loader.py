"""
Tests for src/utils/loader.py
"""
import os
import unittest
import sys
import numpy as np

# Add project root to path to import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.loader import load_csv

TEST_CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'test.csv')


class TestLoadCsv(unittest.TestCase):
    """Test suite for the load_csv function using data/test.csv."""

    def setUp(self):
        self.labels, self.weights, self.profits = load_csv(TEST_CSV_PATH)

    # --- Structure tests ---

    def test_returns_numpy_arrays(self):
        """load_csv should return a tuple of 3 numpy arrays."""
        self.assertIsInstance(self.labels, np.ndarray)
        self.assertIsInstance(self.weights, np.ndarray)
        self.assertIsInstance(self.profits, np.ndarray)

    def test_row_count(self):
        """Should contain 10 elements per array (header is excluded)."""
        self.assertEqual(len(self.labels), 10)
        self.assertEqual(len(self.weights), 10)
        self.assertEqual(len(self.profits), 10)

    # --- Data type tests ---

    def test_labels_are_strings(self):
        """Label column should contain string type values."""
        for val in self.labels:
            self.assertIsInstance(val, (str, np.str_))

    def test_weights_are_floats(self):
        """Weight column should be float64 values."""
        self.assertTrue(np.issubdtype(self.weights.dtype, np.floating))

    def test_profits_are_floats(self):
        """Profit column should be float64 values."""
        self.assertTrue(np.issubdtype(self.profits.dtype, np.floating))

    # --- Content spot-checks ---

    def test_first_data_row(self):
        """Verify the first data row matches expected values."""
        self.assertEqual(self.labels[0], 'apple')
        self.assertAlmostEqual(self.weights[0], 1.2)
        self.assertAlmostEqual(self.profits[0], 3.5)

    def test_last_data_row(self):
        """Verify the last data row matches expected values."""
        self.assertEqual(self.labels[9], 'lemon')
        self.assertAlmostEqual(self.weights[9], 0.7)
        self.assertAlmostEqual(self.profits[9], 2.9)

    def test_labels_are_unique(self):
        """All labels should be unique."""
        self.assertEqual(len(self.labels), len(set(self.labels)))

    def test_float_cast(self):
        """Integer values in the CSV (like 5) should be cast/locked to floats."""
        # cherry is at index 2, profit is listed as '5' in test.csv
        cherry_profit = self.profits[2]
        self.assertIsInstance(cherry_profit, (float, np.float64))
        self.assertAlmostEqual(cherry_profit, 5.0)

    # --- Edge / error case ---

    def test_nonexistent_file_raises(self):
        """load_csv should raise FileNotFoundError or OSError for a missing file."""
        with self.assertRaises((FileNotFoundError, OSError)):
            load_csv('nonexistent_file.csv')


if __name__ == '__main__':
    unittest.main()
