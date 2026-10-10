################################################################################
# REPLICATION CODE: India Political Economy Assessment 2014-2026
# Author: Dr. Varna Sri Raman
# Date: May 2026
# Description: Complete replication code for all analyses and indices
################################################################################

# Load required libraries
library(tidyverse)
library(readr)
library(ggplot2)
library(scales)
library(lubridate)

# Set working directory (adjust path as needed)
# setwd("path/to/your/data")

################################################################################
# SECTION 1: DATA LOADING AND PREPARATION
################################################################################

# Load the master dataset
data <- read_csv("data/SP_masterdataset.csv")

# View structure
str(data)
summary(data)

################################################################################
# SECTION 2: KEY ECONOMIC INDICATORS
################################################################################

# Calculate for two periods
# Employment elasticity is NOT computed here: the master dataset holds no sourced
# series (its Employment_Elasticity column is empty). These are ORF's published
# estimates (Ghosh and Roy Bardhan, ORF Expert Speak, 2 October 2024):
# 0.01 for 2011-16 and 1.11 for 2017-23.
orf_elasticity <- c("2011-2016" = 0.01, "2017-2023" = 1.11)

################################################################################
# SECTION 3: THREE NOVEL INDICES
################################################################################

# The three indices are defined canonically (for both eras, 2004-2026) in
# data/compute_indices.py. This R port reproduces that exact logic. Keep the two
# in sync; the Python file is the single source of truth.

# Component inputs (2004-2026) ------------------------------------------------
idx_years <- 2004:2026

# SSI: weighted sum of GRADED severities (0..1) with persistence; 6 streams.
# UPA years have none -> 0. Weights sum to 10.
ssi_weights <- c(census = 2.5, consumption = 1.5, employment = 1.0,
                 gdp = 1.5, institutional = 1.5, mortality = 2.0)
# severity matrix rows = streams (order of ssi_weights), cols = 2004..2026
ssi_sev <- matrix(0, nrow = 6, ncol = length(idx_years),
                  dimnames = list(names(ssi_weights), idx_years))
yr <- function(y) which(idx_years == y)
ssi_sev["census", as.character(2020:2025)] <- 1.0
ssi_sev["census", "2026"] <- 0.3   # scheduled delay: houselisting Apr-Sep 2026, enumeration Feb 2027 (MHA)
ssi_sev["consumption", as.character(2018:2023)] <- 1.0
ssi_sev["consumption", c("2024","2025","2026")] <- c(0.5, 0.3, 0.2)   # scar
ssi_sev["employment", c("2017","2018","2019")] <- c(1.0, 1.0, 0.3)
ssi_sev["gdp", c("2015","2016","2017")] <- 0.7
ssi_sev["gdp", as.character(2018:2026)] <- 1.0
ssi_sev["institutional", as.character(2019:2026)] <- 1.0
ssi_sev["mortality", c("2021","2022","2023","2024","2025","2026")] <- c(1.0,1.0,0.6,0.4,0.3,0.3)
calculate_ssi <- function(year) {
  round(sum(ssi_weights * ssi_sev[, as.character(year)]), 2)
}

# FCI: mean of the components published for each year. C1-C4 are published fiscal
# ratios, min-max normalised over the years each is published (NA = not published);
# C5 (borrowing) and C6 (GST) are coded. Rebuilt from published figures 2026-10-10.
# columns: cess_share, devolution, states_own_rev, non_fc_grants, borrowing, gst
fci_comp <- matrix(c(
  NA,25.8,62.9,32.8,0.0,0.0,
  NA,25.7,60.4,30.2,0.0,0.0,
  NA,25.4,59.5,30.7,0.0,0.0,
  NA,25.5,58.3,31.6,0.0,0.0,
  NA,26.6,58.1,35.3,0.0,0.0,
  NA,26.4,58.9,38.4,0.0,0.0,
  NA,27.7,59.1,34.5,0.0,0.0,
  10.4,28.8,59.8,32.2,0.0,0.0,
  11.7,28.1,61.6,29.9,0.0,0.0,
  12.4,27.9,61.7,29.0,0.0,0.0,
  13.5,27.1,58.0,40.0,0.0,0.0,
  12.2,34.8,54.6,29.0,0.0,0.0,
  13.5,35.4,52.9,27.0,0.0,0.0,
  13.9,31.5,56.4,31.0,0.0,0.6,
  19.9,35.9,54.7,29.2,0.0,0.7,
  17.5,32.4,55.6,34.7,0.0,0.8,
  24.4,29.4,52.1,37.1,1.0,0.85,
  21.8,32.6,53.3,27.6,0.5,0.9,
  20.4,31.1,55.9,30.3,0.0,1.0,
  18.6,32.6,57.8,31.6,0.0,1.0,
  18.0,33.9,56.9,31.4,0.0,1.0,
  16.4,34.2,58.2,32.6,0.0,1.0,
  14.3,34.7,NA,NA,0.0,1.0),
  ncol = 6, byrow = TRUE)
