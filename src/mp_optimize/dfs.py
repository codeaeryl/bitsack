import os
import time
import multiprocessing
from optimize.data import siapkan_data_barang
from optimize.bound import BoundCalculator

def _greedy_solution(weights, profits, n, kapasitas_w):
    weight = 0.0
    profit = 0.0
    chosen = []
    for i in range(n):
        if weight + weights[i] <= kapasitas_w:
            weight += weights[i]
            profit += profits[i]
            chosen.append(i)
    return profit, tuple(chosen)

def _solve_subproblem_worker(args):
    """
    Worker function executed in child processes.
    args: (index, cw, cp, chosen, weights, profits, ratios, kapasitas_w, best_profit_global, labels)
    """
    index, cw, cp, chosen, weights, profits, ratios, kapasitas_w, best_profit_global, labels = args
    n = len(weights)
    
    bound_calc = BoundCalculator(weights, profits, ratios, kapasitas_w)
    
    stack = [(index, cw, cp, chosen)]
    
    best_profit = best_profit_global
    best_indices = ()
    nodes_visited = 0
    exploration_log = []
    
    pw = bound_calc._prefix_weight
    pp = bound_calc._prefix_profit
    smw = bound_calc._suffix_min_weight
    bound_calculate = bound_calc.calculate
    
    while stack:
        idx, current_w, current_p, current_chosen = stack.pop()
        nodes_visited += 1
        
        chosen_names = [labels[i] for i in current_chosen]
        log_entry = {
            "node": nodes_visited,
            "weight": round(current_w, 2),
            "profit": round(current_p, 2),
            "chosen": chosen_names,
            "status": "Eksplorasi",
        }
        exploration_log.append(log_entry)
        
        if current_p > best_profit:
            best_profit = current_p
            best_indices = current_chosen
            
        if idx == n:
            continue
            
        # Sufficiency Pruning
        total_remaining_weight = pw[n] - pw[idx]
        if current_w + total_remaining_weight <= kapasitas_w:
            total_remaining_profit = pp[n] - pp[idx]
            potential_profit = current_p + total_remaining_profit
            if potential_profit > best_profit:
                best_profit = potential_profit
                best_indices = current_chosen + tuple(range(idx, n))
            log_entry["status"] = "TAKEN ALL (Remaining fit)"
            continue
            
        # Capacity Pruning
        if kapasitas_w - current_w < smw[idx]:
            log_entry["status"] = "PRUNED (No item fits)"
            continue
            
        # Bound check
        bound = bound_calculate(idx, current_w, current_p)
        if bound <= best_profit:
            log_entry["status"] = f"PRUNED (Bound {bound:.2f} <= Best {best_profit:.2f})"
            continue
            
        # Push exclude
        stack.append((idx + 1, current_w, current_p, current_chosen))
        
        # Push include
        w_i = weights[idx]
        if current_w + w_i <= kapasitas_w:
            stack.append((
                idx + 1,
                current_w + w_i,
                current_p + profits[idx],
                current_chosen + (idx,),
            ))
            
    return best_profit, best_indices, nodes_visited, exploration_log

def _generate_subproblems(weights, profits, ratios, kapasitas_w, labels, target_count):
    bound_calc = BoundCalculator(weights, profits, ratios, kapasitas_w)
    n = len(weights)
    best_profit, best_indices = _greedy_solution(weights, profits, n, kapasitas_w)
    
    queue = [(0, 0.0, 0.0, ())]
    nodes_visited = 0
    exploration_log = []
    
    pw = bound_calc._prefix_weight
    pp = bound_calc._prefix_profit
    smw = bound_calc._suffix_min_weight
    bound_calculate = bound_calc.calculate
    
    while queue and len(queue) < target_count:
        state = queue.pop(0)
        idx, cw, cp, chosen = state
        nodes_visited += 1
        
        chosen_names = [labels[i] for i in chosen]
        log_entry = {
            "node": nodes_visited,
            "weight": round(cw, 2),
            "profit": round(cp, 2),
            "chosen": chosen_names,
            "status": "Eksplorasi",
        }
        exploration_log.append(log_entry)
        
        if cp > best_profit:
            best_profit = cp
            best_indices = chosen
            
        if idx == n:
            queue.append(state)
            if all(s[0] == n for s in queue):
                break
            continue
            
        # Sufficiency Pruning
        total_remaining_weight = pw[n] - pw[idx]
        if cw + total_remaining_weight <= kapasitas_w:
            total_remaining_profit = pp[n] - pp[idx]
            potential_profit = cp + total_remaining_profit
            if potential_profit > best_profit:
                best_profit = potential_profit
                best_indices = chosen + tuple(range(idx, n))
            log_entry["status"] = "TAKEN ALL (Remaining fit)"
            continue
            
        # Capacity Pruning
        if kapasitas_w - cw < smw[idx]:
            log_entry["status"] = "PRUNED (No item fits)"
            continue
            
        # Bound check
        bound = bound_calculate(idx, cw, cp)
        if bound <= best_profit:
            log_entry["status"] = f"PRUNED (Bound {bound:.2f} <= Best {best_profit:.2f})"
            continue
            
        # Exclude
        queue.append((idx + 1, cw, cp, chosen))
        
        # Include
        w_i = weights[idx]
        if cw + w_i <= kapasitas_w:
            queue.append((idx + 1, cw + w_i, cp + profits[idx], chosen + (idx,)))
            
    return queue, best_profit, best_indices, nodes_visited, exploration_log

