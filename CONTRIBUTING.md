# Contributing to Some Perspective

Thank you for your interest in contributing to this research project! This document provides guidelines for different types of contributions.

## Types of Contributions

### 1. Data Corrections

If you identify errors in the dataset:

1. **Check the original source** first using the references in `data/sources.bib`
2. **Open an issue** with:
   - Variable name and year affected
   - Current (incorrect) value
   - Correct value with source documentation
   - Link to authoritative source
3. **Include evidence**: Screenshots, PDF pages, or archived links

**Example:**
```markdown
**Variable:** GDP Growth Rate
**Year:** 2019
**Current value:** 6.1%
**Correct value:** 5.2%
**Source:** RBI Annual Report 2019-20, page 45
**Link:** [RBI Report](https://rbi.org.in/...)
```

### 2. Code Improvements

We welcome improvements to analysis code:

**Before submitting:**
- Ensure code runs without errors
- Add comments explaining complex operations
- Update documentation if changing functionality
- Run existing tests: `Rscript tests/run_tests.R`

**Pull request process:**
1. Fork the repository
2. Create a feature branch: `git checkout -b improve-analysis`
3. Make your changes
4. Test thoroughly
5. Submit PR with clear description of changes

### 3. Extending the Analysis

Contributions extending the research are encouraged:

**State-level analysis:**
- Use same methodology applied to state data
- Document data sources thoroughly
- Include validation against national aggregates

**Sectoral analysis:**
- Focus on specific sectors (manufacturing, services, agriculture)
- Maintain consistency with aggregate findings
- Document sector-specific data challenges

**International comparisons:**
- Apply SSI, FCI, DQI indices to other countries
- Document methodological adaptations required
- Ensure data comparability

### 4. Documentation

Help improve documentation:

- Fix typos or unclear explanations
- Add examples to methodology
- Improve code comments
- Translate documentation (if multilingual version needed)

## Coding Standards

### R Code

```r
# Use tidyverse style guide
# Functions should have clear names
calculate_employment_elasticity <- function(employment_growth, gdp_growth) {
  # Input validation
  if (!is.numeric(employment_growth) || !is.numeric(gdp_growth)) {
    stop("Inputs must be numeric")
  }
  
  # Calculate elasticity
  elasticity <- employment_growth / gdp_growth
  
  return(elasticity)
}

# Use meaningful variable names
fiscal_transfer_share <- state_transfers / gross_tax_revenue

# Comment complex calculations
# Calculate Pareto interpolation for top 1% share
# Using formula from Piketty & Saez (2003)
top1_share <- pareto_interpolate(tax_data, threshold = 0.99)
```

### Data Formatting

- **JSON:** Use 2-space indentation
- **CSV:** UTF-8 encoding, comma-separated
- **Dates:** ISO 8601 format (YYYY-MM-DD)
- **Numbers:** No thousands separators, use decimal points

## Submission Checklist

Before submitting any contribution:

- [ ] Code runs without errors
- [ ] All functions have documentation
- [ ] New data includes source references
- [ ] Changes don't break existing functionality
- [ ] README updated if adding new features
- [ ] CHANGELOG.md updated with changes

## Review Process

1. **Initial review** (1-3 days): Maintainer checks submission format
2. **Technical review** (1-2 weeks): Code/data validation
3. **Integration testing**: Ensure compatibility with existing code
4. **Acceptance**: Merge and credit in CHANGELOG

## Questions?

- **Technical questions:** Open a GitHub issue
- **General inquiries:** Email [your-email@domain.com]
- **Collaboration proposals:** Contact via website

## Code of Conduct

This project maintains high standards of academic integrity:

1. **Be respectful:** Engage professionally with other contributors
2. **Be accurate:** Only submit verified information
3. **Be transparent:** Document all sources and methods
4. **Be constructive:** Focus feedback on improving the work

## Attribution

All contributors will be acknowledged in:
- CHANGELOG.md for specific contributions
- Acknowledgments section for substantial contributions
- Co-authorship for major extensions (by agreement)

## License

By contributing, you agree that your contributions will be licensed under CC BY 4.0, the same license as the project.

---

Thank you for helping improve this research!
