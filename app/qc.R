# Constants for control charts based on subgroup size n (2 to 10)
control_constants <- list(
  "2" = list(A2 = 1.880, D3 = 0.0, D4 = 3.267, d2 = 1.128),
  "3" = list(A2 = 1.023, D3 = 0.0, D4 = 2.574, d2 = 1.693),
  "4" = list(A2 = 0.729, D3 = 0.0, D4 = 2.282, d2 = 2.059),
  "5" = list(A2 = 0.577, D3 = 0.0, D4 = 2.114, d2 = 2.326),
  "6" = list(A2 = 0.483, D3 = 0.0, D4 = 2.004, d2 = 2.534),
  "7" = list(A2 = 0.419, D3 = 0.076, D4 = 1.924, d2 = 2.704),
  "8" = list(A2 = 0.373, D3 = 0.136, D4 = 1.864, d2 = 2.847),
  "9" = list(A2 = 0.337, D3 = 0.184, D4 = 1.816, d2 = 2.970),
  "10" = list(A2 = 0.308, D3 = 0.223, D4 = 1.777, d2 = 3.078)
)

compute_qc_analysis <- function(df, value_col = "Stress_Yield_MPa", subgroup_size = 5, usl = 950, lsl = 850) {
  values <- na.omit(df[[value_col]])
  n_total <- length(values)
  
  if (n_total < 2) stop("Dataset must have at least 2 observations.")
  if (var(values) == 0) stop("Degenerate case: data has zero variance.")
  
  num_subgroups <- floor(n_total / subgroup_size)
  if (num_subgroups == 0) {
    subgroups <- list(values)
    num_subgroups <- 1
    subgroup_size <- n_total
  } else {
    truncated_values <- values[1:(num_subgroups * subgroup_size)]
    subgroups <- split(truncated_values, rep(1:num_subgroups, each = subgroup_size))
  }
  
  subgroup_means <- sapply(subgroups, mean)
  subgroup_ranges <- sapply(subgroups, function(x) max(x) - min(x))
  
  grand_mean <- mean(subgroup_means)
  r_bar <- mean(subgroup_ranges)
  
  # Constants
  ss_char <- as.character(subgroup_size)
  if (ss_char %in% names(control_constants)) {
    consts <- control_constants[[ss_char]]
  } else {
    d2 <- sqrt(subgroup_size)
    consts <- list(A2 = 3.0 / (3 * sqrt(subgroup_size)), D3 = 0.0, D4 = 1.43, d2 = d2)
  }
  
  # Limits
  xbar_ucl <- grand_mean + consts$A2 * r_bar
  xbar_lcl <- grand_mean - consts$A2 * r_bar
  
  r_ucl <- consts$D4 * r_bar
  r_lcl <- consts$D3 * r_bar
  
  sigma_hat <- r_bar / consts$d2
  if (sigma_hat == 0) stop("Degenerate case: zero range.")
  
  cp <- (usl - lsl) / (6 * sigma_hat)
  cpk <- min((usl - grand_mean) / (3 * sigma_hat), (grand_mean - lsl) / (3 * sigma_hat))
  
  # Normality
  shapiro_res <- shapiro.test(values)
  
  # Flags
  flags <- data.frame(
    subgroup = 1:num_subgroups,
    mean = subgroup_means,
    range = subgroup_ranges,
    out_of_control = (subgroup_means > xbar_ucl | subgroup_means < xbar_lcl | subgroup_ranges > r_ucl | subgroup_ranges < r_lcl)
  )
  
  list(
    grand_mean = grand_mean,
    xbar_ucl = xbar_ucl,
    xbar_lcl = xbar_lcl,
    r_bar = r_bar,
    r_ucl = r_ucl,
    r_lcl = r_lcl,
    sigma_hat = sigma_hat,
    cp = cp,
    cpk = cpk,
    shapiro_stat = shapiro_res$statistic,
    shapiro_p = shapiro_res$p.value,
    out_of_control_flags = flags
  )
}
