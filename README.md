# FP&A and Treasury Analytics: Four Finance Analyst Case Studies

Python workflows and executive deliverables for four common finance-analyst tasks in a large bank: forecast KPI reporting, regulatory capital verification, scenario analysis, and daily liquidity-limit monitoring. Each task is reproducible from raw data to charts, with the executive decks and workbook that went to stakeholders in `docs/`.

> **Disclosure:** this is a portfolio case study built from a Citi Finance-style job-simulation brief and its provided datasets. It is not work done at Citi, and the data is illustrative. Replace the data in `data/` to reuse the code.

## Results at a glance

| # | Question | Method | Finding |
|---|---|---|---|
| 1 | What drove FY22E vs FY21A performance? | KPI roll-up and net income bridge | Revenue +$989m (+5.8%) and opex -$547m (-4.0%) were outweighed by a $2.3bn swing in cost of credit; net income -20.8% to $2,513m |
| 2 | Are unit capital ratios right? | Recompute RWA with FRB risk weights; test CET1/RWA vs 10.5% | All four units used a 25% card weight (should be 100%). Unit D's reported RWA ($200.2m) cannot be reconciled (true $462.5m, ratio 4.3% vs 10.0% reported). Units C and D below minimum |
| 3 | Will Omicron hurt card sales? | Correlate 2020-21 cases with spending by category | Weak link (r = 0.2-0.4). Troughs tracked restrictions, not case counts. Social and work-related spending most exposed; low risk overall |
| 4 | Are deposit/loan limits breached? | Daily EWT/MAT rules engine | Entity 1 in MAT from 15 Feb (surplus $(19.1)m on 28 Feb); Entity 2 at its surplus EWT; Entity 3 isolated daily moves |

## Repository layout

```
data/      raw input workbooks (illustrative)
src/       one script per task + common.py
outputs/   generated CSVs and charts
docs/      executive slide decks (.pptx) and RWA verification workbook (.xlsx)
run_all.sh runs all four analyses
```

## Run it

```bash
pip install -r requirements.txt
./run_all.sh
```

## Method notes

- **Task 1:** the net income bridge reconciles exactly to reported net income (the "Other" bar is discontinued operations and non-controlling interests). Percentage change is shown as not meaningful (NM) where the 2021 base is negative.
- **Task 2:** RWA = sum of asset balance x risk weight. Ratio = CET1 / RWA, tested against 10.5% (8% total capital + 2.5% conservation buffer). The brief tests CET1 only, which is stricter than the Basel definition (Tier 1 + Tier 2); flagged in the write-up.
- **Task 3:** Pearson correlation of 7-day average cases with the spending index, Mar-20 to Dec-21. The dataset has no 2022 spending, so the Omicron conclusion is an inference from history, not a measured impact. Correlation is not causation: restrictions and seasonality drive much of the pattern.
- **Task 4:** EWT/MAT thresholds are strict ("more than 3%" / "more than 5%"); moves of exactly 3.0% or 5.0% are treated as at-limit, not breaches. Equality is tested with a small tolerance to avoid floating-point noise.

## Skills demonstrated

Financial statement analysis and variance bridges, Basel III capital adequacy, risk-weighted asset validation, scenario and correlation analysis, liquidity trigger monitoring, Python (pandas, openpyxl, matplotlib), and executive communication (PowerPoint, Excel, email).
