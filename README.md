# Lean Sigma Learner's Portfolio

A Lean Six Sigma (DMAIC) case study built on a **purpose-generated dataset** for
a Surface-Mount Technology (SMT) printed-circuit-board assembly line. The data is
synthetic but engineered to behave like a real process: it has a marginal baseline,
a genuine special cause, and a measurable improvement — so every classic Six Sigma
tool (capability, control charts, Pareto, DPMO, hypothesis testing) has something
real to find.

> **Data is simulated.** It is produced by a seeded generator (`generate_data.py`)
> so anyone can clone this repo and reproduce the *exact* same files. Real quality
> measurement data is almost never published, so a reproducible synthetic dataset
> is the standard approach for a Six Sigma portfolio.

---

## The process (Define)

| | |
|---|---|
| **Process** | SMT line: solder-paste print → place → reflow |
| **CTQ characteristic** | Solder paste **deposit height** (µm), measured by SPI on a reference pad |
| **Specification** | Target **120 µm**, LSL **100 µm**, USL **140 µm** |
| **Sampling** | Rational subgroups of **5** boards, once per production hour |
| **Inspection** | 100% inspection of boards for attribute defects (200 solder joints / board = DPMO opportunities) |
| **Timeframe** | 8 weeks, 2 shifts/day, Mon–Fri |

The story built into the data:

- **Weeks 1–4 — baseline:** the print process runs low and wide; capability is poor.
- **Week 3 — special cause:** the stencil begins **clogging** (paste starvation), dragging deposit height down and triggering a spike in the dominant defect.
- **Week 5 onward — improved:** an under-stencil-wipe / cleaning SOP recenters the process and tightens variation; defects fall sharply.

---

## Headline results

These numbers are computed directly from the generated data (printed by the script):

| Metric | Baseline (wk 1–4) | Improved (wk 5–8) | Change |
|---|---|---|---|
| Paste height mean | 115.1 µm | 119.7 µm | recentered on target |
| Std. deviation | 7.70 µm | 4.91 µm | −36% spread |
| **Cp / Cpk** | 0.87 / **0.65** | 1.36 / **1.34** | Cpk **2.1× better** |
| Fraction defective (p) | 0.57 | 0.24 | −58% |
| **DPMO** | 4,560 | 1,362 | **−70%** |
| Process sigma | 4.11 σ | 4.50 σ | +0.39 σ |

Baseline Cpk of 0.65 means the process was **not capable**; the improvement pushes
Cpk past the conventional 1.33 "capable" threshold.

---

## The DMAIC story, tool by tool

| Phase | Artifact | What the data shows | Where it's built |
|---|---|---|---|
| **Define** | SIPOC / project charter | The process, CTQ, and spec window above | Power BI text page |
| **Measure** | Baseline DPMO & sigma | 4,560 DPMO ≈ 4.11σ; Cpk 0.65 | **SQL** |
| **Analyze** | **Pareto** of defects | *Insufficient solder* = 44%, +*Solder bridge* = 64%, +*Misalignment* = 75% → the **vital few** | **SQL** → Power BI |
| **Analyze** | Operator ANOVA / t-test | Operator has **no** significant effect — rules out the obvious suspect | Python (small) |
| **Analyze** | **X̄ / R control chart** | 12 out-of-control points, **all in week 3**, dipping to 98 µm → the special cause | **DAX** in Power BI |
| **Improve** | Before/after capability | Cpk 0.65 → 1.34 once the stencil SOP recenters the process | **DAX** |
| **Control** | Post-improvement chart + plan | Improved process runs in-control on target | **DAX** in Power BI |

The punchline that makes this a *causal* story rather than a coincidence: the same
stencil fix that recentered paste height also collapsed the **insufficient-solder**
defect — the control-chart excursion and the Pareto spike are the same root cause
seen two different ways.

The X̄ chart limits (subgroup n = 5, A₂ = 0.577): **X̿ = 115.11**, **R̄ = 16.68**,
**LCL = 105.48**, **UCL = 124.73**.

---

## Files

```
Lean-Sigma-Learners-Portfolio/
├── generate_data.py        # seeded generator — reproduces every CSV below
├── data/
│   ├── measurements.csv    # 3,200 rows — continuous CTQ in subgroups of 5
│   ├── inspections.csv     # 12,800 rows — one per inspected board
│   ├── defects.csv         #  7,580 rows — one per individual defect
│   ├── specs.csv           # spec limits + sampling constants
│   └── data_dictionary.md  # column-by-column reference
└── README.md
```

See `data/data_dictionary.md` for every column.

---

## Reproduce the data

```bash
pip install numpy pandas
python generate_data.py
```

The seed is fixed (`numpy.random.default_rng(42)`), so the regenerated CSVs are
byte-for-byte identical. Tune the constants at the top of `generate_data.py`
(weeks, subgroup size, spec limits, defect rates) to rescale the whole dataset.

---

## Roadmap

- [x] Reproducible dataset + generator
- [ ] SQL marts: DPMO / sigma level, Pareto, p-chart, X̄/R control limits
- [ ] Power BI report: one page per DMAIC phase
- [ ] Python notebook: operator ANOVA + capability histogram

---

## License

MIT — see [LICENSE](LICENSE).
