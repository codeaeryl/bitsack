"""
Optimised 0/1 Knapsack solver using iterative Branch & Bound DFS.

Optimisations applied:
  #2   Struct-of-Arrays (parallel lists) instead of Array-of-Structs (namedtuples)
  #3   Bound checked before entering child nodes (pre-recurse pruning)
  #4   Greedy heuristic seeds best_profit for aggressive early pruning
  #5   Iterative DFS with explicit stack (no recursion overhead / limit)
  #6   Prefix-sum + binary search O(log n) upper bound
  #7   Redundant weight feasibility check removed (only feasible nodes are pushed)
  #9   Sufficiency pruning (take all remaining if they fit)
  #10  Capacity pruning via suffix minimum weight
  #11  Numpy-accelerated preprocessing (argsort, cumsum, cummin)
  #12  Index-based tracking (store int indices on stack, not item objects)
"""
from .data import siapkan_data_barang
from .bound import BoundCalculator


def _greedy_solution(weights, profits, n, kapasitas_w):
    """
    Greedy heuristic: take items in ratio-descending order while they fit.
    Returns (profit, chosen_indices_tuple).
    """
    weight = 0.0
    profit = 0.0
    chosen = []
    for i in range(n):
        if weight + weights[i] <= kapasitas_w:
            weight += weights[i]
            profit += profits[i]
            chosen.append(i)
    return profit, tuple(chosen)


def jalankan_dfs_modular(daftar_barang_mentah, kapasitas_w):
    """
    Solve 0/1 Knapsack using an optimised iterative Branch & Bound DFS.
    API-compatible with core.dfs.jalankan_dfs_modular.
    """
    labels, weights, profits, ratios = siapkan_data_barang(daftar_barang_mentah)
    n = len(labels)

    bound_calc = BoundCalculator(weights, profits, ratios, kapasitas_w)

    # --- Optimisation #4: greedy initial bound --------------------------------
    best_profit, best_indices = _greedy_solution(weights, profits, n, kapasitas_w)

    nodes_visited = 0
    exploration_log = []
    visualize = True

    # Local references for hot-loop performance
    pw = bound_calc._prefix_weight
    pp = bound_calc._prefix_profit
    smw = bound_calc._suffix_min_weight
    bound_calculate = bound_calc.calculate

    # Stack entries: (index, current_weight, current_profit, chosen_indices_tuple, parent_node_id)
    stack = [(0, 0.0, 0.0, (), None)]

    while stack:
        index, cw, cp, chosen, parent_id = stack.pop()
        nodes_visited += 1
        current_node_id = nodes_visited

        if visualize:
            if len(exploration_log) > 1000:
                visualize = False
                exploration_log.clear()
            else:
                # Logging (preserved from original)
                chosen_names = [labels[i] for i in chosen]
                current_item_name = labels[index] if index < n else "LEAF"
                log_entry = {
                    "node": current_node_id,
                    "parent": parent_id,
                    "current_item": current_item_name,
                    "weight": round(cw, 2),
                    "profit": round(cp, 2),
                    "chosen": chosen_names,
                    "status": "Eksplorasi",
                }
                exploration_log.append(log_entry)

        if cp > best_profit:
            best_profit = cp
            best_indices = chosen

        if index == n:
            continue

        # --- Optimisation #9: Sufficiency Pruning ---
        total_remaining_weight = pw[n] - pw[index]
        if cw + total_remaining_weight <= kapasitas_w:
            total_remaining_profit = pp[n] - pp[index]
            potential_profit = cp + total_remaining_profit
            if potential_profit > best_profit:
                best_profit = potential_profit
                best_indices = chosen + tuple(range(index, n))
            
            if visualize:
                log_entry["status"] = "TAKEN ALL (Remaining fit)"
                log_entry["weight"] = round(cw + total_remaining_weight, 2)
                log_entry["profit"] = round(cp + total_remaining_profit, 2)
                log_entry["chosen"] = [labels[i] for i in best_indices]
            continue

        # --- Optimisation #10: Capacity Pruning ---
        if kapasitas_w - cw < smw[index]:
            if visualize:
                log_entry["status"] = "PRUNED (No item fits)"
            continue

        # --- Optimisation #3: pre-recurse bound check ---
        bound = bound_calculate(index, cw, cp)
        if bound <= best_profit:
            if visualize:
                log_entry["status"] = (
                    f"PRUNED (Bound {bound:.2f} <= Best {best_profit:.2f})"
                )
            continue

        # Push exclude branch first (deeper in stack → explored second)
        stack.append((index + 1, cw, cp, chosen, current_node_id))

        # Push include branch second (top of stack → explored first)
        w_i = weights[index]
        if cw + w_i <= kapasitas_w:
            stack.append((
                index + 1,
                cw + w_i,
                cp + profits[index],
                chosen + (index,),
                current_node_id,
            ))

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
