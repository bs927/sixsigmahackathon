import numpy as np
import pandas as pd
from scipy.stats import shapiro

# Constants for control charts based on subgroup size n (2 to 10)
# A2, D3, D4
CONTROL_CONSTANTS = {
    2: {"A2": 1.880, "D3": 0.0, "D4": 3.267, "d2": 1.128},
    3: {"A2": 1.023, "D3": 0.0, "D4": 2.574, "d2": 1.693},
    4: {"A2": 0.729, "D3": 0.0, "D4": 2.282, "d2": 2.059},
    5: {"A2": 0.577, "D3": 0.0, "D4": 2.114, "d2": 2.326},
    6: {"A2": 0.483, "D3": 0.0, "D4": 2.004, "d2": 2.534},
    7: {"A2": 0.419, "D3": 0.076, "D4": 1.924, "d2": 2.704},
    8: {"A2": 0.373, "D3": 0.136, "D4": 1.864, "d2": 2.847},
    9: {"A2": 0.337, "D3": 0.184, "D4": 1.816, "d2": 2.970},
    10: {"A2": 0.308, "D3": 0.223, "D4": 1.777, "d2": 3.078},
}

def compute_qc_analysis(df, value_col="Stress_Yield_MPa", subgroup_size=5, usl=950, lsl=850):
    """
    Computes all required QC statistics:
    - X-bar chart limits (using A2)
    - R chart limits (using D3, D4)
    - sigma-hat = R-bar / d2
    - Cp and Cpk
    - Normality (Shapiro-Wilk test)
    - Out-of-control flags for each subgroup
    """
    if df is None or len(df) == 0:
        raise ValueError("Dataset is empty.")
    
    if value_col not in df.columns:
        raise ValueError(f"Column '{value_col}' not found in dataset.")

    values = df[value_col].dropna().values
    n_total = len(values)

    if n_total < 2:
        raise ValueError("Dataset must have at least 2 observations to compute statistics.")

    # Check for degenerate case: zero variance / constant data
    if np.all(values == values[0]):
        raise ValueError("Degenerate case: data has zero variance (all values are identical). Capability and control limits are undefined.")

    # Form subgroups of size subgroup_size
    num_subgroups = n_total // subgroup_size
    if num_subgroups == 0:
        # If fewer than subgroup_size, treat as one subgroup or adjust
        subgroups = [values]
        num_subgroups = 1
        subgroup_size = n_total
    else:
        truncated_length = num_subgroups * subgroup_size
        subgroups = np.array_split(values[:truncated_length], num_subgroups)

    subgroup_means = []
    subgroup_ranges = []

    for sg in subgroups:
        if len(sg) == 0:
            continue
        subgroup_means.append(np.mean(sg))
        subgroup_ranges.append(np.max(sg) - np.min(sg))

    subgroup_means = np.array(subgroup_means)
    subgroup_ranges = np.array(subgroup_ranges)

    grand_mean = np.mean(subgroup_means)
    r_bar = np.mean(subgroup_ranges)

    # Get constants
    if subgroup_size in CONTROL_CONSTANTS:
        consts = CONTROL_CONSTANTS[subgroup_size]
    else:
        # Fallback approximation for n > 10
        d2 = np.sqrt(subgroup_size) # rough approximation if not standard
        consts = {
            "A2": 3.0 / (3 * np.sqrt(subgroup_size)),
            "D3": 0.0,
            "D4": 1.43 if subgroup_size <= 15 else 1.36,
            "d2": d2
        }

    A2 = consts["A2"]
    D3 = consts["D3"]
    D4 = consts["D4"]
    d2 = consts["d2"]

    # X-bar limits
    xbar_ucl = grand_mean + A2 * r_bar
    xbar_lcl = grand_mean - A2 * r_bar

    # R chart limits
    r_ucl = D4 * r_bar
    r_lcl = D3 * r_bar

    # sigma-hat = R-bar / d2
    if d2 == 0 or r_bar == 0:
        raise ValueError("Degenerate case: zero range across subgroups. Sigma-hat is zero, capability is undefined.")
    
    sigma_hat = r_bar / d2

    # Capability indices
    # Cp = (USL - LSL) / (6 * sigma_hat)
    # Cpk = min((USL - grand_mean) / (3 * sigma_hat), (grand_mean - LSL) / (3 * sigma_hat))
    cp = (usl - lsl) / (6 * sigma_hat)
    cpk_upper = (usl - grand_mean) / (3 * sigma_hat)
    cpk_lower = (grand_mean - lsl) / (3 * sigma_hat)
    cpk = min(cpk_upper, cpk_lower)

    # Normality test (Shapiro-Wilk)
    shapiro_stat, shapiro_p = shapiro(values)

    # Out of control flags per subgroup
    out_of_control_flags = []
    for i in range(len(subgroup_means)):
        mean_val = subgroup_means[i]
        range_val = subgroup_ranges[i]
        is_xbar_oc = (mean_val > xbar_ucl) or (mean_val < xbar_lcl)
        is_r_oc = (range_val > r_ucl) or (range_val < r_lcl)
        out_of_control_flags.append({
            "subgroup": i + 1,
            "mean": mean_val,
            "range": range_val,
            "out_of_control": bool(is_xbar_oc or is_r_oc)
        })

    return {
        "grand_mean": grand_mean,
        "r_bar": r_bar,
        "xbar_ucl": xbar_ucl,
        "xbar_lcl": xbar_lcl,
        "r_ucl": r_ucl,
        "r_lcl": r_lcl,
        "sigma_hat": sigma_hat,
        "cp": cp,
        "cpk": cpk,
        "shapiro_stat": shapiro_stat,
        "shapiro_p": shapiro_p,
        "out_of_control_flags": out_of_control_flags
    }
