"""
Data preparation using numpy for vectorized computation.
Uses Struct-of-Arrays layout (parallel lists) instead of Array-of-Structs
(list of namedtuples) for faster preprocessing and scalar access in the DFS loop.

# src/optimize/data.py
# Modul pra-pemrosesan data tingkat lanjut. Menggunakan library komputasi matriks C (NumPy)
# untuk mengubah array objek (Array-of-Structs) menjadi sekumpulan List Paralel tunggal (Struct-of-Arrays).
# Cara ini sangat menghemat memori cache dan mempercepat akses data miliaran kali di Python.
"""
import numpy as np


def siapkan_data_barang(daftar_barang_mentah):
    """
    Convert raw item dicts into parallel Python lists, sorted by ratio descending.
    Uses numpy for vectorized ratio computation and argsort.

    Returns:
        labels: list[str]
        weights: list[float]
        profits: list[float]
        ratios: list[float]
    All sorted by profit/weight ratio in descending order.
    """
    import pandas as pd
    if isinstance(daftar_barang_mentah, pd.DataFrame):
        labels_raw = daftar_barang_mentah['label'].tolist()
        weights_np = daftar_barang_mentah['weight'].to_numpy(dtype=float)
        profits_np = daftar_barang_mentah['profit'].to_numpy(dtype=float)
    else:
        labels_raw = [item['label'] for item in daftar_barang_mentah]
        weights_np = np.array([float(item['weight']) for item in daftar_barang_mentah])
        profits_np = np.array([float(item['profit']) for item in daftar_barang_mentah])

    # Vectorized ratio computation (Hitung rasio massal secara serentak, cegah error bagi nol)
    with np.errstate(divide='ignore', invalid='ignore'):
        ratios_np = np.where(weights_np > 0, profits_np / weights_np, np.inf)

    # Sort by ratio descending using numpy argsort (faster than Python sorted)
    # Mencari tahu urutan indeks baru setelah di-sorting berdasar rasio terbesar (secara C-Native)
    order = np.argsort(-ratios_np)

    # Reorder and convert to Python lists for fast scalar access in DFS loop
    labels = [labels_raw[i] for i in order]
    weights = weights_np[order].tolist()
    profits = profits_np[order].tolist()
    ratios = ratios_np[order].tolist()

    return labels, weights, profits, ratios
