"""Task 2 - Independent verification of operating-unit RWA and capital adequacy ratios.

Recomputes RWA with FRB standardized weights, compares with unit submissions and tests
CET1/RWA against the 10.5% Basel III minimum (incl. capital conservation buffer).
"""
import openpyxl, pandas as pd
from common import DATA, OUT

MIN_RATIO = 0.105
FRB_RW = {"Loans for Cards": 1.00, "Consumer Mortgages": 0.55, "Retail Banking": 0.90, "Unsecured Retail Lending": 1.00}
ws = openpyxl.load_workbook(DATA / "RWA_Info_from_Operating_Units.xlsx", data_only=True)["Sheet1"]
units = [ws.cell(2, c).value for c in range(2, 6)]
bal = pd.DataFrame({ws.cell(r, 1).value: [ws.cell(r, c).value for c in range(2, 6)] for r in range(3, 7)}, index=units)
cet1 = pd.Series([ws.cell(8, c).value for c in range(2, 6)], index=units)
rep_rwa = pd.Series([ws.cell(10, c).value for c in range(2, 6)], index=units)
used_rw = {ws.cell(r, 1).value: ws.cell(r, 2).value for r in range(17, 21)}

res = pd.DataFrame({"CET1": cet1, "Reported RWA": rep_rwa})
res["RWA at units' own weights"] = bal.mul(pd.Series(used_rw)).sum(axis=1)
res["Recalculated RWA (FRB)"] = bal.mul(pd.Series(FRB_RW)).sum(axis=1)
res["Reported ratio"] = res["CET1"] / res["Reported RWA"]
res["Recalculated ratio"] = res["CET1"] / res["Recalculated RWA (FRB)"]
res["Unexplained RWA gap"] = res["Reported RWA"] - res["RWA at units' own weights"]
res["Meets 10.5%?"] = res["Recalculated ratio"] >= MIN_RATIO
res["CET1 shortfall"] = (MIN_RATIO * res["Recalculated RWA (FRB)"] - res["CET1"]).clip(lower=0)
res.round(4).to_csv(OUT / "rwa_verification.csv"); print(res.round(3).T)
