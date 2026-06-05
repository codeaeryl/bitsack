"""
End-to-End (E2E) Testing untuk konsistensi Mesin Algoritma Knapsack
"""
import unittest
import os
import sys
import pandas as pd

# Menambahkan root folder agar bisa mengimpor src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.dfs import jalankan_dfs_modular as dfs_core
from src.optimize.dfs import jalankan_dfs_modular as dfs_optimize

class TestKnapsackE2E(unittest.TestCase):
    """Test suite untuk membandingkan mesin Core vs Optimize"""

    def setUp(self):
        # Menyiapkan data testing dari test.csv menggunakan pandas (seperti di UI dan CLI)
        current_dir = os.path.dirname(__file__)
        self.csv_path = os.path.join(current_dir, "../data/test.csv")
        df = pd.read_csv(self.csv_path)
        self.data_list = df.to_dict(orient='records')
        self.kapasitas_w = 10

    def test_core_vs_optimize_consistency(self):
        """Memastikan kedua mesin menghasilkan profit optimal yang sama persis"""
        
        # Eksekusi kedua mesin secara E2E
        hasil_core = dfs_core(self.data_list, kapasitas_w=self.kapasitas_w)
        hasil_opt = dfs_optimize(self.data_list, kapasitas_w=self.kapasitas_w)

        # 1. TEST LOGIKA: Profit harus sama persis
        self.assertEqual(
            hasil_core['best_profit'], 
            hasil_opt['best_profit'], 
            "Gagal: Profit Optimize tidak sama dengan Core!"
        )

        # 2. TEST EFISIENSI: Node yang dikunjungi mesin Optimize harus lebih sedikit / sama
        self.assertLessEqual(
            hasil_opt['nodes_visited'], 
            hasil_core['nodes_visited'],
            "Peringatan: Mesin Optimize mengunjungi lebih banyak node dari Core!"
        )

if __name__ == '__main__':
    unittest.main()