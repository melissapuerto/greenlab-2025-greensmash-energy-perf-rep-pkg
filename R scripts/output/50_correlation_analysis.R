# R/50_correlation_analysis.R
source(here::here("R", "00_setup.R"))

library(dplyr)
library(readr)
library(ggplot2)
library(ggpubr)

# Load data
dat <- read_csv(here::here("outputs", "tables", "01_cleaned.csv"), show_col_types = FALSE)

# Focus only on the optimized treatment
optimized <- dat %>% filter(treatment == "optimized")

# -------------------------------------------------------------------
# Compute correlations per function
# -------------------------------------------------------------------
cor_results <- optimized %>%
  group_by(func) %>%
  summarise(
    rho_time = cor(energy_j, time_s, method = "spearman"),
    p_time = cor.test(energy_j, time_s, method = "spearman")$p.value,
    
    rho_cpu = cor(energy_j, cpu_pct, method = "spearman"),
    p_cpu = cor.test(energy_j, cpu_pct, method = "spearman")$p.value,
    
    rho_mem = cor(energy_j, mem_mb, method = "spearman"),
    p_mem = cor.test(energy_j, mem_mb, method = "spearman")$p.value
  )

# Adjust p-values (Benjamini–Hochberg correction)
cor_results <- cor_results %>%
  mutate(
    p_time_adj = p.adjust(p_time, method = "BH"),
    p_cpu_adj = p.adjust(p_cpu, method = "BH"),
    p_mem_adj = p.adjust(p_mem, method = "BH")
  )

# Save results
write_csv(cor_results, here::here("outputs", "tables", "07_correlation_results.csv"))

# -------------------------------------------------------------------
# Scatter plots with trend lines
# -------------------------------------------------------------------

# Energy vs Time
p_time <- ggplot(optimized, aes(x = time_s, y = energy_j, color = func)) +
  geom_point(alpha = 0.7) +
  geom_smooth(method = "lm", se = FALSE, color = "black") +
  labs(title = "Energy vs Execution Time (Optimized Functions)",
       x = "Execution Time (s)", y = "Energy Consumption (J)") +
  theme_minimal(base_size = 12) +
  theme(legend.position = "none")

# Energy vs CPU
p_cpu <- ggplot(optimized, aes(x = cpu_pct, y = energy_j, color = func)) +
  geom_point(alpha = 0.7) +
  geom_smooth(method = "lm", se = FALSE, color = "black") +
  labs(title = "Energy vs CPU Utilization (Optimized Functions)",
       x = "CPU Utilization (%)", y = "Energy Consumption (J)") +
  theme_minimal(base_size = 12) +
  theme(legend.position = "none")

# Energy vs Memory
p_mem <- ggplot(optimized, aes(x = mem_mb, y = energy_j, color = func)) +
  geom_point(alpha = 0.7) +
  geom_smooth(method = "lm", se = FALSE, color = "black") +
  labs(title = "Energy vs Memory Usage (Optimized Functions)",
       x = "Memory Usage (MB)", y = "Energy Consumption (J)") +
  theme_minimal(base_size = 12) +
  theme(legend.position = "none")

ggsave(here::here("outputs", "figures", "cor_energy_time.png"), p_time, width = 7, height = 5, dpi = 300)
ggsave(here::here("outputs", "figures", "cor_energy_cpu.png"), p_cpu, width = 7, height = 5, dpi = 300)
ggsave(here::here("outputs", "figures", "cor_energy_mem.png"), p_mem, width = 7, height = 5, dpi = 300)

print("✅ Correlation analysis complete: results and figures saved.")
