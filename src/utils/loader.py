import numpy as np

def load_csv(file_path: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Load CSV file using NumPy.
    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: (label, weight, profit)
    """
    data = np.genfromtxt(file_path, delimiter=',', dtype=None, names=True, encoding='utf-8')
    return data['label'], data['weight'].astype(float), data['profit'].astype(float)