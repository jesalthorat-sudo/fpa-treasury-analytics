"""Task 1 - FY22 forecast vs FY21 actual: KPI movements and net income bridge.

Reads the consolidated income statement, computes revenue, opex, cost of credit and
net income movements, and rebuilds the net income bridge (2021A -> 2022E).
"""
import openpyxl, pandas as pd
import matplotlib.pyplot as plt
from common import DATA, OUT, NAVY, RED, GREEN

ws = openpyxl.load_workbook(DATA / "YE_22.xlsx", data_only=True)["Income Statement"]
rows = {}
for r in ws.iter_rows(values_only=True):
    label = next((c for c in r[1:5] if isinstance(c, str)), None)
    nums = [c for c in r if isinstance(c, (int, float))]
    if label and len(nums) >= 2:
        rows[label.strip()] = (nums[0], nums[1])  # (2021A, 2022E)

def g(label): return rows[label]
REV, OPX = "Total revenues, net of interest expense", "Total operating expenses"
COC, NI, TAX = "Total provisions for credit losses and for benefits and claims(3)", "Citigroup's net income", "Provision for income taxes(4)"
kpi = pd.DataFrame({"2021A": [g(k)[0] for k in (REV, OPX, COC, NI)], "2022E": [g(k)[1] for k in (REV, OPX, COC, NI)]},
                   index=["Revenues", "Operating expenses", "Cost of credit", "Net income"])
kpi["Change"] = kpi["2022E"] - kpi["2021A"]
kpi["Change %"] = (kpi["Change"] / kpi["2021A"]).where(kpi["2021A"] > 0).round(3)  # NM when base is negative
kpi.to_csv(OUT / "kpi_summary.csv"); print(kpi)

# Net income bridge ($m): favourable = +, adverse = -
rev, opx, coc = kpi.loc["Revenues", "Change"], -kpi.loc["Operating expenses", "Change"], -kpi.loc["Cost of credit", "Change"]
tax = g(TAX)[0] - g(TAX)[1]
ni0, ni1 = kpi.loc["Net income", "2021A"], kpi.loc["Net income", "2022E"]
other = ni1 - (ni0 + rev + opx + coc + tax)   # discontinued ops and non-controlling interests
steps = [("2021A", ni0, "t"), ("Revenues", rev, "d"), ("Expenses", opx, "d"), ("Cost of credit", coc, "d"),
         ("Taxes", tax, "d"), ("Other", other, "d"), ("2022E", ni1, "t")]
fig, ax = plt.subplots(figsize=(9, 4.5)); cum = 0
for i, (n, v, k) in enumerate(steps):
    if k == "t": ax.bar(i, v, color=NAVY); cum = v; y = v
    else: ax.bar(i, v, bottom=cum, color=GREEN if v > 0 else RED); y = max(cum, cum + v); cum += v
    ax.text(i, y + 40, f"{v:+,.0f}" if k == "d" else f"{v:,.0f}", ha="center", fontsize=9)
ax.set_xticks(range(len(steps))); ax.set_xticklabels([s[0] for s in steps]); ax.set_title("Citigroup net income bridge, 2021A to 2022E ($m)")
plt.tight_layout(); plt.savefig(OUT / "net_income_bridge.png", dpi=150)
print("bridge:", dict((s[0], round(s[1])) for s in steps))
