# CPR Aerospace QC — Quality Control & Process Capability Tool

**CPR Aerospace QC** is a production-grade monitoring and quality control web application and analysis engine designed for process engineers managing 3D printing lines for titanium aerospace brackets.

---

## What the Tool Does
The tool ingests high-frequency process telemetry logs (`process_logs.csv`) measuring **Temperature (°C)**, **Pressure (PSI)**, and **Stress Yield (MPa)**. It computes rigorous Statistical Process Control (SPC) limits, performs Process Capability Analysis ($C_p$ and $C_{pk}$), runs tests for normality, flags out-of-control subgroups, and returns actionable engineering recommendations (e.g., immediate machine calibration vs. process stable).

---

## For Whom
- **Primary User:** The process engineer monitoring the 3D printing line for titanium aerospace brackets.
- **Decision Supported:** Whether the current printing process is capable of meeting strict aerospace tolerances or requires an immediate machine calibration after each production run.

---

## Inputs and Parameters
- **Input File:** `process_logs.csv` (or any of the test datasets in `data/`).
- **Columns:**
  - `Temperature` (°C): Printer chamber temperature logs.
  - `Pressure` (PSI): Chamber pressure telemetry.
  - `Stress_Yield_MPa` (MPa): Measured yield stress per printed part.
- **Parameters:**
  - `subgroup_size`: Default = 5.
  - `usl`: Upper Specification Limit (Default = 950 MPa).
  - `lsl`: Lower Specification Limit (Default = 850 MPa).

---

## How Each Function or Endpoint Works

### 1. Core Statistical Engine (`app/qc.py`)
Implements plain, tested functions adhering strictly to the Six Sigma methodology:
- **X-bar Chart Limits:** Computes subgroup means and limits using factor $A_2$.
- **R Chart Limits:** Computes subgroup ranges and limits using factors $D_3$ and $D_4$.
- **$\hat{\sigma}$ (Sigma-hat):** Computed strictly via $\bar{R} / d_2$ (never overall sample standard deviation, ensuring accurate $C_p$ and $C_{pk}$ estimation).
- **Process Capability ($C_p, C_{pk}$):** Evaluates potential and actual process capability against specification limits.
- **Normality Test:** Executes the Shapiro-Wilk test on raw telemetry values.
- **Out-of-Control Flags:** Evaluates each subgroup against X-bar and R control boundaries.

### 2. FastAPI REST Endpoints (`app/main.py`)
- `GET /`: Serves the interactive React frontend dashboard.
- `POST /api/analyze`: Ingests uploaded CSV telemetry files or selects built-in test datasets, running the full statistical analysis and returning structured JSON results with actionable engineering recommendations.

---

## How to Run It in One Command
From the root of the repository, start the FastAPI application using the `testme` script:

```bash
bash app/testme.sh
```

Or on Windows PowerShell:
```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## Live URL
- **Posit Connect Deployment URL:** *Coming soon / deployed via H-06 workflow.*

---

## Walkthrough & Demo Datasets
Detailed walkthroughs of the tool across all test datasets (`capable.csv`, `incapable_drift.csv`, `incapable_high_variance.csv`) are documented in [demo/README.md](demo/README.md).
