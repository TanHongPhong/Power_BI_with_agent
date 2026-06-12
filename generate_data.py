"""
generate_data.py
================
Reproducible synthetic dataset for a Lean Six Sigma (DMAIC) portfolio project.

Scenario
--------
A Surface-Mount Technology (SMT) PCB assembly line. The Critical-to-Quality
(CTQ) characteristic is the SOLDER PASTE DEPOSIT HEIGHT (in microns), measured
by a Solder Paste Inspection (SPI) machine on a reference pad. Spec window is
120 um target, 100 um lower spec limit (LSL), 140 um upper spec limit (USL).

The data is engineered to tell a complete DMAIC story:
  * Weeks 1-4  = BASELINE process  (off-center, marginal capability)
  * Week 3     = a SPECIAL CAUSE (stencil clogging -> paste starvation) that
                 drags paste height down and causes a spike in the dominant
                 defect, "Insufficient solder".
  * Weeks 5-8  = IMPROVED process  (after a stencil-cleaning SOP is introduced;
                 recentered + tighter, defects fall sharply).

Three output files are written to ./data :
  * measurements.csv  -> continuous CTQ, in rational subgroups of 5
                         (drives capability Cp/Cpk and X-bar / R control charts)
  * inspections.csv   -> one row per inspected board
                         (drives p-chart, yield, and the DPMO denominator)
  * defects.csv       -> one row per individual defect, joins to inspections
                         (drives Pareto analysis and DPMO numerator)

Run:  python generate_data.py
Requires: numpy, pandas  (pip install numpy pandas)

The random seed is fixed, so the output is identical on every machine.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# A single seeded random generator => fully reproducible output.
RNG = np.random.default_rng(42)

# --------------------------------------------------------------------------
# Configuration -- change these in one place to rescale the whole dataset.
# --------------------------------------------------------------------------
WEEKS          = 8
DAYS_PER_WEEK  = 5                       # Mon-Fri production
SHIFT_HOURS    = list(range(6, 22))      # 06:00..21:00 -> 16 hourly subgroups/day
SUBGROUP_N     = 5                       # boards measured per hour for the X-bar/R chart
BOARDS_PER_HR  = 20                      # boards 100%-inspected per hour (for defects)
OPP_PER_BOARD  = 200                     # solder joints per board = DPMO "opportunities"

# CTQ specification (solder paste deposit height, microns)
TARGET, LSL, USL = 120.0, 100.0, 140.0

START = datetime(2025, 1, 6, 0, 0)       # a Monday; production calendar anchor

# Defect catalogue. Values are the expected number of defects per board
# (Poisson mean) in each phase. "Insufficient solder" is the vital-few driver
# and is additionally amplified when paste height runs low (see below).
DEFECT_LAMBDAS = {
    # defect_type            baseline  improved
    "Insufficient solder":  (0.30,     0.05),
    "Solder bridge":        (0.18,     0.07),
    "Component misalignment":(0.10,    0.05),
    "Tombstoning":          (0.07,     0.03),
    "Cold joint":           (0.06,     0.02),
    "Solder ball":          (0.05,     0.02),
    "Missing component":    (0.03,     0.015),
    "Lifted lead":          (0.02,     0.01),
}

OPERATORS = ["OP-1", "OP-2", "OP-3"]     # operator is a red herring: no real effect


def paste_mean_sigma(week, day_of_week, hour):
    """Return (process_mean, process_sigma) for a given hour of production.

    Encodes the three regimes: baseline, the week-3 stencil-clog special cause,
    and the improved process from week 5 onward.
    """
    if week >= 5:
        # Improved process: recentered on target, tighter spread.
        return 120.0, 5.0

    # Baseline process: runs a touch low and wide.
    mu, sigma = 116.0, 7.0

    # Special cause: stencil clogging on Wed-Thu of week 3 starves the paste.
    # Paste height sags through the two days, then a cleaning restores it.
    if week == 3 and day_of_week in (2, 3):           # Wed=2, Thu=3 (Mon=0)
        # Progress through the 2-day event as a 0..1 fraction.
        frac = (day_of_week - 2) / 1.0 + (hour - SHIFT_HOURS[0]) / (2 * len(SHIFT_HOURS))
        mu -= 12.0 * min(frac, 1.0)                   # drift down to ~104 um
    return mu, sigma


def lambda_for(defect_type, phase, paste_mu):
    """Per-board Poisson mean for a defect type, given phase and paste height.

    'Insufficient solder' scales up sharply as paste height drops below ~114 um,
    which is what links the control-chart excursion to the Pareto spike.
    """
    base, improved = DEFECT_LAMBDAS[defect_type]
    lam = improved if phase == "improved" else base
    if defect_type == "Insufficient solder" and phase == "baseline":
        lam += max(0.0, (114.0 - paste_mu)) * 0.18    # paste starvation surge
    return lam


# --------------------------------------------------------------------------
# Generation loop
# --------------------------------------------------------------------------
measurements = []
inspections  = []
defects      = []

measurement_id = 0
board_id       = 0
defect_id      = 0
subgroup_id    = 0

for week in range(1, WEEKS + 1):
    phase = "improved" if week >= 5 else "baseline"
    for day in range(DAYS_PER_WEEK):
        day_date = START + timedelta(weeks=week - 1, days=day)
        for hour in SHIFT_HOURS:
            ts = day_date.replace(hour=hour)
            shift = "A" if hour < 14 else "B"
            operator = OPERATORS[(week + day + hour) % len(OPERATORS)]
            mu, sigma = paste_mean_sigma(week, day, hour)
            subgroup_id += 1

            # --- continuous CTQ: one rational subgroup of SUBGROUP_N boards ---
            heights = RNG.normal(mu, sigma, SUBGROUP_N)
            for h in heights:
                measurement_id += 1
                measurements.append({
                    "measurement_id": measurement_id,
                    "timestamp": ts,
                    "subgroup_id": subgroup_id,
                    "week": week,
                    "phase": phase,
                    "shift": shift,
                    "operator": operator,
                    "paste_height_um": round(float(h), 2),
                })

            # --- attribute data: 100% inspection of BOARDS_PER_HR boards ---
            for _ in range(BOARDS_PER_HR):
                board_id += 1
                board_defects = 0
                for dtype in DEFECT_LAMBDAS:
                    lam = lambda_for(dtype, phase, mu)
                    n = int(RNG.poisson(lam))
                    board_defects += n
                    for _ in range(n):
                        defect_id += 1
                        defects.append({
                            "defect_id": defect_id,
                            "board_id": board_id,
                            "timestamp": ts,
                            "week": week,
                            "phase": phase,
                            "defect_type": dtype,
                        })
                inspections.append({
                    "board_id": board_id,
                    "timestamp": ts,
                    "week": week,
                    "phase": phase,
                    "shift": shift,
                    "operator": operator,
                    "opportunities": OPP_PER_BOARD,
                    "defect_count": board_defects,
                    "disposition": "FAIL" if board_defects > 0 else "PASS",
                })

df_meas = pd.DataFrame(measurements)
df_insp = pd.DataFrame(inspections)
df_def  = pd.DataFrame(defects)

df_meas.to_csv("data/measurements.csv", index=False)
df_insp.to_csv("data/inspections.csv", index=False)
df_def.to_csv("data/defects.csv", index=False)

# Small reference file so Power BI / SQL can pick up the spec window.
pd.DataFrame([{
    "ctq": "solder_paste_height_um", "target": TARGET, "lsl": LSL, "usl": USL,
    "subgroup_size": SUBGROUP_N, "opportunities_per_board": OPP_PER_BOARD,
}]).to_csv("data/specs.csv", index=False)


# --------------------------------------------------------------------------
# Console summary -- quick sanity check + the headline numbers for the README.
# --------------------------------------------------------------------------
def capability(values):
    mu, sd = values.mean(), values.std(ddof=1)
    cp  = (USL - LSL) / (6 * sd)
    cpk = min(USL - mu, mu - LSL) / (3 * sd)
    return mu, sd, cp, cpk


def sigma_level(dpmo):
    # Standard "process sigma" with the conventional 1.5-sigma shift.
    from math import erf, sqrt
    yield_ = 1 - dpmo / 1_000_000
    # invert the normal CDF via bisection (no scipy dependency)
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        cdf = 0.5 * (1 + erf(mid / sqrt(2)))
        lo, hi = (mid, hi) if cdf < yield_ else (lo, mid)
    return (lo + hi) / 2 + 1.5


print("=" * 60)
print("DATASET SUMMARY")
print("=" * 60)
print(f"measurements rows : {len(df_meas):>7,}   ({df_meas.subgroup_id.nunique()} subgroups)")
print(f"inspections  rows : {len(df_insp):>7,}   boards")
print(f"defects      rows : {len(df_def):>7,}   individual defects")
print()

for phase in ("baseline", "improved"):
    m = df_meas.loc[df_meas.phase == phase, "paste_height_um"]
    i = df_insp[df_insp.phase == phase]
    d = df_def[df_def.phase == phase]
    mu, sd, cp, cpk = capability(m)
    total_def = len(d)
    opp = i.opportunities.sum()
    dpmo = 1_000_000 * total_def / opp
    print(f"[{phase.upper()}]")
    print(f"  paste height  mean={mu:6.2f}  sd={sd:5.2f}  Cp={cp:4.2f}  Cpk={cpk:4.2f}")
    print(f"  fraction defective (p) = {(i.disposition=='FAIL').mean():.3f}")
    print(f"  DPMO = {dpmo:,.0f}   ->  process sigma = {sigma_level(dpmo):.2f}")
    print()

print("Top defects (baseline) — Pareto vital few:")
pareto = (df_def[df_def.phase == "baseline"]
          .defect_type.value_counts())
cum = 0
for name, cnt in pareto.items():
    cum += cnt
    print(f"  {name:24s} {cnt:6,}  ({cum/pareto.sum()*100:5.1f}% cumulative)")
