def urutkan_berdasarkan_rasio(items):
    for item in items:
        if item['weight'] > 0:
            item['ratio'] = item['profit'] / item['weight']
        else:
            item['ratio'] = float('inf')
            
    items.sort(key=lambda x: x['ratio'], reverse=True)
    return items 