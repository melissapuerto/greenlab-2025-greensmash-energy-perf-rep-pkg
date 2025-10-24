
library(tidyverse)
library(readr)
library(janitor)
library(here)
library(ggplot2)
library(bestNormalize)
library(ARTool)
library(lmerTest)
library(xtable)
library(ggpubr)

set.seed(42)

# output folders
dir.create(here("outputs","tables"), showWarnings = FALSE, recursive = TRUE)
dir.create(here("outputs","figures"), showWarnings = FALSE, recursive = TRUE)
