import pandas as pd
import os
import time
from src.core.dfs import jalankan_dfs_modular

def run_cli():
    print("\n" + "="*40)
    print("🎒 Knapsack 0/1 - Mode CLI (Terminal)")
    print("="*40)

    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "../../data/test.csv")

    try:
        df_barang = pd.read_csv(csv_path)
        print("\n📦 Data Barang Input (test.csv):")
        print(df_barang.to_string(index=False))
        print("\n" + "-"*40)
        print("⚙️ Meneruskan data ke mesin modular algoritma Calvin...")
        
        data_list = df_barang.to_dict(orient='records')
        
        start_time = time.time()
        hasil = jalankan_dfs_modular(data_list, kapasitas_w=10)
        end_time = time.time()
        
        waktu_eksekusi = (end_time - start_time) * 1000

        print("Status: Berhasil Dieksekusi via Modul Inti!")
        print("-" * 40)
        print(f"📊 Total Profit Optimal : {hasil['best_profit']}")
        print(f"⏱️ Waktu Eksekusi       : {waktu_eksekusi:.4f} ms")
        print(f"👁️ Total Node Dikunjungi: {hasil['nodes_visited']} Node")
        print(f"🎒 Barang Terpilih      : {[b['label'] for b in hasil['best_combination']]}")
        print("="*40 + "\n")

    except FileNotFoundError:
        print(f"❌ Error: File CSV tidak ditemukan di rute: {csv_path}")

if __name__ == "__main__":
    run_cli()