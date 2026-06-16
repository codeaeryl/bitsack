import pandas as pd
import os
import sys
import time
import glob

# src/utils/cli.py
# Modul ini adalah antarmuka Command Line Interface (CLI) interaktif.
# Berfungsi sebagai lingkungan pengujian (Sandbox) ringan via Terminal 
# sebelum algoritma divisualisasikan secara berat di Web UI (app.py).

# Tambahkan root directory ke sys.path agar bisa import module 'src' dari mana saja
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
# Solusi: Menaikkan batas rekursi hingga 150.000 untuk mengakomodasi algoritma Core pada data skala 100.000
sys.setrecursionlimit(150000)

def run_cli():
    print("\n" + "="*60)
    print("🎒 Knapsack 0/1 - CLI Sandbox Mode (Fitur Pengujian)")
    print("="*60)

    # 1. Pilihan Sumber Data Dinamis dari Folder 'data'
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "../../data")
    
    # Mencari semua file dengan ekstensi .csv di folder data
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    
    if not csv_files:
        print("❌ Error: Tidak ada file CSV yang ditemukan di folder data!")
        return

    print("\n📂 Pilih File Data CSV yang ingin diuji:")
    for idx, file_path in enumerate(csv_files):
        file_name = os.path.basename(file_path)
        print(f"[{idx + 1}] {file_name}")
        
    try:
        pilihan_file = int(input("\nMasukkan nomor file pilihanmu: ")) - 1
        if pilihan_file < 0 or pilihan_file >= len(csv_files):
            print("❌ Pilihan tidak valid!")
            return
        csv_path = csv_files[pilihan_file]
    except ValueError:
        print("❌ Harap masukkan angka yang valid!")
        return

    try:
        df_barang = pd.read_csv(csv_path)
        
        # Convert weight and profit columns to integer to satisfy integer requirement
        if 'weight' in df_barang.columns:
            df_barang['weight'] = pd.to_numeric(df_barang['weight'], errors='coerce').fillna(0).astype(int)
        if 'profit' in df_barang.columns:
            df_barang['profit'] = pd.to_numeric(df_barang['profit'], errors='coerce').fillna(0).astype(int)
        
        # 2. Validasi Syarat Jumlah Barang (Minimal 8)
        jumlah_barang = len(df_barang)
        if jumlah_barang < 8:
            print("\n" + "!"*60)
            print(f"❌ ERROR VALIDASI: File '{os.path.basename(csv_path)}' hanya berisi {jumlah_barang} barang.")
            print("Syarat tugas mengharuskan input n minimal 8 barang. Proses dihentikan.")
            print("!"*60 + "\n")
            return
            
        print(f"\n📦 Data Barang Input ({os.path.basename(csv_path)}):")
        print(df_barang.to_string(index=False))
        print("\n" + "-"*60)
        
        # 3. Integrasi Pemilihan Modul (Core vs Optimize)
        print("⚙️ Pilih Mesin Algoritma yang ingin diuji:")
        print("[1] Modul Core     (Calvin - Standar DFS & Pruning)")
        print("[2] Modul Optimize (Jayden - Iterative & Heuristik)")
        
        try:
            pilihan_mesin = int(input("\nMasukkan nomor mesin pilihanmu: "))
            if pilihan_mesin == 1:
                from src.core.dfs import jalankan_dfs_modular
                nama_mesin = "Core (Calvin)"
            elif pilihan_mesin == 2:
                from src.optimize.dfs import jalankan_dfs_modular
                nama_mesin = "Optimize (Jayden)"
            else:
                print("❌ Pilihan tidak valid!")
                return
        except ValueError:
            print("❌ Harap masukkan angka yang valid!")
            return
        except ImportError as e:
            print(f"❌ Gagal memuat mesin (Pastikan struktur folder benar): {e}")
            return

        # 4. Input Kapasitas Dinamis (W)
        print("\n" + "-"*60)
        try:
            input_w = input("Masukkan kapasitas tas (W) [Tekan Enter untuk default 10]: ")
            kapasitas_w = int(input_w) if input_w.strip() else 10
        except ValueError:
            kapasitas_w = 10
            print("Format salah, menggunakan kapasitas default = 10")

        print(f"\n🚀 Meneruskan data ke mesin {nama_mesin} dengan Kapasitas = {kapasitas_w}...")
        
        # Konversi dataframe ke list of dicts
        data_list = df_barang.to_dict(orient='records')
        
        # Eksekusi dan pengukuran waktu
        start_time = time.time()
        hasil = jalankan_dfs_modular(data_list, kapasitas_w=kapasitas_w)
        end_time = time.time()
        
        waktu_eksekusi = (end_time - start_time) * 1000

        # Menampilkan Langkah Eksplorasi (Fitur Wajib)
        print("\n🔍 Langkah/Urutan Eksplorasi Node (10 Terakhir):")
        print(f"{'Node':<8} | {'Item Evaluasi':<15} | {'Profit':<10} | {'Berat':<10} | {'Status'}")
        print("-" * 80)
        for log in hasil.get('exploration_log', [])[-10:]:
            node_str = str(log.get('node', '?'))
            item_str = str(log.get('current_item', '-'))
            profit_str = str(log.get('profit', '?'))
            weight_str = str(log.get('weight', '?'))
            status_str = str(log.get('status', '?'))
            print(f"{node_str:<8} | {item_str:<15} | {profit_str:<10} | {weight_str:<10} | {status_str}")

        # Menampilkan Output
        print("\n" + "="*60)
        print(f"✅ Status: Berhasil Dieksekusi via Mesin {nama_mesin}!")
        print("="*60)
        print(f"📊 Total Profit Optimal : {hasil['best_profit']}")
        print(f"⏱️ Waktu Eksekusi       : {waktu_eksekusi:.4f} ms")
        print(f"👁️ Total Node Dikunjungi: {hasil['nodes_visited']} Node")
        
        # 1. Tambahkan Total Bobot
        total_weight = sum(b['weight'] for b in hasil['best_combination'])
        print(f"⚖️ Total Bobot (Weight) : {int(total_weight)} / {kapasitas_w}")
        
        # 2. Merapikan List Barang Terpilih
        chosen_items = [b['label'] for b in hasil['best_combination']]
        if len(chosen_items) > 20:
            print(f"🎒 Barang Terpilih      : {chosen_items[:15]} ... (+ {len(chosen_items) - 15} more)")
        else:
            print(f"🎒 Barang Terpilih      : {chosen_items}")
            
        print("="*60 + "\n")

    except FileNotFoundError:
        print(f"❌ Error: File CSV tidak ditemukan di rute: {csv_path}")
    except Exception as e:
        print(f"❌ Terjadi kesalahan sistem: {e}")

if __name__ == "__main__":
    run_cli()