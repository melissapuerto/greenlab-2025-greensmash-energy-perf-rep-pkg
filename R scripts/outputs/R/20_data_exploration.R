print("Starting data exploration script...")

source(here::here("R", "00_setup.R"))

dat <- read_csv(here::here("outputs", "tables", "01_cleaned.csv"), show_col_types = FALSE)

# Summary statistics per function × treatment
descriptive_stats <- dat |>
  group_by(func, treatment) |>
  summarise(
    n = n(),
    mean_time = mean(time_s),
    median_time = median(time_s),
    sd_time = sd(time_s),
    iqr_time = IQR(time_s),
    mean_energy = mean(energy_j),
    median_energy = median(energy_j),
    sd_energy = sd(energy_j),
    iqr_energy = IQR(energy_j),
    mean_cpu = mean(cpu_pct),
    mean_mem = mean(mem_mb),
    .groups = "drop"
  )

write_csv(descriptive_stats, here::here("outputs", "tables", "03_descriptive_stats.csv"))

# Load the ggplot2 library
library(ggplot2)

# ENERGY plot ----------------------------------------------------------
p_energy <- ggplot(dat, aes(x = treatment, y = energy_j, fill = treatment)) +
  geom_violin(trim = FALSE, alpha = 0.6, color = "gray30") +
  geom_boxplot(width = 0.1, alpha = 0.5, outlier.size = 0.8, color = "black") +
  facet_wrap(~ func, scales = "free_y") +
  scale_y_log10() +
  labs(
    title = "Energy Consumption by Treatment and Function",
    y = "Energy (J, log scale)",
    x = "Treatment"
  ) +
  scale_fill_manual(values = c("#F8766D", "#00BFC4"), name = "Treatment") +
  theme_minimal(base_size = 12) +
  theme(
    strip.text = element_text(face = "bold"),
    legend.position = "bottom",
    panel.grid.minor = element_blank()
  )

ggsave(
  here::here("outputs", "figures", "energy_violin_box_log.png"),
  p_energy,
  width = 12, height = 8, dpi = 300
)


# TIME plot ------------------------------------------------------------
p_time <- ggplot(dat, aes(x = treatment, y = time_s, fill = treatment)) +
  geom_violin(trim = FALSE, alpha = 0.6, color = "gray30") +
  geom_boxplot(width = 0.1, alpha = 0.5, outlier.size = 0.8, color = "black") +
  facet_wrap(~ func, scales = "free_y") +
  scale_y_log10() +
  labs(
    title = "Execution Time by Treatment and Function",
    y = "Time (s, log scale)",
    x = "Treatment"
  ) +
  scale_fill_manual(values = c("#F8766D", "#00BFC4"), name = "Treatment") +
  theme_minimal(base_size = 12) +
  theme(
    strip.text = element_text(face = "bold"),
    legend.position = "bottom",
    panel.grid.minor = element_blank()
  )

ggsave(
  here::here("outputs", "figures", "time_violin_box_log.png"),
  p_time,
  width = 12, height = 8, dpi = 300
)
