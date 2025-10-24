# R/10_load_clean.R
source(here::here("R","00_setup.R"))

# Load raw data
raw <- read_csv(here::here("data","run_table1.csv"), show_col_types = FALSE) |>
  janitor::clean_names()

# Split script_name into treatment and func
dat <- raw |>
  separate(script_name, into = c("treatment", "func"), sep = "_", extra = "merge", remove = FALSE) |>
  mutate(
    treatment = factor(treatment, levels = c("baseline","optimized")),
    func = as.factor(func),
    time_s = wall_seconds,
    energy_j = energy_joules,
    cpu_pct = avg_cpu_util_percent,
    mem_mb = peak_memory_mb
  ) |>
  select(run_id, treatment, func, rep,
         time_s, energy_j, cpu_pct, mem_mb)

# Quick summary to confirm structure
summary(dat)

# Save cleaned dataset
write_csv(dat, here::here("outputs","tables","01_cleaned.csv"))
