import pandas as pd
import os
import time


def jalankan_dfs(daftar_barang, kapasitas_w):
    items = [dict(item) for item in daftar_barang]
    for item in items:
        item['ratio'] = item['profit'] / item['weight']
    
    items.sort(key=lambda x: x['ratio'], reverse=True)
    n = len(items)
    
    best_profit = 0.0
    best_combination = []
    nodes_visited = 0
    exploration_log = []

    def calculate_upper_bound(index, current_weight, current_profit):
        if current_weight >= kapasitas_w:
            return 0
        bound = current_profit
        total_weight = current_weight
        j = index
        while j < n and total_weight + items[j]['weight'] <= kapasitas_w:
            total_weight += items[j]['weight']
            bound += items[j]['profit']
            j += 1
        if j < n:
            bound += (kapasitas_w - total_weight) * items[j]['ratio']
        return bound

    def dfs(index, current_weight, current_profit, current_items):
        nonlocal best_profit, best_combination, nodes_visited
        nodes_visited += 1
        
        chosen_names = [item['label'] for item in current_items]
        exploration_log.append({
            "node": nodes_visited, "weight": round(current_weight, 2),
            "profit": round(current_profit, 2), "chosen": chosen_names, "status": "Eksplorasi"
        })
        
        if current_weight <= kapasitas_w and current_profit > best_profit:
            best_profit = current_profit
            best_combination = list(current_items)
            
        if index == n:
            return

        bound = calculate_upper_bound(index, current_weight, current_profit)
        if bound <= best_profit:
            exploration_log[-1]["status"] = f"PRUNED (Bound {bound:.2f} <= Best {best_profit:.2f})"
            return

        if current_weight + items[index]['weight'] <= kapasitas_w:
            current_items.append(items[index])
            dfs(index + 1, current_weight + items[index]['weight'], current_profit + items[index]['profit'], current_items)
            current_items.pop()

        dfs(index + 1, current_weight, current_profit, current_items)

    dfs(0, 0, 0, [])
    return {
        "best_profit": round(best_profit, 2),
        "best_combination": best_combination,
        "nodes_visited": nodes_visited,
        "execution_time_ms": round((time.time()) * 1000, 4), # Placeholder waktu awal
        "exploration_log": exploration_log
    }




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
        
        # === INTEGRASI LOGIKA CALVIN COCOK DENGAN DATA JAYDEN ===
    # Mengirim data_list dari CSV ke fungsi dfs milik Calvin dengan Kapasitas W = 10
        start_time = time.time()
        hasil = jalankan_dfs(data_list, kapasitas_w=10)
        end_time = time.time()
        
        waktu_eksekusi = (end_time - start_time) * 1000

        print("Status: Berhasil Dieksekusi via Algoritma Calvin!")
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