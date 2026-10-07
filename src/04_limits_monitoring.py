"""Task 4 - Daily EWT/MAT limits monitoring for deposits and loans (Entities 1-3, Jan-Feb 2023).

EWT: deposits -3% d/d; loans +5% d/d; loans > 150% of Dec-22; surplus < 50% of Dec-22.  MAT: surplus < 0.
Surplus = D - L. Stressed surplus = 0.9 D - 1.2 L. Moves exactly at a threshold are not breaches.
"""
import openpyxl, pandas as pd
import matplotlib.pyplot as plt
from common import DATA, OUT, NAVY, RED, AMBER

w = openpyxl.load_workbook(DATA / "Task_4-Data.xlsx", data_only=True)["Data"]
n = sum(1 for c in range(2, 80) if w.cell(3, c).value is not None)
idx = pd.to_datetime([w.cell(3, c).value for c in range(2, 2 + n)])
dep = pd.DataFrame({i: [w.cell(3 + i, c).value for c in range(2, 2 + n)] for i in (1, 2, 3)}, index=idx)
loan = pd.DataFrame({i: [w.cell(8 + i, c).value for c in range(2, 2 + n)] for i in (1, 2, 3)}, index=idx)
sur, st = dep - loan, 0.9 * dep - 1.2 * loan
EPS = 1e-6  # exact-threshold moves are at-limit, not breaches (guards against float noise)
dd, ld = dep.pct_change().round(6), loan.pct_change().round(6)

log = []
for i in (1, 2, 3):
    l0, s0 = loan[i].iloc[0], sur[i].iloc[0]
    for d, v in dd[i][dd[i] < -0.03 - EPS].items(): log.append((i, d, "EWT deposit fall >3%", v))
    for d, v in ld[i][ld[i] > 0.05 + EPS].items(): log.append((i, d, "EWT loan rise >5%", v))
    for d, v in loan[i][loan[i] > 1.5 * l0].items(): log.append((i, d, "EWT loan >150% of Dec-22", v / l0 - 1))
    for d, v in sur[i][sur[i] < 0.5 * s0].items(): log.append((i, d, "EWT surplus <50% of Dec-22", v))
    for d, v in sur[i][sur[i] < 0].items(): log.append((i, d, "MAT surplus <0", v))
log = pd.DataFrame(log, columns=["Entity", "Date", "Trigger", "Level"]).sort_values(["Entity", "Trigger", "Date"])
log.to_csv(OUT / "breach_log.csv", index=False)
print(log.groupby(["Entity", "Trigger"]).agg(days=("Date", "count"), first=("Date", "min")).reset_index().to_string(index=False))

for i in (1, 2, 3):
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(sur.index, sur[i], color=NAVY, lw=2, label="Surplus"); ax.plot(st.index, st[i], color="#1B9AAA", lw=2, label="Stressed surplus")
    ax.axhline(0.5 * sur[i].iloc[0], color=AMBER, ls="--", label="EWT: 50% of Dec-22 surplus"); ax.axhline(0, color=RED, ls="--", label="MAT: zero")
    ax.set_title(f"Entity {i}: surplus and stressed surplus ($m)"); ax.legend(frameon=False, ncol=2); plt.tight_layout(); plt.savefig(OUT / f"entity{i}_surplus.png", dpi=150); plt.close()
