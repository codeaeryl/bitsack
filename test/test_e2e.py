"""
End-to-End (E2E) Testing untuk Mesin Algoritma Knapsack (Core + NumPy)
"""
import unittest
import os
import sys
import pandas as pd

# Menambahkan root folder agar bisa mengimpor src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.dfs import jalankan_dfs_modular as dfs_core

class TestKnapsackE2E(unittest.TestCase):
    """Test suite untuk memverifikasi kebenaran mesin Core (NumPy-Accelerated)"""

    def setUp(self):
        # Menyiapkan data testing dari test.csv menggunakan load_csv (seperti di UI dan CLI)
        current_dir = os.path.dirname(__file__)
        self.csv_path = os.path.join(current_dir, "../data/test.csv")
        from src.utils.loader import load_csv
        raw_data = load_csv(self.csv_path)
        self.data_list = []
        if raw_data and len(raw_data) > 1:
            for row in raw_data[1:]:
                self.data_list.append({
                    "label": str(row[0]),
                    "weight": int(row[1]),
                    "profit": int(row[2])
                })
        self.kapasitas_w = 10

    def test_profit_optimal(self):
        """Memastikan algoritma menemukan profit optimal yang benar"""
        hasil = dfs_core(self.data_list, kapasitas_w=self.kapasitas_w)
        
        # Profit harus lebih dari 0 (ada solusi)
        self.assertGreater(hasil['best_profit'], 0, "Gagal: Tidak ada solusi ditemukan!")

    def test_weight_within_capacity(self):
        """Memastikan total bobot solusi tidak melebihi kapasitas"""
        hasil = dfs_core(self.data_list, kapasitas_w=self.kapasitas_w)
        
        total_weight = sum(item['weight'] for item in hasil['best_combination'])
        self.assertLessEqual(
            total_weight, 
            self.kapasitas_w, 
            f"Gagal: Total bobot {total_weight} melebihi kapasitas {self.kapasitas_w}!"
        )

    def test_best_node_id_exists(self):
        """Memastikan best_node_id tercatat untuk visualisasi pohon"""
        hasil = dfs_core(self.data_list, kapasitas_w=self.kapasitas_w)
        
        self.assertIsNotNone(hasil['best_node_id'], "Gagal: best_node_id tidak tercatat!")

    def test_exploration_log_has_pruned_nodes(self):
        """Memastikan pruning berfungsi (ada node yang dipangkas)"""
        hasil = dfs_core(self.data_list, kapasitas_w=3)
        
        statuses = {log['status'] for log in hasil['exploration_log']}
        has_pruning = 'Pruned' in statuses or any('PRUNED' in s for s in statuses)
        self.assertTrue(has_pruning, "Gagal: Tidak ada node yang dipruning!")

    def test_nodes_visited_reasonable(self):
        """Memastikan jumlah node yang dikunjungi masuk akal (kurang dari brute force 2^n)"""
        hasil = dfs_core(self.data_list, kapasitas_w=self.kapasitas_w)
        n = len(self.data_list)
        brute_force_max = 2 ** (n + 1)
        
        self.assertLess(
            hasil['nodes_visited'], 
            brute_force_max, 
            f"Gagal: Node dikunjungi ({hasil['nodes_visited']}) >= brute force ({brute_force_max})!"
        )

    def test_different_capacities(self):
        """Memastikan algoritma bekerja dengan berbagai kapasitas"""
        for w in [5, 10, 20, 50]:
            hasil = dfs_core(self.data_list, kapasitas_w=w)
            total_weight = sum(item['weight'] for item in hasil['best_combination'])
            self.assertLessEqual(total_weight, w, f"Gagal pada kapasitas W={w}!")

if __name__ == '__main__':
    unittest.main()