mm <- function(x) { r <- max(x, na.rm = TRUE) - min(x, na.rm = TRUE)
  if (r == 0) ifelse(is.na(x), NA, 0) else (x - min(x, na.rm = TRUE)) / r }
fci_series <- {
  c1 <- mm(fci_comp[,1]); c2 <- 1 - mm(fci_comp[,2]); c3 <- 1 - mm(fci_comp[,3])
  c4 <- mm(fci_comp[,4]); c5 <- fci_comp[,5]; c6 <- mm(fci_comp[,6])
  round(rowMeans(cbind(c1, c2, c3, c4, c5, c6), na.rm = TRUE), 2)
}
names(fci_series) <- idx_years

# DQI: geometric mean of V-Dem LDI, FreedomHouse/100, (180-RSF)/180, V-Dem Civil Society
# columns: vdem_ldi, freedom_house, rsf_rank, civil_society
dqi_comp <- matrix(c(
  0.578,76,120,0.826,
  0.573,76,106,0.76,
  0.569,76,105,0.76,
  0.569,76,120,0.76,
  0.569,76,118,0.76,
  0.539,76,105,0.76,
  0.532,76,122,0.744,
  0.532,77,131,0.744,
  0.525,76,131,0.743,
  0.522,77,140,0.735,
  0.488,78,140,0.669,
  0.417,77,136,0.576,
  0.406,77,133,0.555,
  0.371,77,136,0.523,
  0.363,75,138,0.471,
  0.324,71,140,0.454,
  0.292,67,142,0.404,
  0.307,66,142,0.421,
  0.291,66,150,0.421,
  0.273,66,161,0.346,
  0.281,63,159,0.302,
  0.26,62,151,0.302,
  0.26,62,157,0.302),
  ncol = 4, byrow = TRUE)
calculate_dqi <- function(year) {
  i <- which(idx_years == year)
  v <- dqi_comp[i,1]; f <- dqi_comp[i,2] / 100; r <- (180 - dqi_comp[i,3]) / 180; csi <- dqi_comp[i,4]
  round((v * f * r * csi)^(1/4), 2)
}

# Calculate all indices for each year
data$ssi <- sapply(data$year, calculate_ssi)
data$fci <- sapply(data$year, function(y) ifelse(as.character(y) %in% names(fci_series), fci_series[[as.character(y)]], NA))
data$dqi <- sapply(data$year, function(y) ifelse(y %in% idx_years, calculate_dqi(y), NA))

################################################################################
# SECTION 4: INEQUALITY ANALYSIS
################################################################################

# Gini coefficient calculation
calculate_gini <- function(income_shares) {
  n <- length(income_shares)
  sorted_shares <- sort(income_shares)
  cumsum_shares <- cumsum(sorted_shares)
  
  gini <- 1 - (2 / (n * sum(sorted_shares))) * sum((n - seq(1, n) + 1) * sorted_shares)
  return(gini)
}

# Top 1% income share trend analysis
inequality_model <- lm(top1_percent ~ year, data = data)
summary(inequality_model)

# Predict 2025 value
predict_2025 <- predict(inequality_model, newdata = data.frame(year = 2025))
print(paste("Predicted top 1% share in 2025:", round(predict_2025, 1), "%"))

################################################################################
# SECTION 5: VISUALIZATIONS
################################################################################

# Theme for all plots
theme_india <- theme_minimal() +
  theme(
    plot.title = element_text(size = 14, face = "bold"),
    axis.title = element_text(size = 11),
    legend.position = "bottom",
    panel.grid.minor = element_blank()
  )

