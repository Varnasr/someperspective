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

# Calculate employment elasticity
employment_elasticity <- function(data, start_year, end_year) {
  emp_growth <- (data$employment[data$year == end_year] - 
                 data$employment[data$year == start_year]) / 
                 data$employment[data$year == start_year] * 100
  
  gdp_growth <- (data$gdp[data$year == end_year] - 
                 data$gdp[data$year == start_year]) / 
                 data$gdp[data$year == start_year] * 100
  
  return(emp_growth / gdp_growth)
}

# Calculate for two periods
elasticity_2011_2016 <- employment_elasticity(data, 2011, 2016)  # Result: 0.01
elasticity_2017_2023 <- employment_elasticity(data, 2017, 2023)  # Result: 1.11

################################################################################
# SECTION 3: THREE NOVEL INDICES
################################################################################

# The three indices are defined canonically (for both eras, 2004-2026) in
# data/compute_indices.py. This R port reproduces that exact logic. Keep the two
# in sync; the Python file is the single source of truth.

# Component inputs (2004-2026) ------------------------------------------------
idx_years <- 2004:2026

# SSI: weighted binary triggers; UPA years have none -> 0
ssi_weights <- c(census = 3.0, consumption = 2.5, employment = 2.0,
                 gdp = 1.5, committee = 1.0)
ssi_triggers <- list(
  "2015" = c("gdp"), "2016" = c("gdp"),
  "2017" = c("employment", "gdp"),
  "2018" = c("consumption", "employment", "gdp"),
  "2019" = c("consumption", "gdp", "committee"),
  "2020" = c("census", "consumption", "gdp"),
  "2021" = c("census", "gdp"), "2022" = c("census", "gdp"),
  "2023" = c("census", "gdp"), "2024" = c("census", "gdp"),
  "2025" = c("census", "gdp"), "2026" = c("census", "gdp")
)
calculate_ssi <- function(year) {
  trig <- ssi_triggers[[as.character(year)]]
  if (is.null(trig)) return(0)
  round(sum(ssi_weights[trig]), 2)
}

# FCI: mean of 5 min-max-normalised centralisation components over 2004-2026
# columns: cess, devolution, states_own_rev, css_share, borrowing
fci_comp <- matrix(c(
  6.5,36.5,45.0,22.0,0.0, 7.0,36.3,44.8,22.8,0.0, 7.5,36.1,44.5,23.5,0.0,
  8.0,35.9,44.2,24.2,0.0, 8.5,35.8,44.0,24.8,0.0, 9.0,35.7,43.7,25.4,0.0,
  9.3,35.6,43.4,26.0,0.0, 9.6,35.5,43.1,26.6,0.0, 9.9,35.4,42.9,27.2,0.0,
  10.1,35.3,42.7,27.7,0.0, 10.4,35.0,42.5,28.3,0.0, 11.5,35.6,41.8,29.5,0.0,
  13.5,36.2,40.2,31.2,0.0, 15.3,36.6,38.5,33.8,0.0, 17.8,35.5,37.2,36.5,0.0,
  19.0,34.0,36.1,38.9,0.0, 20.2,33.0,34.5,42.3,1.0, 18.3,32.7,35.2,41.5,0.5,
  16.3,32.4,36.8,40.2,0.0, 14.8,32.1,37.5,39.8,0.0, 14.8,31.8,37.9,39.5,0.0,
  14.6,31.6,38.0,39.2,0.0, 14.5,31.4,38.1,39.0,0.0),
  ncol = 5, byrow = TRUE)
mm <- function(x) { r <- max(x) - min(x); if (r == 0) rep(0, length(x)) else (x - min(x)) / r }
fci_series <- {
  c1 <- mm(fci_comp[,1]); c2 <- 1 - mm(fci_comp[,2]); c3 <- 1 - mm(fci_comp[,3])
  c4 <- mm(fci_comp[,4]); c5 <- fci_comp[,5]
  round((c1 + c2 + c3 + c4 + c5) / 5, 2)
}
names(fci_series) <- idx_years

# DQI: geometric mean of V-Dem, FreedomHouse/100, (180-RSF)/180
dqi_comp <- matrix(c(
  0.553,78,120, 0.560,78,106, 0.562,78,105, 0.567,78,120, 0.566,78,118,
  0.567,79,105, 0.566,79,122, 0.560,79,131, 0.557,79,140, 0.554,78,140,
  0.555,78,140, 0.529,77,136, 0.501,77,133, 0.462,77,136, 0.422,75,138,
  0.389,71,140, 0.365,67,142, 0.357,66,142, 0.290,66,150, 0.275,66,161,
  0.271,66,159, 0.270,66,151, 0.270,66,157),
  ncol = 3, byrow = TRUE)
calculate_dqi <- function(year) {
  i <- which(idx_years == year)
  v <- dqi_comp[i,1]; f <- dqi_comp[i,2] / 100; r <- (180 - dqi_comp[i,3]) / 180
  round((v * f * r)^(1/3), 2)
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
  Period = c("2011-2016", "2017-2023"),
  Elasticity = c(0.01, 1.11)
)

p3 <- ggplot(elasticity_data, aes(x = Period, y = Elasticity, fill = Period)) +
  geom_bar(stat = "identity", width = 0.6) +
  geom_text(aes(label = Elasticity), vjust = -0.5, size = 5, fontface = "bold") +
  scale_fill_manual(values = c("#ef4444", "#10b981")) +
  labs(title = "Employment Elasticity: The Jobs Recovery Paradox",
       subtitle = "Higher elasticity post-2017 driven by informal employment",
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

write_json(json_data, "data.json", pretty = TRUE)

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
