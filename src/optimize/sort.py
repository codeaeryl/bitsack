"""
Sorting is now integrated into data.py (numpy argsort).
This module is kept for API compatibility.
"""


def urutkan_berdasarkan_rasio(labels, weights, profits, ratios):
    """No-op: data is already sorted by ratio descending in data.py."""
    return labels, weights, profits, ratios
