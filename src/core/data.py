# src/core/data.py
# Modul ini berfungsi sebagai utilitas ringan untuk mempersiapkan data mentah.

def siapkan_data_barang(daftar_barang_mentah):
    """
    Mengonversi daftar barang mentah (misal dari representasi CSV/Streamlit)
    menjadi list of dictionaries biasa agar mudah dimanipulasi oleh DFS.
    """
    return [dict(item) for item in daftar_barang_mentah]