# Data Codebook: Titanium 3D Printing Process Logs

This directory contains test datasets for the Process Capability and SPC tool (`CPR Aerospace QC`).

## Files

1. `capable.csv`
   - Description: Process logs from a stable, capable 3D printer run where all parts meet aerospace yield stress tolerances (850 - 950 MPa).
   - Columns:
     - `temperature`: Numeric, printer chamber temperature in degrees Celsius (deg C). Collected via embedded thermocouple sensors.
     - `pressure`: Numeric, chamber argon gas pressure in PSI. Collected via inline pressure transducers.
     - `stress_yield`: Numeric, measured yield stress of the printed titanium bracket in megapascals (MPa). Collected via post-print tensile destructive and non-destructive testing logs.

2. `incapable_drift.csv`
   - Description: Process logs showing a gradual mean drift in temperature, pressure, and yield stress, causing the process to exceed the upper specification limit (USL).
   - Columns: Same as above (`temperature` deg C, `pressure` PSI, `stress_yield` MPa).

3. `incapable_high_variance.csv`
   - Description: Process logs showing high volatility and process spread (high standard deviation), resulting in failures at both lower and upper specification limits (LSL and USL).
   - Columns: Same as above (`temperature` deg C, `pressure` PSI, `stress_yield` MPa).

## Data Collection
Real data is collected automatically from the 3D printer's supervisory control and data acquisition (SCADA) system logs combined with mechanical testing lab reports after each production batch.
