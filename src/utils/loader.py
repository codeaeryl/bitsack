"""
Handles loading data from various sources
"""

def _try_numeric(value: str) -> str | int | float:
    """
    Attempt to cast a string to int, then float. Return original string on failure.
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
    """
    import csv

    data = []

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append([_try_numeric(cell) for cell in row])
    return data