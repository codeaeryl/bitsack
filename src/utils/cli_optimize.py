import pandas as pd
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.setrecursionlimit(15000)
from optimize.dfs import jalankan_dfs_modular as dfs_optimized
from core.dfs import jalankan_dfs_modular as dfs_core

def run_cli_optimized():
    print("\n" + "="*40)
    print("🎒 Knapsack 0/1 - Mode CLI (Optimised)")
    print("="*40)

    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "../../data/data.csv")
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        csv_path = os.path.join(current_dir, "../../data/test.csv")

    try:
        df_barang = pd.read_csv(csv_path)
        print(f"\n📦 Data Barang Input ({os.path.basename(csv_path)}):")
        print(df_barang.to_string(index=False))
        print("\n" + "-"*40)
        print("⚙️ Meneruskan data ke mesin modular algoritma...")
        
        # Test Optimised DFS
        print("\n--- DFS Optimised ---")
        import tracemalloc
        tracemalloc.start()
        start_time = time.time()
        hasil_dfs = dfs_optimized(df_barang, kapasitas_w=10)
        end_time = time.time()
        _, peak_mem_dfs = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        waktu_eksekusi_dfs = (end_time - start_time) * 1000

        print(f"📊 Total Profit Optimal : {hasil_dfs['best_profit']}")
        print(f"⏱️ Waktu Eksekusi       : {waktu_eksekusi_dfs:.4f} ms")
        print(f"👁️ Total Node Dikunjungi: {hasil_dfs['nodes_visited']} Node")
        print(f"💾 Peak Memory Usage    : {peak_mem_dfs / 1024:.2f} KB")
        print(f"🎒 Barang Terpilih      : {[b['label'] for b in hasil_dfs['best_combination']]}")
        
        # Test Core DFS (Original)
        print("\n--- DFS Core (Original) ---")
        tracemalloc.start()
        start_time = time.time()
        data_list_core = df_barang.to_dict(orient='records')
        hasil_core = dfs_core(data_list_core, kapasitas_w=10)
        end_time = time.time()
        _, peak_mem_core = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        waktu_eksekusi_core = (end_time - start_time) * 1000

        print(f"📊 Total Profit Optimal : {hasil_core['best_profit']}")
        print(f"⏱️ Waktu Eksekusi       : {waktu_eksekusi_core:.4f} ms")
        print(f"👁️ Total Node Dikunjungi: {hasil_core['nodes_visited']} Node")
        print(f"💾 Peak Memory Usage    : {peak_mem_core / 1024:.2f} KB")
        print(f"🎒 Barang Terpilih      : {[b['label'] for b in hasil_core['best_combination']]}")
        print("="*40 + "\n")

    except FileNotFoundError:
        print(f"❌ Error: File CSV tidak ditemukan di rute: {csv_path}")

if __name__ == "__main__":
    run_cli_optimized()
