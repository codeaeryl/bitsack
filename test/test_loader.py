"""
Tests for src/utils/loader.py
"""
import os
import unittest
import sys

# Add project root to path to import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.loader import load_csv

TEST_CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'test.csv')


class TestLoadCsv(unittest.TestCase):
    """Test suite for the load_csv function using data/test.csv."""

    def setUp(self):
        self.data = load_csv(TEST_CSV_PATH)

    # --- Structure tests ---

    def test_returns_list(self):
        """load_csv should return a list."""
        self.assertIsInstance(self.data, list)

    def test_row_count(self):
        """Should contain 11 rows: 1 header + 10 data rows."""
        self.assertEqual(len(self.data), 11)

    def test_column_count(self):
        """Every row should have exactly 3 columns."""
        for row in self.data:
            self.assertEqual(len(row), 3)

    # --- Header tests ---

    def test_header_values(self):
        """First row should be the header: label, weight, profit."""
        self.assertEqual(self.data[0], ['label', 'weight', 'profit'])

    # --- Data type tests ---

    def test_labels_are_strings(self):
        """Label column should remain as strings."""
        for row in self.data:
            self.assertIsInstance(row[0], str)

    def test_weights_are_numeric(self):
        """Weight column (data rows) should be int or float."""
        for row in self.data[1:]:
            self.assertIsInstance(row[1], (int, float))

    def test_profits_are_numeric(self):
        """Profit column (data rows) should be int or float."""
        for row in self.data[1:]:
            self.assertIsInstance(row[2], (int, float))

    # --- Content spot-checks ---

    def test_first_data_row(self):
        """Verify the first data row matches expected values."""
        self.assertEqual(self.data[1], ['apple', 1.2, 3.5])

    def test_last_data_row(self):
        """Verify the last data row matches expected values."""
        self.assertEqual(self.data[10], ['lemon', 0.7, 2.9])

    def test_labels_are_unique(self):
        """All labels (excluding header) should be unique."""
        labels = [row[0] for row in self.data[1:]]
        self.assertEqual(len(labels), len(set(labels)))

    def test_integer_cast(self):
        """Values like 5.00 should be cast to int, not float."""
        # cherry has profit 5.00 → should become int 5
        cherry_profit = self.data[3][2]
        self.assertIsInstance(cherry_profit, int)
        self.assertEqual(cherry_profit, 5)

    # --- Edge / error case ---

    def test_nonexistent_file_raises(self):
        """load_csv should raise FileNotFoundError for a missing file."""
        with self.assertRaises(FileNotFoundError):
            load_csv('nonexistent_file.csv')


if __name__ == '__main__':
    unittest.main()
