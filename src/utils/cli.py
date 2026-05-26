import pandas as pd
import os

def run_cli():
    print("\n" + "="*40)
    print("🎒 Knapsack 0/1 - Mode CLI (Terminal)")
    print("="*40)

    # Mengambil path relatif ke data/test.csv
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "../../data/test.csv")

    try:
        # Membaca data CSV
        df_barang = pd.read_csv(csv_path)
        
        print("\n📦 Data Barang Input (test.csv):")
        # Mencetak dataframe ke terminal tanpa nomor indeks agar rapi
        print(df_barang.to_string(index=False))
        
        print("\n" + "-"*40)
        print("⚙️ Meneruskan data ke mesin algoritma Jayden...")
        
        # Mengubah dataframe menjadi list of dictionary (Format yang diminta Jayden)
        data_list = df_barang.to_dict(orient='records')
        
        # Nanti Jayden tinggal memanggil fungsinya di sini
        # contoh: hasil = jalankan_dfs(data_list, kapasitas=10)
        
        print("Status: Menunggu logika Backtracking & Multithreading diimplementasikan.")
        print("="*40 + "\n")

    except FileNotFoundError:
        print(f"❌ Error: File CSV tidak ditemukan di rute: {csv_path}")

if __name__ == "__main__":
    run_cli()