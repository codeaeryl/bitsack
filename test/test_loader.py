"""
Pengujian untuk src/utils/loader.py
"""
import os
import unittest
import sys

# Tambahkan root project ke path untuk memuat modul src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.loader import load_csv

TEST_CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'test.csv')


class TestLoadCsv(unittest.TestCase):
    """Kumpulan pengujian untuk fungsi load_csv menggunakan data/test.csv."""

    def setUp(self):
        self.data = load_csv(TEST_CSV_PATH)

    # --- Pengujian Struktur ---

    def test_returns_list(self):
        """load_csv harus mengembalikan sebuah list."""
        self.assertIsInstance(self.data, list)

    def test_row_count(self):
        """Harus berisi 11 baris: 1 header + 10 baris data, dengan mengabaikan baris yang tidak valid."""
        self.assertEqual(len(self.data), 11)
        
        # Verifikasi bahwa file mentah benar-benar berisi 16 baris (header + 10 valid + 5 tidak valid)
        with open(TEST_CSV_PATH, 'r') as f:
            raw_lines = f.readlines()
            self.assertEqual(len(raw_lines), 16)

    def test_column_count(self):
        """Setiap baris harus memiliki tepat 3 kolom."""
        for row in self.data:
            self.assertEqual(len(row), 3)

    # --- Pengujian Header ---

    def test_header_values(self):
        """Baris pertama harus berupa header: label, weight, profit."""
        self.assertEqual(self.data[0], ['label', 'weight', 'profit'])

    # --- Pengujian Tipe Data ---

    def test_labels_are_strings(self):
        """Kolom label harus tetap berupa string."""
        for row in self.data:
            self.assertIsInstance(row[0], str)

    def test_weights_are_numeric(self):
        """Kolom weight (baris data) harus berupa int."""
        for row in self.data[1:]:
            self.assertIsInstance(row[1], int)

    def test_profits_are_numeric(self):
        """Kolom profit (baris data) harus berupa int."""
        for row in self.data[1:]:
            self.assertIsInstance(row[2], int)

    # --- Pengecekan Konten ---

    def test_first_data_row(self):
        """Verifikasi bahwa baris data pertama cocok dengan nilai yang diharapkan."""
        self.assertEqual(self.data[1], ['apple', 1, 4])

    def test_last_data_row(self):
        """Verifikasi bahwa baris data terakhir cocok dengan nilai yang diharapkan."""
        self.assertEqual(self.data[10], ['lemon', 1, 3])

    def test_labels_are_unique(self):
        """Semua label (kecuali header) harus unik."""
        labels = [row[0] for row in self.data[1:]]
        self.assertEqual(len(labels), len(set(labels)))

    def test_integer_cast(self):
        """Nilai seperti 5.00 harus diubah ke int, bukan float."""
        # cherry memiliki profit 5.00 → harus menjadi int 5
        cherry_profit = self.data[3][2]
        self.assertIsInstance(cherry_profit, int)
        self.assertEqual(cherry_profit, 5)

    # --- Edge / Kasus Error ---

    def test_nonexistent_file_raises(self):
        """load_csv harus melemparkan FileNotFoundError untuk file yang tidak ada."""
        with self.assertRaises(FileNotFoundError):
            load_csv('nonexistent_file.csv')

    def test_skips_invalid_rows(self):
        """load_csv harus diam-diam melewati baris di mana weight atau profit gagal diubah ke int atau bernilai < 1."""
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("label,weight,profit\nitem1,5,10\nbad_item1,5.5,10\nbad_item2,5,10.1\nbad_item3,abc,10\nbad_item4,5,xyz\nbad_item5,0,10\nbad_item6,5,0\nitem2,3,6\n")
            tmp_path = tmp.name
        
        try:
            data = load_csv(tmp_path)
            # Hanya boleh berisi header + 2 baris yang valid
            self.assertEqual(len(data), 3)
            self.assertEqual(data[1][0], "item1")
            self.assertEqual(data[2][0], "item2")
        finally:
            os.remove(tmp_path)


if __name__ == '__main__':
    unittest.main()
