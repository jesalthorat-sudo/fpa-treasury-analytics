"""Shared paths and helpers."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

NAVY, SLATE, RED, GREEN, AMBER, GREY = "#002D72", "#44546A", "#C8102E", "#2E7D32", "#D98E04", "#A6B1C2"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})
