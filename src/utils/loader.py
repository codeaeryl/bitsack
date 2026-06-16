"""
Handles loading data from various sources

# src/utils/loader.py
# Modul pendukung (Utility) untuk menangani proses pembacaan file mentah (seperti CSV)
# dan mengonversinya menjadi struktur data dasar Python secara aman.
"""

def _try_numeric(value: str) -> str | int | float:
    """
    Attempt to cast a string to int, then float. Return original string on failure.
    
    Fungsi internal untuk menebak tipe data secara otomatis.
    Jika sebuah teks angka bisa diubah ke Integer (tanpa koma desimal), ubah ke Integer.
    Jika ada komanya, ubah ke Float. Jika gagal semuanya, biarkan tetap String.
    """
    try:
        num = float(value)
        if num == int(num):
            return int(num)
        return num
    except (ValueError, OverflowError):
        return value


def load_csv(file_path: str) -> list[list[str | int | float]]:
    """
    Load CSV file into a list object.
    Numeric values are automatically cast to int or float.
    
    Fungsi utama untuk memuat file CSV ke dalam bentuk array/list Python.
    Memanfaatkan fungsi _try_numeric di atas agar kolom 'weight' dan 'profit' 
    langsung bisa dihitung tanpa tersangkut tipe string.
    """
    import csv

    data = []

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append([_try_numeric(cell) for cell in row])
    return data