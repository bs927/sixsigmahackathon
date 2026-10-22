# Demonstration Walkthrough: CPR Aerospace QC

This guide demonstrates how to use the CPR Aerospace QC tool on each of the test datasets in `data/`.

## 1. Prerequisites
Ensure Python and dependencies are installed:
```bash
python -m pip install -r app/requirements.txt
```

## 2. Running Tests
To run the H-03 process capability and SPC unit tests:
```bash
python -m pytest tests/
```

## 3. Demonstration on Test Datasets

You can analyze each test dataset using the Python CLI script or by querying the FastAPI app.

### Dataset A: `capable.csv`
- **File:** `data/capable.csv`
- **Description:** Stable process logs where all titanium brackets meet tolerances (LSL = 850, USL = 950).
- **Command / How to run:**
  ```bash
  python -c "import sys; sys.path.insert(0, 'app'); import pandas as pd, json; from qc import compute_qc_analysis; df = pd.read_csv('data/capable.csv', comment='#'); print(json.dumps(compute_qc_analysis(df, 'stress_yield', 950, 850), indent=2))"
  ```
- **How to read this:** `cpk` indicates process capability. `out_of_control_flags` will show whether any subgroup points exceed control limits.

### Dataset B: `incapable_drift.csv`
- **File:** `data/incapable_drift.csv`
- **Description:** Process logs with an upward drift causing violation of the Upper Specification Limit (USL).
- **Command / How to run:**
  ```bash
  python -c "import sys; sys.path.insert(0, 'app'); import pandas as pd, json; from qc import compute_qc_analysis; df = pd.read_csv('data/incapable_drift.csv', comment='#'); print(json.dumps(compute_qc_analysis(df, 'stress_yield', 950, 850), indent=2))"
  ```
- **How to read this:** `cpk` will be low due to the mean exceeding USL, and out-of-control flags will be triggered.

### Dataset C: `incapable_high_variance.csv`
- **File:** `data/incapable_high_variance.csv`
- **Description:** Process logs with excessive spread (high variance), violating specification limits.
- **Command / How to run:**
  ```bash
  python -c "import sys; sys.path.insert(0, 'app'); import pandas as pd, json; from qc import compute_qc_analysis; df = pd.read_csv('data/incapable_high_variance.csv', comment='#'); print(json.dumps(compute_qc_analysis(df, 'stress_yield', 950, 850), indent=2))"
  ```
- **How to read this:** A high `sigma_hat` widens the process spread beyond specification limits, resulting in poor process capability metrics.
