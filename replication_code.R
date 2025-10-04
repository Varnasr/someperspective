################################################################################
# REPLICATION CODE: India Political Economy Assessment 2014-2025
# Author: Dr. Varna Sri Raman
# Date: October 2025
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

# 1. STATISTICAL SUPPRESSION INDEX (SSI)
calculate_ssi <- function(year) {
  events <- data.frame(
    year = c(2017, 2019, 2020, 2021, 2023),
    event = c("Consumption Survey Withheld", "PLFS Delayed", 
              "GDP Revision", "Census Postponed", "Multiple Suppressions"),
    severity = c(1.0, 0.5, 0.3, 1.0, 0.8),
    salience = c(0.8, 0.7, 0.6, 1.0, 0.9)
  )
  
  year_events <- events[events$year == year, ]
  if(nrow(year_events) == 0) return(0)
  
  ssi <- sum(year_events$severity * year_events$salience) / nrow(year_events)
  return(ssi)
}

# Calculate SSI for all years
data$ssi <- sapply(data$year, calculate_ssi)

# 2. FISCAL CENTRALIZATION INDEX (FCI)
calculate_fci <- function(data, year) {
  row <- data[data$year == year, ]
  
  # Components (normalized 0-1)
  cess_component <- row$cess_percentage / 25  # Normalize by max possible 25%
  devolution_component <- 1 - (row$actual_devolution / row$promised_devolution)
  borrowing_conditions <- row$conditional_borrowing / row$total_borrowing
  
  # Average of three components
  fci <- mean(c(cess_component, devolution_component, borrowing_conditions), na.rm = TRUE)
  return(fci)
}

# Calculate FCI
data$fci <- sapply(data$year, function(y) calculate_fci(data, y))

# 3. DEMOCRATIC QUALITY INDEX (DQI)
calculate_dqi <- function(data, year) {
  row <- data[data$year == year, ]
  
  # Normalize press freedom rank (180 = worst)
  press_freedom_norm <- (180 - row$press_freedom_rank) / 180
  
  # V-Dem score (already 0-1)
  vdem_score <- row$vdem_liberal_democracy
  
  # Freedom House score (normalize from 100 point scale)
  fh_score <- row$freedom_house_score / 100
  
  # Geometric mean ensures weakness in any dimension reduces overall score
  dqi <- (press_freedom_norm * vdem_score * fh_score)^(1/3)
  return(dqi)
}

# Calculate DQI
data$dqi <- sapply(data$year, function(y) calculate_dqi(data, y))

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
