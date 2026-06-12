# Data dictionary

All data is synthetic, produced by `generate_data.py` (seed = 42). Three related
tables plus a small spec reference. They join as a simple star:

```
defects.board_id  ──►  inspections.board_id
measurements      ──►  (standalone; the continuous CTQ stream)
specs             ──►  (single-row reference for the CTQ spec window)
```

---

## measurements.csv  (continuous CTQ — drives capability & X̄/R charts)

| Column | Type | Description |
|---|---|---|
| `measurement_id` | int | Unique row id. |
| `timestamp` | datetime | Production hour the subgroup was taken. |
| `subgroup_id` | int | Rational subgroup key. Each subgroup = 5 boards measured in the same hour. Group by this for X̄/R charts. |
| `week` | int | 1–8. Weeks 1–4 baseline, 5–8 improved. |
| `phase` | text | `baseline` or `improved`. |
| `shift` | text | `A` (06:00–13:00) or `B` (14:00–21:00). No engineered effect. |
| `operator` | text | `OP-1/2/3`. **Deliberately no real effect** — the Analyze-phase red herring. |
| `paste_height_um` | float | The CTQ: solder paste deposit height in microns. Compare to specs (T=120, LSL=100, USL=140). |

## inspections.csv  (one row per board — drives p-chart, yield, DPMO denominator)

| Column | Type | Description |
|---|---|---|
| `board_id` | int | Unique board id (join key for `defects`). |
| `timestamp` | datetime | Hour the board was inspected. |
| `week` | int | 1–8. |
| `phase` | text | `baseline` / `improved`. |
| `shift` | text | `A` / `B`. |
| `operator` | text | `OP-1/2/3`. |
| `opportunities` | int | Solder joints per board (200). Sum this for the DPMO denominator. |
| `defect_count` | int | Total defects found on the board (0 = clean). |
| `disposition` | text | `PASS` (zero defects) or `FAIL` (≥1 defect). Note: FAIL means "has a defect," not "scrapped" — many are reworkable. Use for the p-chart fraction-defective. |

## defects.csv  (one row per defect — drives Pareto & DPMO numerator)

| Column | Type | Description |
|---|---|---|
| `defect_id` | int | Unique defect id. |
| `board_id` | int | Board the defect was found on (joins to `inspections`). |
| `timestamp` | datetime | Hour the defect was recorded. |
| `week` | int | 1–8. |
| `phase` | text | `baseline` / `improved`. |
| `defect_type` | text | One of 8 categories. *Insufficient solder* is the vital-few driver and spikes during the week-3 stencil clog. |

## specs.csv  (single-row reference)

| Column | Description |
|---|---|
| `ctq` | Name of the CTQ characteristic. |
| `target`, `lsl`, `usl` | Target and spec limits for paste height (µm). |
| `subgroup_size` | Rational subgroup size (5). |
| `opportunities_per_board` | Joints per board (200) for DPMO. |

---

### Quick formulas

- **DPMO** = (total defects ÷ (boards × opportunities_per_board)) × 1,000,000
- **Fraction defective (p)** = FAIL boards ÷ total boards
- **Cpk** = min(USL − x̄, x̄ − LSL) ÷ (3σ)
- **X̄/R limits** (n=5): UCL/LCL = X̿ ± A₂·R̄, with A₂ = 0.577
