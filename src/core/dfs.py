import time
import numpy as np
from .data import siapkan_data_barang

# src/core/dfs.py
# Modul ini berisi logika utama algoritma menggunakan pendekatan 
# Depth-First Search (DFS) secara rekursif murni (pemanggilan fungsi ke dalam fungsi itu sendiri).
# Dioptimasi dengan NumPy untuk preprocessing dan Struct-of-Arrays untuk akses data cepat.

def jalankan_dfs_modular(daftar_barang_mentah, kapasitas_w):
    """
    Fungsi utama untuk mengeksekusi DFS.
    Menerima daftar barang dan kapasitas tas (W).
    Menggunakan NumPy-accelerated preprocessing dan Struct-of-Arrays layout.
    """
    # Menyiapkan data barang (NumPy-accelerated, sorted by weight descending)
    labels, weights, profits = siapkan_data_barang(daftar_barang_mentah)
    
    n = len(labels)
    
    weights_np = np.array(weights)
    
    # Suffix minimum weight menggunakan NumPy untuk capacity pruning
    # Jika barang teringan yang tersisa pun tidak muat, hentikan penelusuran
    smw = [float('inf')] * (n + 1)
    if n > 0:
        reversed_cummin = np.minimum.accumulate(weights_np[::-1])[::-1]
        smw[:n] = reversed_cummin.tolist()
    
    best_profit = 0             # Menyimpan profit tertinggi yang ditemukan sejauh ini
    best_combination = []       # Menyimpan kombinasi barang terbaik sejauh ini
    best_node_id = None         # Menyimpan ID node yang mencapai solusi terbaik
    nodes_visited = -1          # Menghitung total node yang dieksplorasi (dimulai dari 0)
    exploration_log = []        # Log untuk kebutuhan visualisasi pohon Graphviz di app.py
    


    def dfs(index, current_weight, current_profit, chosen_indices, parent_node=None):
        """
        Fungsi rekursif untuk menelusuri kemungkinan (Ambil atau Tidak Ambil barang).
        Menggunakan index-based tracking untuk efisiensi memori.
        """
        nonlocal best_profit, best_combination, best_node_id, nodes_visited

        nodes_visited += 1
        current_node_id = nodes_visited
        
        chosen_names = [labels[i] for i in chosen_indices]
        item_evaluasi = "ROOT" if parent_node is None else (labels[index] if index < n else "LEAF")
        
        # Fitur parent_node ditambahkan untuk UI Graphviz (Richard)
        log_entry = {
            "node": current_node_id,
            "parent": parent_node,
            "current_item": item_evaluasi, 
            "weight": current_weight,
            "profit": current_profit, 
            "chosen": chosen_names, 
            "status": "Eksplorasi"
        }
        exploration_log.append(log_entry)
        
        # Jika tas tidak overkapasitas dan profit cabang ini mengalahkan rekor sebelumnya, update rekor!
        if current_weight <= kapasitas_w and current_profit > best_profit:
            best_profit = current_profit
            best_combination = [{"label": labels[i], "weight": weights[i], "profit": profits[i]} for i in chosen_indices]
            best_node_id = current_node_id
            
        # Jika indeks sudah mencapai ujung array barang, hentikan pencarian (Base Case)
        if index == n:
            return


        
        # --- OPTIMASI: Capacity Pruning (NumPy suffix-min) ---
        # Jika barang teringan yang tersisa pun tidak muat, hentikan cabang ini
        if kapasitas_w - current_weight < smw[index]:
            if current_weight == kapasitas_w:
                log_entry["status"] = "LEAF"
            else:
                log_entry["status"] = "PRUNED"
            return

        # CABANG KIRI: Eksplorasi dengan MEMASUKKAN barang saat ini (jika muat)
        if current_weight + weights[index] <= kapasitas_w:
            dfs(index + 1, current_weight + weights[index], current_profit + profits[index], chosen_indices + (index,), current_node_id)
        else:
            # PRUNED: Barang tidak muat, catat node yang dipangkas (menunjukkan backtracking)
            nodes_visited += 1
            pruned_node_id = nodes_visited
            pruned_weight = current_weight + weights[index]
            pruned_profit = current_profit + profits[index]
            pruned_names = [labels[i] for i in chosen_indices] + [labels[index]]
            exploration_log.append({
                "node": pruned_node_id,
                "parent": current_node_id,
                "current_item": labels[index + 1] if index + 1 < n else "LEAF",
                "weight": pruned_weight,
                "profit": pruned_profit,
                "chosen": pruned_names,
                "status": "PRUNED"
            })

        # CABANG KANAN: Eksplorasi dengan MENGABAIKAN (skip) barang saat ini
        dfs(index + 1, current_weight, current_profit, chosen_indices, current_node_id)

    # Memulai pencarian dari indeks 0, beban 0, dan profit 0
    dfs(0, 0, 0, (), None)
    
    return {
        "best_profit": int(best_profit),
        "best_combination": best_combination,
        "best_node_id": best_node_id,
        "nodes_visited": nodes_visited + 1,
        "exploration_log": exploration_log,
        "timeout": False
    }