# Replication code (R) for "Some Perspective: India's Political Economy, 2004-2026".
# Author: Dr. Varna Sri Raman. Licence: CC BY 4.0.
#
# Reads data/SP_masterdataset.csv, prints the UPA (2004-2013) and NDA
# (2014-2026) averages for each measure in the cross-era scorecard with the
# verdict on each, and draws the three constructed indices. Base R only; run
# from the repository root:  Rscript replication_code.R
#
# The indices themselves are computed by data/compute_indices.py, and
# replication_code.py confirms the CSV columns equal a fresh computation.
# Averages use the years with a published figure only.
#
# Employment elasticity is not computed here. The site reports published
# estimates (technical appendix A5): 0.01 for 2004-05 to 2009-10 (RBI Working
# Paper 06/2014, Table 4), 0.01 for 2011-16 and 1.11 for 2017-23 (Ghosh and
# Roy Bardhan, ORF Expert Speak, 2 October 2024).

data <- read.csv("data/SP_masterdataset.csv", stringsAsFactors = FALSE)

scorecard <- data.frame(
  column = c("GDP_Growth", "CPI_Inflation", "Fiscal_Deficit_Pct_GDP",
             "Top_1pct_Income_Share", "Bottom_50pct_Share", "Press_Freedom_Rank",
             "SSI", "FCI", "DQI"),
  label = c("GDP growth (%)", "CPI inflation (%)", "Fiscal deficit (% of GDP)",
            "Top 1% income share (%)", "Bottom 50% income share (%)",
            "Press freedom rank (of 180)", "Statistical Suppression Index",
            "Fiscal Centralisation Index", "Democratic Quality Index"),
  high_is_worse = c(FALSE, TRUE, TRUE, TRUE, FALSE, TRUE, TRUE, TRUE, FALSE),
  stringsAsFactors = FALSE
)

upa <- data[data$Period == "UPA", ]
nda <- data[data$Period == "NDA", ]

scorecard$upa <- sapply(scorecard$column, function(c) mean(upa[[c]], na.rm = TRUE))
scorecard$nda <- sapply(scorecard$column, function(c) mean(nda[[c]], na.rm = TRUE))
scorecard$nda_worse <- ifelse(scorecard$high_is_worse,
                              scorecard$nda > scorecard$upa,
                              scorecard$nda < scorecard$upa)

print(scorecard[, c("label", "upa", "nda", "nda_worse")], digits = 4, row.names = FALSE)
cat(sprintf("\nNDA period worse on %d of %d comparable measures.\n",
            sum(scorecard$nda_worse), nrow(scorecard)))

png("replication_indices_R.png", width = 1500, height = 420)
par(mfrow = c(1, 3))
titles <- c(SSI = "Statistical Suppression Index (0-10)",
            FCI = "Fiscal Centralisation Index (0-1)",
            DQI = "Democratic Quality Index (0-1)")
for (ix in names(titles)) {
  plot(data$Year, data[[ix]], type = "o", pch = 16, xlab = "Year", ylab = ix,
       main = titles[[ix]])
  abline(v = 2013.5, col = "grey")
}
invisible(dev.off())
cat("Wrote replication_indices_R.png\n")
