import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('df.csv')

# Define the columns
screentime_col = 'What is your average screentime?'  # Ensure this is numeric (e.g., hours)
tiktok_usage_col = 'What is your average daily time on Tik Tok or Tik Tok equivalents?'  # Ensure this is numeric
gpa_col = 'What was your GPA LAST SEMESTER?'  # Ensure this is numeric

# Check if the required columns exist
required_cols = [screentime_col, tiktok_usage_col, gpa_col]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    print(f"Error: The following required columns are missing from the dataset: {missing_cols}")
else:
    # Drop rows with missing values in the relevant columns
    df_clean = df.dropna(subset=required_cols)

    # Ensure that the numeric columns are of numeric type
    df_clean[screentime_col] = pd.to_numeric(df_clean[screentime_col], errors='coerce')
    df_clean[tiktok_usage_col] = pd.to_numeric(df_clean[tiktok_usage_col], errors='coerce')
    df_clean[gpa_col] = pd.to_numeric(df_clean[gpa_col], errors='coerce')

    # Drop any rows that became NaN after conversion
    df_clean = df_clean.dropna(subset=[screentime_col, tiktok_usage_col, gpa_col])

    # ---------------------------
    # Scatter Plot: GPA vs. Screentime
    # ---------------------------

    plt.figure(figsize=(14, 10))
    sns.scatterplot(
        data=df_clean,
        x=screentime_col,
        y=gpa_col,
        color='blue',
        alpha=0.7,
        edgecolor='w'
    )

    # Add Regression Line
    sns.regplot(
        data=df_clean,
        x=screentime_col,
        y=gpa_col,
        scatter=False,
        color='grey'
    )

    # Titles and Labels
    plt.title('GPA vs. Screentime', fontsize=16)
    plt.xlabel('Screentime (hours)', fontsize=14)
    plt.ylabel('GPA Last Semester', fontsize=14)

    plt.tight_layout()
    plt.show()

    # ---------------------------
    # Scatter Plot: GPA vs. TikTok Usage
    # ---------------------------

    plt.figure(figsize=(14, 10))
    sns.scatterplot(
        data=df_clean,
        x=tiktok_usage_col,
        y=gpa_col,
        color='green',
        alpha=0.7,
        edgecolor='w'
    )

    # Add Regression Line
    sns.regplot(
        data=df_clean,
        x=tiktok_usage_col,
        y=gpa_col,
        scatter=False,
        color='grey'
    )

    # Titles and Labels
    plt.title('GPA vs. TikTok Usage', fontsize=16)
    plt.xlabel('TikTok Usage (hours)', fontsize=14)
    plt.ylabel('GPA Last Semester', fontsize=14)

    plt.tight_layout()
    plt.show()

    # ---------------------------
    # Correlation Calculations
    # ---------------------------

    from scipy.stats import pearsonr

    # Pearson Correlation: Screentime vs. GPA
    corr_screentime_gpa, p_val_screentime_gpa = pearsonr(df_clean[screentime_col], df_clean[gpa_col])
    print(f'\nPearson correlation between Screentime and GPA: {corr_screentime_gpa:.2f}, P-value: {p_val_screentime_gpa:.4f}')

    # Pearson Correlation: TikTok Usage vs. GPA
    corr_tiktok_gpa, p_val_tiktok_gpa = pearsonr(df_clean[tiktok_usage_col], df_clean[gpa_col])
    print(f'Pearson correlation between TikTok Usage and GPA: {corr_tiktok_gpa:.2f}, P-value: {p_val_tiktok_gpa:.4f}')

    # Pearson Correlation: Screentime vs. TikTok Usage
    corr_screentime_tiktok, p_val_screentime_tiktok = pearsonr(df_clean[screentime_col], df_clean[tiktok_usage_col])
    print(f'Pearson correlation between Screentime and TikTok Usage: {corr_screentime_tiktok:.2f}, P-value: {p_val_screentime_tiktok:.4f}')

    # Interpretation
    alpha = 0.05
    correlations = [
        ('Screentime vs GPA', corr_screentime_gpa, p_val_screentime_gpa),
        ('TikTok Usage vs GPA', corr_tiktok_gpa, p_val_tiktok_gpa),
        ('Screentime vs TikTok Usage', corr_screentime_tiktok, p_val_screentime_tiktok)
    ]

    for name, corr, p_val in correlations:
        if p_val < alpha:
            result = "statistically significant"
        else:
            result = "not statistically significant"
        print(f"Result: The correlation between {name} is {result} (p-value = {p_val:.4f}).")