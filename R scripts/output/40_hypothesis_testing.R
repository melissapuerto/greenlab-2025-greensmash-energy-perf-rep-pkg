# R/40_hypothesis_testing.R
source(here::here("R", "00_setup.R"))

library(dplyr)
library(readr)
library(rstatix)

# Load cleaned dataset
dat <- read_csv(here::here("outputs", "tables", "01_cleaned.csv"), show_col_types = FALSE)

# -------------------------------------------------------------------
# Run Wilcoxon Signed-Rank Test for energy consumption (paired)
# -------------------------------------------------------------------
wilcox_energy <- dat %>%
  group_by(func) %>%
  summarise(
    p_value = wilcox.test(
      energy_j[treatment == "baseline"],
      energy_j[treatment == "optimized"],
      paired = TRUE,
      exact = FALSE
    )$p.value,
    effect_size = wilcox_effsize(
      data.frame(
        value = energy_j,
        group = treatment
      ),
      value ~ group,
      paired = TRUE
    )$effsize
  )

# Apply Benjamini–Hochberg correction
wilcox_energy <- wilcox_energy %>%
  mutate(
    p_adj = p.adjust(p_value, method = "BH"),
    Significant = ifelse(p_adj < 0.05, "Yes", "No")
  )

# Save results
write_csv(wilcox_energy, here::here("outputs", "tables", "06_wilcoxon_energy_results.csv"))

print(wilcox_energy)
print("✅ Wilcoxon Signed-Rank tests for energy complete: results saved to outputs/tables/06_wilcoxon_energy_results.csv")
