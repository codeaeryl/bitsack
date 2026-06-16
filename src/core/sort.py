# src/core/sort.py
# Modul ini bertanggung jawab untuk pengurutan awal barang (pre-processing).

def urutkan_berdasarkan_rasio(items):
    """
    Fungsi untuk mengurutkan daftar barang berdasarkan nilai profit/berat secara menurun (descending).
    Pengurutan ini wajib dilakukan dalam Branch & Bound Knapsack 0/1 agar
    Bounding Function (heuristic) bisa bertindak 'rakus' (memasukkan barang terbaik lebih dulu).
    """
    for item in items:
        if item['weight'] > 0:
            # Hitung densitas / rasio keuntungan dari tiap barang
            item['ratio'] = item['profit'] / item['weight']
        else:
            # Jika beratnya 0 (tidak masuk akal secara fisik, tapi untuk safety), rasionya tak terhingga
            item['ratio'] = float('inf')
            
    # Lakukan sorting array Python bawaan berdasarkan nilai rasio tertinggi ke terendah
    items.sort(key=lambda x: x['ratio'], reverse=True)
    return items  