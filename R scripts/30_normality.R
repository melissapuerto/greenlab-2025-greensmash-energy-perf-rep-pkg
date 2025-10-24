# R/30_normality.R
source(here::here("R", "00_setup.R"))

library(ggplot2)
library(ggpubr)
library(dplyr)
library(readr)

# Load cleaned dataset
dat <- read_csv(here::here("outputs", "tables", "01_cleaned.csv"), show_col_types = FALSE)

# Define a helper function for normality testing 
check_normality <- function(data, variable, var_label) {
  results <- data %>%
    group_by(treatment) %>%
    summarise(
      W = shapiro.test(.data[[variable]])$statistic,
      p_value = shapiro.test(.data[[variable]])$p.value,
      Normal = ifelse(p_value > 0.05, "Yes", "No"),
      .groups = "drop"
    ) %>%
    mutate(Metric = var_label)
  return(results)
}

# Run Shapiro–Wilk tests for Energy and Time ------------------------------------
normality_energy <- check_normality(dat, "energy_j", "Energy (J)")
normality_time   <- check_normality(dat, "time_s", "Execution Time (s)")

normality_results <- bind_rows(normality_energy, normality_time)
write_csv(normality_results, here::here("outputs", "tables", "05_normality_results.csv"))

print("✅ Shapiro–Wilk test results saved to outputs/tables/05_normality_results.csv")
print(normality_results)

# Histograms --------------------------------------------------------------------
p_energy_hist <- ggplot(dat, aes(x = energy_j, fill = treatment)) +
  geom_histogram(bins = 15, color = "black", alpha = 0.7, position = "identity") +
  facet_wrap(~ treatment, scales = "free_y") +
  labs(title = "Energy Distribution per Treatment", x = "Energy (J)", y = "Frequency") +
  theme_minimal() +
  scale_fill_manual(values = c("#E76F51", "#2A9D8F"))

p_time_hist <- ggplot(dat, aes(x = time_s, fill = treatment)) +
  geom_histogram(bins = 15, color = "black", alpha = 0.7, position = "identity") +
  facet_wrap(~ treatment, scales = "free_y") +
  labs(title = "Execution Time Distribution per Treatment", x = "Time (s)", y = "Frequency") +
  theme_minimal() +
  scale_fill_manual(values = c("#E76F51", "#2A9D8F"))

ggsave(here::here("outputs", "figures", "hist_energy_treatment.png"), p_energy_hist, width = 8, height = 5, dpi = 300)
ggsave(here::here("outputs", "figures", "hist_time_treatment.png"), p_time_hist, width = 8, height = 5, dpi = 300)

# Q–Q Plots ---------------------------------------------------------------------
p_energy_qq <- ggqqplot(dat, x = "energy_j", facet.by = "treatment",
                        title = "Q–Q Plot: Energy Distributions by Treatment")

p_time_qq <- ggqqplot(dat, x = "time_s", facet.by = "treatment",
                      title = "Q–Q Plot: Execution Time Distributions by Treatment")

ggsave(here::here("outputs", "figures", "qq_energy_treatment.png"), p_energy_qq, width = 8, height = 5, dpi = 300)
ggsave(here::here("outputs", "figures", "qq_time_treatment.png"), p_time_qq, width = 8, height = 5, dpi = 300)

print("✅ Normality plots created for each treatment group.")
