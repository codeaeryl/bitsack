"""
Data preparation using numpy for vectorized computation.
Uses Struct-of-Arrays layout (parallel lists) instead of Array-of-Structs
for faster preprocessing and scalar access in the DFS loop.

# src/core/data.py
# Modul pra-pemrosesan data menggunakan library komputasi matriks C (NumPy)
# untuk sorting dan konversi data secara efisien.
"""
import numpy as np


def siapkan_data_barang(daftar_barang_mentah):
    """
    Convert raw item dicts into parallel Python lists, sorted by weight descending.
    Uses numpy for vectorized sorting (argsort).

    Returns:
        labels: list[str]
        weights: list[int]
        profits: list[int]
    All sorted by weight in descending order (heaviest first for earlier pruning).
    """
    import pandas as pd
    if isinstance(daftar_barang_mentah, pd.DataFrame):
        labels_raw = daftar_barang_mentah['label'].tolist()
        weights_np = daftar_barang_mentah['weight'].to_numpy(dtype=int)
        profits_np = daftar_barang_mentah['profit'].to_numpy(dtype=int)
    else:
        labels_raw = [item['label'] for item in daftar_barang_mentah]
        weights_np = np.array([int(item['weight']) for item in daftar_barang_mentah])
        profits_np = np.array([int(item['profit']) for item in daftar_barang_mentah])

    # Sort by weight descending using numpy argsort (faster than Python sorted)
    # Barang terberat dievaluasi duluan agar pruning terjadi lebih awal
    order = np.argsort(-weights_np)

    # Reorder and convert to Python lists for fast scalar access in DFS loop
    labels = [labels_raw[i] for i in order]
    weights = weights_np[order].tolist()
    profits = profits_np[order].tolist()

    return labels, weights, profits