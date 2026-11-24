# Page 05 Implementation Report

## Project

- Project location: `D:\A UEH_UNIVERSITY\MONEY\Portfilio\marnufacturing_digitalization\Lean-Sigma-Learners-Portfolio\SMT_quality_dashboard_CODEX`
- Power BI report: `SMT_Quality_Dashboard_CODEX.Report`
- Page 05 identifier: `927b003107e1f538711f`
- Page name: `5. Improvement Assessment`

## Changes made

- Added the Page 05 native visual definitions and increased its canvas height to 1520.
- Implemented four KPI cards: yield improvement, defective-rate reduction, DPMO reduction, and overall-standard-deviation reduction.
- Implemented before/after yield and defective-rate column charts; weekly defective-rate and aligned weekly-DPMO line charts; capability and SPC matrices; and static Control Plan / Key Findings content.
- Added model measures in `DimDate`: `Unique Xbar-R Alerted Subgroups`, `Yield Improvement (pp)`, `Defective Rate Reduction (pp)`, `DPMO Reduction`, `Overall Std Reduction (um)`, and `Weekly DPMO (Aligned)`.
- Reused: `Yield %`, `Defective Rate %`, `DPMO`, `Mean Height`, `Overall Std`, `Cp`, `Cpk`, `Pp`, `Ppk`, `Total SPC Subgroups`, `Xbar Violations`, `R Violations`, and `p Violations`.

## SPC methodology

`Unique Xbar-R Alerted Subgroups` iterates `VALUES(SPC_XbarR[subgroup_id])` and evaluates `[XbarR Alarm]`, so an Xbar and R signal in the same subgroup is counted once. It deliberately does not apply `COALESCE`, preserving blank/error-like unavailable alarm outcomes instead of presenting them as zero.

The existing control limits calculate trial limits independently by phase. Therefore the Page 05 note explicitly limits interpretation to descriptive within-phase results; it does not claim that differing signal counts prove a fixed-reference stability improvement.

## Validation

- Executed: `powerbi-report-author --help`
- Executed: `powerbi-report-author preview-pages .\SMT_Quality_Dashboard_CODEX.Report --pretty`
- Executed: `powerbi-report-author preview-visuals .\SMT_Quality_Dashboard_CODEX.Report --pretty`
- Executed twice: `powerbi-report-author validate .\SMT_Quality_Dashboard_CODEX.Report --pretty`
- Page 05 JSON parse errors were resolved before the final validation.
- Final validator result remains failed because of existing project-wide issues outside Page 05: missing `$schema` entries in the original `.pbip` and `definition.pbir`, and Page 04 scatter-chart Category-role overflow. A schema-retrieval warning also occurred.

## Limitations

- No valid Desktop host or render screenshot has yet been confirmed; screenshot validation is pending the Desktop preview bridge.
- DAX execution against an imported live model was not available in this local TMDL session, so calculated KPI outputs were not claimed.
- Pages 01–04 were preserved; the listed Page 04 validator error was intentionally left untouched.

## File-change summary

Modified:

- `SMT_Quality_Dashboard_CODEX.SemanticModel/definition/tables/DimDate.tmdl`
- `SMT_Quality_Dashboard_CODEX.Report/definition/pages/927b003107e1f538711f/page.json`

Created:

- Twelve visual definitions under `SMT_Quality_Dashboard_CODEX.Report/definition/pages/927b003107e1f538711f/visuals/`
- `PAGE05_IMPLEMENTATION_REPORT.md`

No source CSV file was modified. A pre-change tar snapshot was created under `_backups`.