def jalankan_dfs_modular(daftar_barang_mentah, kapasitas_w):
    labels, weights, profits, ratios = siapkan_data_barang(daftar_barang_mentah)
    n = len(labels)
    
    cpu_count = os.cpu_count() or 1
    
    # Threshold check: small problem or single CPU -> run sequentially
    if n <= 12 or cpu_count < 2:
        print(f"ℹ️ running sequentially (n={n}, cpus={cpu_count})")
        # Run sequentially
        bound_calc = BoundCalculator(weights, profits, ratios, kapasitas_w)
        best_profit, best_indices = _greedy_solution(weights, profits, n, kapasitas_w)
        
        nodes_visited = 0
        exploration_log = []
        pw = bound_calc._prefix_weight
        pp = bound_calc._prefix_profit
        smw = bound_calc._suffix_min_weight
        bound_calculate = bound_calc.calculate
        
        stack = [(0, 0.0, 0.0, ())]
        while stack:
            idx, cw, cp, chosen = stack.pop()
            nodes_visited += 1
            
            chosen_names = [labels[i] for i in chosen]
            log_entry = {
                "node": nodes_visited,
                "weight": round(cw, 2),
                "profit": round(cp, 2),
                "chosen": chosen_names,
                "status": "Eksplorasi",
            }
            exploration_log.append(log_entry)
            
            if cp > best_profit:
                best_profit = cp
                best_indices = chosen
                
            if idx == n:
                continue
                
            total_remaining_weight = pw[n] - pw[idx]
            if cw + total_remaining_weight <= kapasitas_w:
                total_remaining_profit = pp[n] - pp[idx]
                potential_profit = cp + total_remaining_profit
                if potential_profit > best_profit:
                    best_profit = potential_profit
                    best_indices = chosen + tuple(range(idx, n))
                log_entry["status"] = "TAKEN ALL (Remaining fit)"
                continue
                
            if kapasitas_w - cw < smw[idx]:
                log_entry["status"] = "PRUNED (No item fits)"
                continue
                
            bound = bound_calculate(idx, cw, cp)
            if bound <= best_profit:
                log_entry["status"] = f"PRUNED (Bound {bound:.2f} <= Best {best_profit:.2f})"
                continue
                
            stack.append((idx + 1, cw, cp, chosen))
            w_i = weights[idx]
            if cw + w_i <= kapasitas_w:
                stack.append((idx + 1, cw + w_i, cp + profits[idx], chosen + (idx,)))
                
        best_combination = [
            {"label": labels[i], "weight": weights[i], "profit": profits[i]}
            for i in best_indices
        ]
        return {
            "best_profit": round(best_profit, 2),
            "best_combination": best_combination,
            "nodes_visited": nodes_visited,
            "exploration_log": exploration_log,
        }

    # Parallel implementation
    target_tasks = cpu_count * 4
    subproblems, best_profit, best_indices, bfs_nodes, bfs_log = _generate_subproblems(
        weights, profits, ratios, kapasitas_w, labels, target_tasks
    )
    
    print(f"🚀 Running in Parallel (CPUs: {cpu_count}, Generated Subproblems: {len(subproblems)})")
    
    active_subproblems = [sub for sub in subproblems if sub[0] < n]
    
    # Prepare worker arguments
    worker_args = []
    for sub in active_subproblems:
        # sub: (idx, cw, cp, chosen)
        worker_args.append((
            sub[0], sub[1], sub[2], sub[3],
            weights, profits, ratios, kapasitas_w, best_profit, labels
        ))
        
    nodes_visited = bfs_nodes
    exploration_log = list(bfs_log)
    
    if worker_args:
        with multiprocessing.Pool(processes=cpu_count) as pool:
            results = pool.map(_solve_subproblem_worker, worker_args)
            
        current_node_index = bfs_nodes
        for res_profit, res_indices, res_nodes, res_log in results:
            for entry in res_log:
                current_node_index += 1
                entry["node"] = current_node_index
            nodes_visited += len(res_log)
            exploration_log.extend(res_log)
            if res_profit > best_profit:
                best_profit = res_profit
                best_indices = res_indices
                
    # Reconstruct best combination from indices
    best_combination = [
        {"label": labels[i], "weight": weights[i], "profit": profits[i]}
        for i in best_indices
    ]
    
    return {
        "best_profit": round(best_profit, 2),
        "best_combination": best_combination,
        "nodes_visited": nodes_visited,
        "exploration_log": exploration_log,
    }
