from .data import siapkan_data_barang
from .sort import urutkan_berdasarkan_rasio
from .bound import calculate_upper_bound

def jalankan_dfs_modular(daftar_barang_mentah, kapasitas_w):
    items = siapkan_data_barang(daftar_barang_mentah)
    items = urutkan_berdasarkan_rasio(items)
    
    n = len(items)
    best_profit = 0.0
    best_combination = []
    nodes_visited = 0
    exploration_log = []

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

        bound = calculate_upper_bound(index, current_weight, current_profit, items, n, kapasitas_w)
        
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
        "exploration_log": exploration_log
    }