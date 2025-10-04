#!/usr/bin/env python3
"""
REPLICATION CODE: India Political Economy Assessment 2014-2025
Author: Dr. Varna Sri Raman
Date: October 2025
Description: Complete replication code for all analyses and indices
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
from datetime import datetime

# Set style for all plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

################################################################################
# SECTION 1: DATA LOADING AND PREPARATION
################################################################################

def load_and_prepare_data(filepath='data/SP_masterdataset.csv'):
    """Load and prepare the master dataset"""
    data = pd.read_csv(filepath)
    
    # Display basic information
    print("Dataset Shape:", data.shape)
    print("\nColumn Names:")
    print(data.columns.tolist())
    print("\nFirst few rows:")
    print(data.head())
    print("\nData types:")
    print(data.dtypes)
    print("\nSummary statistics:")
    print(data.describe())
    
    return data

# Load data
data = load_and_prepare_data()

################################################################################
# SECTION 2: KEY ECONOMIC INDICATORS
################################################################################

def calculate_employment_elasticity(data, start_year, end_year):
    """Calculate employment elasticity of growth"""
    start_data = data[data['year'] == start_year].iloc[0]
    end_data = data[data['year'] == end_year].iloc[0]
    
    emp_growth = ((end_data['employment'] - start_data['employment']) / 
                  start_data['employment'] * 100)
    gdp_growth = ((end_data['gdp'] - start_data['gdp']) / 
                  start_data['gdp'] * 100)
    
    elasticity = emp_growth / gdp_growth if gdp_growth != 0 else 0
    return round(elasticity, 2)

# Calculate for two periods
elasticity_2011_2016 = calculate_employment_elasticity(data, 2011, 2016)  # Result: 0.01
elasticity_2017_2023 = calculate_employment_elasticity(data, 2017, 2023)  # Result: 1.11

print(f"\nEmployment Elasticity:")
print(f"2011-2016: {elasticity_2011_2016}")
print(f"2017-2023: {elasticity_2017_2023}")

################################################################################
# SECTION 3: THREE NOVEL INDICES
################################################################################

def calculate_ssi(year):
    """Calculate Statistical Suppression Index"""
    events = {
        2017: [("Consumption Survey Withheld", 1.0, 0.8)],
        2019: [("PLFS Delayed", 0.5, 0.7), ("NSC Resignations", 0.8, 0.6)],
        2020: [("GDP Revision", 0.3, 0.6)],
        2021: [("Census Postponed", 1.0, 1.0)],
        2023: [("Multiple Suppressions", 0.8, 0.9)]
    }
    
    if year not in events:
        return 0
    
    year_events = events[year]
    total_score = sum(severity * salience for _, severity, salience in year_events)
    return total_score / len(year_events)

def calculate_fci(row):
    """Calculate Fiscal Centralization Index"""
    # Normalize components to 0-1 scale
    cess_component = row['cess_percentage'] / 25  # Max 25%
    devolution_component = 1 - (row['actual_devolution'] / row['promised_devolution'])
    borrowing_component = row['conditional_borrowing'] / row['total_borrowing']
    
    # Average of three components
    components = [cess_component, devolution_component, borrowing_component]
    return np.nanmean(components)

def calculate_dqi(row):
    """Calculate Democratic Quality Index"""
    # Normalize press freedom (180 = worst)
    press_freedom_norm = (180 - row['press_freedom_rank']) / 180
    
    # V-Dem score (already 0-1)
    vdem_score = row['vdem_liberal_democracy']
    
    # Freedom House score (normalize from 100)
    fh_score = row['freedom_house_score'] / 100
    
    # Geometric mean
    return (press_freedom_norm * vdem_score * fh_score) ** (1/3)

# Calculate all indices
data['ssi'] = data['year'].apply(calculate_ssi)
data['fci'] = data.apply(calculate_fci, axis=1)
data['dqi'] = data.apply(calculate_dqi, axis=1)

print("\nIndices calculated successfully")
print(data[['year', 'ssi', 'fci', 'dqi']].head())

################################################################################
# SECTION 4: INEQUALITY ANALYSIS
################################################################################

def calculate_gini(income_shares):
    """Calculate Gini coefficient"""
    sorted_shares = np.sort(income_shares)
    n = len(sorted_shares)
    cumsum = np.cumsum(sorted_shares)
    return (2 * np.sum((n - np.arange(n)) * sorted_shares)) / (n * np.sum(sorted_shares)) - 1

def analyze_inequality_trend(data):
    """Analyze inequality trends"""
    # Linear regression on top 1% share
    from sklearn.linear_model import LinearRegression
    
    X = data['year'].values.reshape(-1, 1)
    y = data['top1_percent'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict 2025
    prediction_2025 = model.predict([[2025]])[0]
    
    # Calculate trend statistics
    slope = model.coef_[0]
    r_squared = model.score(X, y)
    
    print("\nInequality Trend Analysis:")
    print(f"Annual increase in top 1% share: {slope:.2f} percentage points")
    print(f"R-squared: {r_squared:.3f}")
    print(f"Predicted top 1% share in 2025: {prediction_2025:.1f}%")
    
    return model

inequality_model = analyze_inequality_trend(data)

################################################################################
# SECTION 5: VISUALIZATIONS
################################################################################

def create_key_indicators_plot(data):
    """Create key economic indicators visualization"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(data['year'], data['gdp_growth'], marker='o', label='GDP Growth (%)', 
            color='#10b981', linewidth=2)
    ax.plot(data['year'], data['unemployment'], marker='s', label='Unemployment (%)', 
            color='#ef4444', linewidth=2)
    ax.plot(data['year'], data['top1_percent'], marker='^', label='Top 1% Share (%)', 
            color='#f97316', linewidth=2)
    
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Value (%)', fontsize=12)
    ax.set_title('Key Economic Indicators (2014-2025)', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('key_indicators.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_indices_plot(data):
    """Create three indices visualization"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    indices = [('ssi', 'Statistical Suppression', '#dc2626'),
               ('fci', 'Fiscal Centralization', '#f59e0b'),
               ('dqi', 'Democratic Quality', '#3b82f6')]
    
    for ax, (index, title, color) in zip(axes, indices):
        ax.plot(data['year'], data[index], marker='o', color=color, linewidth=2)
        ax.fill_between(data['year'], data[index], alpha=0.3, color=color)
        ax.set_xlabel('Year', fontsize=11)
        ax.set_ylabel('Index Value', fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('Three Indices of Institutional Change', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('three_indices.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_employment_elasticity_plot():
    """Create employment elasticity comparison"""
    periods = ['2011-2016', '2017-2023']
    elasticity = [0.01, 1.11]
    colors = ['#ef4444', '#10b981']
    
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(periods, elasticity, color=colors, width=0.6)
    
    # Add value labels on bars
    for bar, val in zip(bars, elasticity):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{val}', ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    ax.set_ylabel('Employment Elasticity of Growth', fontsize=12)
    ax.set_title('Employment Elasticity: The Jobs Recovery Paradox', fontsize=14, fontweight='bold')
    ax.set_subtitle('Higher elasticity post-2017 driven by informal employment', fontsize=10)
    ax.set_ylim(0, 1.3)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('employment_elasticity.png', dpi=300, bbox_inches='tight')
    plt.show()

# Create all visualizations
create_key_indicators_plot(data)
create_indices_plot(data)
create_employment_elasticity_plot()

################################################################################
# SECTION 6: STATISTICAL TESTS
################################################################################

def perform_statistical_tests(data):
    """Perform various statistical tests"""
    print("\n" + "="*60)
    print("STATISTICAL TESTS")
    print("="*60)
    
    # 1. Correlation analysis
    correlation_vars = ['gdp_growth', 'unemployment', 'top1_percent', 
                       'formal_employment', 'press_freedom_rank']
    corr_matrix = data[correlation_vars].corr()
    
    print("\nCorrelation Matrix:")
    print(corr_matrix.round(2))
    
    # 2. Structural break test (simplified)
    from scipy import stats
    
    # Test for structural break in formal employment around 2016
    pre_2016 = data[data['year'] <= 2016]['formal_employment']
    post_2016 = data[data['year'] > 2016]['formal_employment']
    
    t_stat, p_value = stats.ttest_ind(pre_2016, post_2016)
    print(f"\nStructural Break Test (Formal Employment):")
    print(f"T-statistic: {t_stat:.3f}")
    print(f"P-value: {p_value:.4f}")
    
    # 3. Multiple regression
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler
    
    # Prepare data
    features = ['gdp_growth', 'formal_employment', 'press_freedom_rank', 'fci']
    X = data[features].dropna()
    y = data.loc[X.index, 'top1_percent']
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Fit model
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    print(f"\nMultiple Regression: Inequality Drivers")
    print(f"R-squared: {model.score(X_scaled, y):.3f}")
    print("\nCoefficients:")
    for feature, coef in zip(features, model.coef_):
        print(f"  {feature}: {coef:.3f}")

perform_statistical_tests(data)

################################################################################
# SECTION 7: EXPORT RESULTS
################################################################################

def export_results(data):
    """Export all results to various formats"""
    
    # 1. Summary statistics by period
    data['period'] = data['year'].apply(lambda x: '2014-2019' if x <= 2019 else '2020-2025')
    
    summary_stats = data.groupby('period').agg({
        'gdp_growth': 'mean',
        'unemployment': 'mean',
        'top1_percent': 'mean',
        'formal_employment': 'mean',
        'press_freedom_rank': 'mean'
    }).round(2)
    
    summary_stats.to_csv('summary_statistics.csv')
    print("\nSummary statistics saved to 'summary_statistics.csv'")
    
    # 2. Export indices
    indices_df = data[['year', 'ssi', 'fci', 'dqi']]
    indices_df.to_csv('three_indices.csv', index=False)
    print("Indices saved to 'three_indices.csv'")
    
    # 3. Export to JSON for web visualization
    json_data = {
        'metadata': {
            'title': 'India Economic Indicators 2014-2025',
            'lastUpdated': datetime.now().strftime('%Y-%m-%d')
        },
        'timeSeries': {
            'years': data['year'].tolist(),
            'gdpGrowth': data['gdp_growth'].tolist(),
            'unemployment': {'overall': data['unemployment'].tolist()},
            'inequality': {'top1Percent': data['top1_percent'].tolist()},
            'employment': {'formalSector': data['formal_employment'].tolist()},
            'democraticIndicators': {'pressFreedomRank': data['press_freedom_rank'].tolist()},
            'indices': {
                'ssi': data['ssi'].tolist(),
                'fci': data['fci'].tolist(),
                'dqi': data['dqi'].tolist()
            }
        }
    }
    
    with open('data.json', 'w') as f:
        json.dump(json_data, f, indent=2)
    print("JSON data saved to 'data.json'")

export_results(data)

################################################################################
# SECTION 8: GENERATE CUSTOM DATASETS
################################################################################

def generate_custom_dataset(data, indicators, years, filename):
    """Generate custom filtered datasets"""
    custom_data = data[data['year'].isin(years)][['year'] + indicators]
    custom_data.to_csv(filename, index=False)
    print(f"Custom dataset saved as: {filename}")
    return custom_data

# Generate specialized datasets
print("\n" + "="*60)
print("GENERATING CUSTOM DATASETS")
print("="*60)

# Employment dataset
employment_indicators = ['employment', 'formal_employment', 'unemployment', 
                         'youth_unemployment', 'manufacturing_jobs']
employment_data = generate_custom_dataset(
    data, employment_indicators, 
    range(2014, 2026), 
    'employment_analysis.csv'
)

# Inequality dataset
inequality_indicators = ['top1_percent', 'top10_percent', 'bottom50_percent', 
                         'gini_coefficient']
inequality_data = generate_custom_dataset(
    data, inequality_indicators, 
    range(2014, 2026), 
    'inequality_analysis.csv'
)

# Fiscal federalism dataset
fiscal_indicators = ['cess_percentage', 'actual_devolution', 'promised_devolution',
                     'state_borrowing', 'central_spending']
fiscal_data = generate_custom_dataset(
    data, fiscal_indicators, 
    range(2014, 2026), 
    'fiscal_federalism.csv'
)

# Democratic indicators dataset
democratic_indicators = ['press_freedom_rank', 'vdem_liberal_democracy', 
                        'freedom_house_score', 'internet_shutdowns']
democratic_data = generate_custom_dataset(
    data, democratic_indicators, 
    range(2014, 2026), 
    'democratic_indicators.csv'
)

print("\n" + "="*60)
print("REPLICATION COMPLETE!")
print("="*60)
print("\nAll analyses, visualizations, and datasets have been generated.")
print("Check your working directory for the following output files:")
print("  - key_indicators.png")
print("  - three_indices.png") 
print("  - employment_elasticity.png")
print("  - summary_statistics.csv")
print("  - three_indices.csv")
print("  - data.json")
print("  - employment_analysis.csv")
print("  - inequality_analysis.csv")
print("  - fiscal_federalism.csv")
print("  - democratic_indicators.csv")

################################################################################
# END OF REPLICATION CODE
################################################################################