# 1. Key Economic Indicators
p1 <- data %>%
  select(year, gdp_growth, unemployment, top1_percent) %>%
  pivot_longer(-year, names_to = "indicator", values_to = "value") %>%
  mutate(indicator = factor(indicator, 
                           levels = c("gdp_growth", "unemployment", "top1_percent"),
                           labels = c("GDP Growth (%)", "Unemployment (%)", "Top 1% Share (%)"))) %>%
  ggplot(aes(x = year, y = value, color = indicator)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +
  scale_color_manual(values = c("#10b981", "#ef4444", "#f97316")) +
  labs(title = "Key Economic Indicators (2014-2025)",
       x = "Year", y = "Value (%)", color = "Indicator") +
  theme_india

ggsave("key_indicators.png", p1, width = 10, height = 6, dpi = 300)

# 2. Three Indices
p2 <- data %>%
  select(year, ssi, fci, dqi) %>%
  pivot_longer(-year, names_to = "index", values_to = "value") %>%
  mutate(index = factor(index,
                        levels = c("ssi", "fci", "dqi"),
                        labels = c("Statistical Suppression", "Fiscal Centralization", 
                                 "Democratic Quality"))) %>%
  ggplot(aes(x = year, y = value, color = index)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +
  facet_wrap(~index, scales = "free_y") +
  scale_color_manual(values = c("#dc2626", "#f59e0b", "#3b82f6")) +
  labs(title = "Three Indices of Institutional Change",
       x = "Year", y = "Index Value") +
  theme_india +
  theme(legend.position = "none")

ggsave("three_indices.png", p2, width = 12, height = 4, dpi = 300)

# 3. Employment Elasticity Comparison
elasticity_data <- data.frame(
  Period = names(orf_elasticity),
  Elasticity = unname(orf_elasticity)
)

p3 <- ggplot(elasticity_data, aes(x = Period, y = Elasticity, fill = Period)) +
  geom_bar(stat = "identity", width = 0.6) +
  geom_text(aes(label = Elasticity), vjust = -0.5, size = 5, fontface = "bold") +
  scale_fill_manual(values = c("#ef4444", "#10b981")) +
  labs(title = "Employment elasticity of growth, two periods",
       subtitle = "Published estimates: Ghosh and Roy Bardhan, ORF Expert Speak, 2 October 2024",
       y = "Employment Elasticity of Growth") +
  theme_india +
  theme(legend.position = "none")

ggsave("employment_elasticity.png", p3, width = 8, height = 6, dpi = 300)

################################################################################
# SECTION 6: STATISTICAL TESTS
################################################################################

# 1. Structural break test for employment
library(strucchange)
employment_ts <- ts(data$formal_employment, start = 2014, frequency = 1)
breakpoints <- breakpoints(employment_ts ~ seq_along(employment_ts))
summary(breakpoints)

# 2. Correlation analysis
cor_matrix <- cor(data[, c("gdp_growth", "unemployment", "top1_percent", 
                           "formal_employment", "press_freedom_rank")], 
                  use = "complete.obs")
print(round(cor_matrix, 2))

# 3. Regression analysis: Inequality drivers
inequality_model_full <- lm(top1_percent ~ gdp_growth + formal_employment + 
                           press_freedom_rank + fci, data = data)
summary(inequality_model_full)

################################################################################
# SECTION 7: EXPORT RESULTS
################################################################################

# Create summary statistics table
summary_stats <- data %>%
  group_by(period = ifelse(year <= 2019, "2014-2019", "2020-2025")) %>%
  summarise(
    avg_gdp_growth = mean(gdp_growth, na.rm = TRUE),
    avg_unemployment = mean(unemployment, na.rm = TRUE),
    avg_top1_share = mean(top1_percent, na.rm = TRUE),
    avg_formal_emp = mean(formal_employment, na.rm = TRUE),
    avg_press_freedom = mean(press_freedom_rank, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_stats, "summary_statistics.csv")

# Export indices
indices_export <- data %>%
  select(year, ssi, fci, dqi)
write_csv(indices_export, "three_indices.csv")

# Export for web visualization (JSON format)
library(jsonlite)
json_data <- list(
  metadata = list(
    title = "India Economic Indicators 2014-2025",
    lastUpdated = Sys.Date()
  ),
  timeSeries = list(
    years = data$year,
    gdpGrowth = data$gdp_growth,
    unemployment = list(overall = data$unemployment),
    inequality = list(top1Percent = data$top1_percent),
    employment = list(formalSector = data$formal_employment),
    democraticIndicators = list(pressFreedomRank = data$press_freedom_rank),
    indices = list(ssi = data$ssi, fci = data$fci, dqi = data$dqi)
  )
)

write_json(json_data, "replication_output.json", pretty = TRUE)  # data.json is the source of record

################################################################################
# SECTION 8: GENERATE CUSTOM DATASETS
################################################################################

# Function to create filtered datasets based on user needs
generate_custom_dataset <- function(data, indicators, years, filename) {
  custom_data <- data %>%
    filter(year %in% years) %>%
    select(year, all_of(indicators))
  
  write_csv(custom_data, filename)
  print(paste("Custom dataset saved as:", filename))
  return(custom_data)
}

# Example: Create employment-focused dataset
employment_dataset <- generate_custom_dataset(
  data,
  indicators = c("employment", "formal_employment", "unemployment", 
                "youth_unemployment", "manufacturing_jobs"),
  years = 2014:2025,
  filename = "employment_analysis.csv"
)

# Example: Create inequality dataset
inequality_dataset <- generate_custom_dataset(
  data,
  indicators = c("top1_percent", "top10_percent", "bottom50_percent", 
                "gini_coefficient"),
  years = 2014:2025,
  filename = "inequality_analysis.csv"
)

# Example: Create fiscal federalism dataset
fiscal_dataset <- generate_custom_dataset(
  data,
  indicators = c("cess_percentage", "actual_devolution", "promised_devolution",
                "state_borrowing", "central_spending"),
  years = 2014:2025,
  filename = "fiscal_federalism.csv"
)

print("Replication complete! All analyses, visualizations, and datasets generated.")
print("Check your working directory for output files.")

################################################################################
# END OF REPLICATION CODE
################################################################################
