# src/core/bound.py
# Modul ini berisi fungsi heuristik penaksir (Bounding Function) untuk algoritma Branch & Bound.

def calculate_upper_bound(index, current_weight, current_profit, items, n, kapasitas_w):
    """
    Fungsi untuk menghitung batas atas (upper bound) potensi profit maksimal 
    yang bisa didapat jika kita meneruskan cabang node ini.
    Menggunakan pendekatan Knapsack Fraksional (barang bisa dipecah) untuk estimasi optimis.
    """
    # Jika berat saat ini sudah melebih kapasitas tas, otomatis tidak ada potensi profit tambahan
    if current_weight >= kapasitas_w:
        return 0
        
    bound = current_profit
    total_weight = current_weight
    j = index
    
    # Masukkan barang utuh selama kapasitas tas masih muat
    while j < n and total_weight + items[j]['weight'] <= kapasitas_w:
        total_weight += items[j]['weight']
        bound += items[j]['profit']
        j += 1
        
    # Jika tas belum penuh tapi barang utuh berikutnya tidak muat,
    # potong barang tersebut (ambil pecahannya saja) untuk mengisi sisa kapasitas tas.
    if j < n:
        bound += (kapasitas_w - total_weight) * items[j]['ratio']
        
    return bound