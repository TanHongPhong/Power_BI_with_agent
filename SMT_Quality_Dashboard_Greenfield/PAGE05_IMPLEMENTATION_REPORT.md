# Page 05 Implementation Report

## Project

- Project location: `D:\A UEH_UNIVERSITY\MONEY\Portfilio\marnufacturing_digitalization\Lean-Sigma-Learners-Portfolio\SMT_Quality_Dashboard_Greenfield`
- Power BI report: `SMT_Quality_Dashboard_Greenfield.Report`
- Page 05 identifier: `55555555555555555555` — **5. Improvement & Control Plan**

## Files created or modified

- New independent PBIP project: `SMT_Quality_Dashboard_Greenfield.pbip`, report definition, and semantic model definition.
- Report page definitions for five pages: Overview, SPC Control Center, Process Capability, Defect Analysis, and Improvement Assessment & Control Plan.
- Semantic-model TMDL files for Measurements, Inspections, Defects, Specifications, SPC XbarR, and SPC p Hourly.
- This report. No source CSV was modified. The pre-existing project `SMT_quality_dashboard_CODEX` was not read or copied into this project.

## Measures

New/reused model measures include: `Total Boards`, `Yield %`, `Defective Rate %`, `Total Defects`, `DPMO`, `Mean Paste Height`, `Overall Std`, `Cp`, `Cpk`, `Pp`, `Ppk`, `Total SPC Subgroups`, `Xbar Violations`, `R Violations`, `Unique Xbar-R Alerted Subgroups`, `p Violations`, `p Violations by Phase`, `Baseline Yield %`, `Improved Yield %`, `Yield Improvement (pp)`, `Baseline DPMO`, `Improved DPMO`, `DPMO Reduction`, and `DPMO by Phase`.

`Unique Xbar-R Alerted Subgroups` iterates the real `SPC XbarR[subgroup_id]` grain and uses the combined alarm measure, so a subgroup with both Xbar and R signals is counted once. Baseline and Improved measures explicitly fix the scopes to Weeks 1–4 and Weeks 5–8 and remove external week filters.

## Visuals implemented

- Overview: KPI card and weekly yield/defective-rate trend.
- SPC: Xbar, R, p control charts; phase stability matrix; Xbar-versus-range scatter.
- Capability: phase comparison, Cp/Cpk/Pp/Ppk card, capability matrix, histogram.
- Defects: defect-type column chart, weekly defect trend, Pareto combo chart, process scatter.
- Page 05: fixed phase KPI card, yield/DPMO comparison, defective-rate comparison, process-capability matrix, SPC stability matrix, proposed Control Plan content, and Key Findings note.
- Page 06: dedicated native X-bar control chart (subgroup timestamp, Xbar, CL, UCL, LCL) with the established trial-limit methodological note.
- Slicers: compact Phase, Week, and Shift dropdowns on the overview/capability pages; Phase and Week on the SPC, defect, and X-bar pages. Page 05 intentionally has no slicer so its fixed Before/After comparison is preserved.

## Style update

The report uses the original bright Fluent base theme. No GIF or animated asset was introduced.

## Validation executed

1. `powerbi-report-author validate <report-directory>`
2. Semantic model loaded from TMDL; four new DPMO measures created and retrieved successfully.
3. Model exported to the TMDL folder.
4. Parsed all 36 PBIR JSON files successfully; `pages.json` contains exactly five ordered pages.
5. DAX-query validation was attempted, but the installed model tool does not execute DAX against offline TMDL connections.

## Results and limitations

- Compatibility correction (2026-11-24): `definition.pbism` now uses the documented `definitionProperties/1.0.0` schema while retaining semantic-model format `version: 4.0` required for the TMDL `definition/` folder. This replaces the incompatible schema `2.0.0`.
- Model-load correction (2026-11-24): renamed specification measures that conflicted with source columns: `LSL` to `LSL Target`, `USL` to `USL Target`, and `Target` to `Specification Target`; capability measures now use the renamed measures.
- Slicer correction (2026-11-24): added conformed `Phase`, `Week`, and `Shift` dimensions and eight one-direction relationships to the base fact tables. Fixed-scope Page 05 measures explicitly remove those dimension filters before applying their baseline/improved week conditions.
- PBIR validation completed with **0 errors** and warnings. The remaining warnings are schema fetch unavailability and four empty legacy page-directory stubs which are not in `pageOrder`; the report itself contains five pages in `pageOrder`.
- The Desktop host executable could not be found by the authoring CLI; live Desktop reload, render, screenshot, and calculated KPI query could not be completed here. No screenshot has been fabricated.
- The dataset is synthetic. The page explicitly warns that phase-specific trial limits are descriptive within-phase limits, not fixed-reference operational limits; fewer alerts must not be treated as proof of better stability across phases.
- Stencil-cleaning execution, approvals, maintenance, and operator-accountability data do not exist in the source. The Control Plan labels all actions as proposed.

## Before / after change summary

The deliverable is a new greenfield PBIP folder. Pages 01–04 of the original project are untouched because this report does not alter or reference the original PBIP.
