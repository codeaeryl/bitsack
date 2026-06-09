import pandas as pd
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.setrecursionlimit(15000)
from optimize.dfs import jalankan_dfs_modular as dfs_optimized
from mp_optimize.dfs import jalankan_dfs_modular as dfs_parallel

def run_cli_optimized():
    KAPASITAS_W = 67.69
    print("\n" + "="*40)
    print("🎒 Knapsack 0/1 - Mode CLI (Optimised)")
    print("="*40)

    current_dir = os.path.dirname(__file__)
    # Use test.csv by default to avoid hangs on large datasets unless --full is requested
    if "--full" in sys.argv:
        csv_path = os.path.join(current_dir, "../../data/data.csv")
    else:
        csv_path = os.path.join(current_dir, "../../data/test.csv")
        print("💡 Running with test.csv. Pass '--full' to run with data.csv.")

    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        csv_path = os.path.join(current_dir, "../../data/test.csv")

    try:
        df_barang = pd.read_csv(csv_path)
        print(f"\n📦 Data Barang Input ({os.path.basename(csv_path)}):")
        if len(df_barang) > 20:
            print(df_barang.head(10).to_string(index=False))
            print(f"... and {len(df_barang) - 10} more rows ...")
        else:
            print(df_barang.to_string(index=False))
        print("\n" + "-"*40)
        print("⚙️ Meneruskan data ke mesin modular algoritma...")
        
        # Test Parallel DFS
        print("\n--- DFS Parallel (Multiprocessed) ---")
        import tracemalloc
        tracemalloc.start()
        start_time = time.time()
        hasil_parallel = dfs_parallel(df_barang, kapasitas_w=KAPASITAS_W)
        end_time = time.time()
        _, peak_mem_parallel = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        waktu_eksekusi_parallel = (end_time - start_time) * 1000

        print(f"📊 Total Profit Optimal : {hasil_parallel['best_profit']}")
        print(f"⏱️ Waktu Eksekusi       : {waktu_eksekusi_parallel:.4f} ms")
        print(f"👁️ Total Node Dikunjungi: {hasil_parallel['nodes_visited']} Node")
        
        total_weight_parallel = sum(b['weight'] for b in hasil_parallel['best_combination'])
        print(f"⚖️ Total Bobot (Weight) : {total_weight_parallel:.2f} / {KAPASITAS_W}")
        print(f"💾 Peak Memory Usage    : {peak_mem_parallel / 1024:.2f} KB")
        
        chosen_parallel = [b['label'] for b in hasil_parallel['best_combination']]
        if len(chosen_parallel) > 20:
            print(f"🎒 Barang Terpilih      : {chosen_parallel[:15]} ... (+ {len(chosen_parallel) - 15} more)")
        else:
            print(f"🎒 Barang Terpilih      : {chosen_parallel}")

        # Test Optimised DFS
        print("\n--- DFS Optimised ---")
        tracemalloc.start()
        start_time = time.time()
        hasil_dfs = dfs_optimized(df_barang, kapasitas_w=KAPASITAS_W)
        end_time = time.time()
        _, peak_mem_dfs = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        waktu_eksekusi_dfs = (end_time - start_time) * 1000

        print(f"📊 Total Profit Optimal : {hasil_dfs['best_profit']}")
        print(f"⏱️ Waktu Eksekusi       : {waktu_eksekusi_dfs:.4f} ms")
        print(f"👁️ Total Node Dikunjungi: {hasil_dfs['nodes_visited']} Node")
        
        total_weight_dfs = sum(b['weight'] for b in hasil_dfs['best_combination'])
        print(f"⚖️ Total Bobot (Weight) : {total_weight_dfs:.2f} / {KAPASITAS_W}")
        print(f"💾 Peak Memory Usage    : {peak_mem_dfs / 1024:.2f} KB")
        
        chosen_dfs = [b['label'] for b in hasil_dfs['best_combination']]
        if len(chosen_dfs) > 20:
            print(f"🎒 Barang Terpilih      : {chosen_dfs[:15]} ... (+ {len(chosen_dfs) - 15} more)")
        else:
            print(f"🎒 Barang Terpilih      : {chosen_dfs}")
        
        print("="*40 + "\n")

    except FileNotFoundError:
        print(f"❌ Error: File CSV tidak ditemukan di rute: {csv_path}")

if __name__ == "__main__":
    run_cli_optimized()
