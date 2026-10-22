# Implementation Plan: Titanium 3D Printing Process Capability Tool

## Core Formulas
- Mean: $\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$
- Standard Deviation: $s = \sqrt{\frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2}$
- Process Capability ($C_p$): $C_p = \frac{\text{USL} - \text{LSL}}{6s}$
- Centered Capability ($C_{pk}$): $C_{pk} = \min\left(\frac{\text{USL}-\bar{x}}{3s}, \frac{\bar{x}-\text{LSL}}{3s}\right)$
- Normality Test Statistic (Shapiro-Wilk $W$): $W = \frac{\left(\sum a_i x_{(i)}\right)^2}{\sum (x_i - \bar{x})^2}$

## Tasks
1. **H-01: Fill SPEC.md**
   - Owns: `SPEC.md`
   - Test: `grep -c "FILL IN" SPEC.md` returns 0.
   - Estimate: 15 mins.

2. **H-03: Core Statistics Engine**
   - Owns: `app/qc.py`, `app/requirements.txt`, `tests/`
   - Test: `pytest` passes textbook case ($\bar{x}=900, s=10, \text{USL}=950, \text{LSL}=850 \implies C_{pk}=1.67$) AND degenerate case ($s=0$ constant data raises `ValueError`).
   - Estimate: 45 mins.

3. **H-02: Test Datasets & Codebook**
   - Owns: `data/`
   - Test: `data/capable.csv`, `incapable_drift.csv`, `incapable_high_variance.csv` exist and `data/README.md` details all columns.
   - Estimate: 30 mins.

4. **H-04: API Tool Wrapper**
   - Owns: `app/`
   - Test: `testme` runs FastAPI server; POST `/analyze` returns $C_{pk}=1.67$ for test parameters.
   - Estimate: 45 mins.

5. **H-05: Frontend Capability Dashboard & Demo**
   - Owns: `demo/`, `app/frontend/`
   - Test: `demo/README.md` describes outputs; dashboard displays $C_{pk}$ badge and status.
   - Estimate: 45 mins.

6. **H-06: Posit Connect Deployment**
   - Owns: `.github/workflows/`, `.github/scripts/`, `app/manifest.json`, `app/.python-version`
   - Test: GitHub Action green; public URL returns 200 and matches $C_{pk}$ test result.
   - Estimate: 30 mins.

7. **H-07: Documentation & User Guide**
   - Owns: `README.md`, `app/README.md`
   - Test: Clean clone runs `testme` and pytest passes.
   - Estimate: 30 mins.

8. **H-08: Public Repo & Submission**
   - Owns: `.gitignore`
   - Test: Repo is public; clean clone passes; Devpost URL active.
   - Estimate: 15 mins.

## Decisions
1. **Handling missing values in process logs:** 1. Drop rows with missing values (Recommended: keeps calculations robust and avoids distorting $C_{pk}$ with imputed artifacts); 2. Impute missing values with column mean; 3. Raise an error and abort analysis.
2. **Normality violation fallback behavior:** 1. Warn the user via API response but still return capability metrics (Recommended: process engineers often need numerical capability metrics even if distributions deviate slightly); 2. Abort analysis and return error; 3. Automatically apply a Box-Cox transformation.
3. **Spec limit configuration source:** 1. Allow dynamic USL/LSL query parameters in the API request (Recommended: provides maximum flexibility for engineers testing different tolerances); 2. Hardcode spec limits based on dataset defaults; 3. Read spec limits from a config file in `app/`.
4. **Primary statistical metric for Pass/Fail status:** 1. $C_{pk}$ (Recommended: accounts for process centering as required for critical aerospace titanium parts); 2. $C_p$ (ignores centering); 3. Both $C_p$ and $C_{pk}$ equally weighted.

## Top 3 Risks & Mitigation
1. **Wrong formula:** Test math in isolation against textbook numbers before writing UI.
2. **Deployment failure:** Deploy early on Day 1 using `manifestme` to catch server issues.
3. **Data non-normality:** Use Shapiro-Wilk test to warn user if capability assumption fails.
