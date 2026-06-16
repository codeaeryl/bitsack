import time
from .data import siapkan_data_barang
from .sort import urutkan_berdasarkan_rasio
from .bound import calculate_upper_bound

# src/core/dfs.py
# Modul ini berisi logika utama algoritma Branch & Bound menggunakan pendekatan 
# Depth-First Search (DFS) secara rekursif murni (pemanggilan fungsi ke dalam fungsi itu sendiri).

def jalankan_dfs_modular(daftar_barang_mentah, kapasitas_w):
    """
    Fungsi utama untuk mengeksekusi DFS.
    Menerima daftar barang dan kapasitas tas (W).
    """
    # Menyiapkan dan mengurutkan barang berdasarkan rasio profit/berat (Penting untuk optimasi Bound)
    items = siapkan_data_barang(daftar_barang_mentah)
    items = urutkan_berdasarkan_rasio(items)
    
    n = len(items)
    best_profit = 0             # Menyimpan profit tertinggi yang ditemukan sejauh ini
    best_combination = []       # Menyimpan kombinasi barang terbaik sejauh ini
    nodes_visited = 0           # Menghitung total node yang dieksplorasi (kiri & kanan)
    exploration_log = []        # Log untuk kebutuhan visualisasi pohon Graphviz di app.py
    


    def dfs(index, current_weight, current_profit, current_items, parent_node=None):
        """
        Fungsi rekursif untuk menelusuri kemungkinan (Ambil atau Tidak Ambil barang).
        """
        nonlocal best_profit, best_combination, nodes_visited

        nodes_visited += 1
        current_node_id = nodes_visited
        
        chosen_names = [item['label'] for item in current_items]
        item_evaluasi = items[index]['label'] if index < n else "LEAF"
        
        # Fitur parent_node ditambahkan untuk UI Graphviz (Richard)
        exploration_log.append({
            "node": current_node_id,
            "parent": parent_node,
            "current_item": item_evaluasi, 
            "weight": current_weight,
            "profit": current_profit, 
            "chosen": chosen_names, 
            "status": "Eksplorasi"
        })
        
        # Jika tas tidak overkapasitas dan profit cabang ini mengalahkan rekor sebelumnya, update rekor!
        if current_weight <= kapasitas_w and current_profit > best_profit:
            best_profit = current_profit
            best_combination = list(current_items)
            
        # Jika indeks sudah mencapai ujung array barang, hentikan pencarian (Base Case)
        if index == n:
            return

        # Hitung prediksi batas atas menggunakan modul bound.py
        bound = calculate_upper_bound(index, current_weight, current_profit, items, n, kapasitas_w)
        
        # PRUNING (Pemangkasan Cabang): 
        # Jika prediksi profit di masa depan ternyata sama atau lebih kecil dari rekor terbaik, 
        # cabang ini terbukti tidak berguna. Potong sekarang juga!
        if bound <= best_profit:
            exploration_log[-1]["status"] = f"PRUNED (Bound {bound:.2f} <= Best {best_profit:.2f})"
            return

        # CABANG KIRI: Eksplorasi dengan MEMASUKKAN barang saat ini (jika muat)
        if current_weight + items[index]['weight'] <= kapasitas_w:
            current_items.append(items[index])
            dfs(index + 1, current_weight + items[index]['weight'], current_profit + items[index]['profit'], current_items, current_node_id)
            current_items.pop() # Backtrack: Keluarkan barang sebelum mencoba cabang kanan

        # CABANG KANAN: Eksplorasi dengan MENGABAIKAN (skip) barang saat ini
        dfs(index + 1, current_weight, current_profit, current_items, current_node_id)

    # Memulai pencarian dari indeks 0, beban 0, dan profit 0
    dfs(0, 0, 0, [], None)
    
    return {
        "best_profit": int(best_profit),
        "best_combination": best_combination,
        "nodes_visited": nodes_visited,
        "exploration_log": exploration_log,
        "timeout": False
    }