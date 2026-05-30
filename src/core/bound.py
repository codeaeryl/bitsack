def calculate_upper_bound(index, current_weight, current_profit, items, n, kapasitas_w):
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