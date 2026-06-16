"""
Menangani pemuatan data dari berbagai sumber

# src/utils/loader.py
# Modul pendukung (Utility) untuk menangani proses pembacaan file mentah (seperti CSV)
# dan mengonversinya menjadi struktur data dasar Python secara aman.
"""

def _try_numeric(value: str) -> str | int:
    """
    Mencoba mengubah teks (string) menjadi integer. Mengembalikan teks asli jika gagal.
    
    Fungsi internal untuk menebak tipe data secara otomatis.
    Semua input angka akan dipaksa menjadi Integer.
    Jika gagal, biarkan tetap String.
    """
    try:
        return int(value)
    except ValueError:
        return value


def load_csv(file_path: str) -> list[list[str | int]]:
    """
    Memuat file CSV ke dalam bentuk array/list.
    Nilai angka akan secara otomatis diubah menjadi integer.
    
    Fungsi utama untuk memuat file CSV ke dalam bentuk array/list Python.
    Memanfaatkan fungsi _try_numeric di atas agar kolom 'weight' dan 'profit' 
    langsung bisa dihitung tanpa tersangkut tipe string.
    """
    import csv

    data = []

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header:
            data.append(header)
        for row in reader:
            parsed_row = [_try_numeric(cell) for cell in row]
            if len(parsed_row) >= 3:
                w, p = parsed_row[1], parsed_row[2]
                if not isinstance(w, int) or not isinstance(p, int):
                    continue
                
                if w < 1 or p < 1:
                    continue
            data.append(parsed_row)
    return data