import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Load raw data
df = pd.read_csv(r'C:\google_play_analytics_project\data\googleplaystore.csv')

print("===== RAW DATA SHAPE =====")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())
print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

# ANOMALY 1: Impossible ratings (Play Store max = 5.0)
print("===== ANOMALY: Rating above 5.0 =====")
bad_rating = df[pd.to_numeric(df['Rating'], errors='coerce') > 5]
print(bad_rating[['App', 'Category', 'Rating', 'Reviews', 'Size', 'Installs']])

# Save anomaly for report 
bad_rating.to_csv(r'C:\google_play_analytics_project\data\anomaly_log_bad_rating.csv', index=False)
print(f"\nFound {len(bad_rating)} corrupted row(s). Saved to anomaly_log_bad_rating.csv")

# Remove this single malformed row (column-shift corruption)
df = df[pd.to_numeric(df['Rating'], errors='coerce') <= 5.0].copy()
print(f"Shape after removing corrupted row: {df.shape}")

print("===== BEFORE dropping missing Rating =====")
print(df.isnull().sum())

rows_before = df.shape[0]

# Drop ONLY rows where Rating is missing. All other columns untouched.
df = df.dropna(subset=['Rating']).copy()

rows_after = df.shape[0]

print(f"\nRows removed: {rows_before - rows_after}")
print(f"New shape: {df.shape}")
print("\n=== AFTER (notice other columns still have their NaN) ===")
print(df.isnull().sum())

# ANOMALY 2: Duplicate app listings
print("===== ANOMALY: Duplicate Apps =====")
print(f"Exact duplicate rows: {df.duplicated().sum()}")
print(f"Duplicate app NAMES: {df.duplicated(subset=['App']).sum()}")

# I Show a real example
print("\nExample - 'Instagram' appears multiple times:")
print(df[df['App'] == 'Instagram'][['App', 'Rating', 'Reviews', 'Installs']])


# Remove exact duplicates first
df = df.drop_duplicates().copy()

# For duplicate app names, keep the record with the MOST reviews (most recent snapshot)
df['Reviews_temp'] = pd.to_numeric(df['Reviews'], errors='coerce')
df = df.sort_values('Reviews_temp', ascending=False)
df = df.drop_duplicates(subset=['App'], keep='first').copy()
df = df.drop(columns=['Reviews_temp'])

print(f"\nShape after deduplication: {df.shape}")
print(f"Unique apps now: {df['App'].nunique()}")

df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce').astype('Int64')

print("===== Reviews column cleaned =====")
print(df['Reviews'].describe())

# Installs looks like "10,000+" — remove '+' and ','
df['Installs'] = (
    df['Installs']
    .astype(str)
    .str.replace('+', '', regex=False)
    .str.replace(',', '', regex=False)
)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce').astype('Int64')

print("===== Installs cleaned =====")
print(df['Installs'].value_counts().sort_index().head(10))
print(f"\nMax installs: {df['Installs'].max():,}")

# Clean Price column - remove '$' and convert to float
df['Price'] = (
    df['Price']
    .astype(str)
    .str.replace('$', '', regex=False)
)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# I Create a useful business metric - Is_Paid flag
df['Is_Paid'] = np.where(df['Price'] > 0, 1, 0)

print("===== Price cleaned =====")
print(f"Free apps: {(df['Price'] == 0).sum()}")
print(f"Paid apps: {(df['Price'] > 0).sum()}")
print(f"Most expensive app price: ${df['Price'].max()}")

# top 5 most expensive apps
top_expensive = df.nlargest(5, 'Price')[['App', 'Category', 'Price']]

# Print without special characters to avoid the Unicode error
print("\nTop 5 most expensive apps:")
for idx, row in top_expensive.iterrows():
    # Remove any special Unicode characters that might cause display issues
    app_name = row['App'].encode('ascii', 'ignore').decode('ascii')
    print(f"{app_name} - {row['Category']} - ${row['Price']}")


def convert_size_to_mb(size):
    """Convert Play Store size strings to numeric MB."""
    size = str(size).strip()
    if 'Varies with device' in size or size == 'nan':
        return np.nan
    if size.endswith('M'):
        return float(size[:-1])
    if size.endswith('k'):
        return float(size[:-1]) / 1024      # kilobytes → MB
    if size.endswith('G'):
        return float(size[:-1]) * 1024      # gigabytes → MB
    try:
        return float(size)
    except:
        return np.nan

df['Size_MB'] = df['Size'].apply(convert_size_to_mb)

print("===== Size converted to MB =====")
print(df['Size_MB'].describe())
print(f"\n'Varies with device' entries kept as NaN: {df['Size_MB'].isnull().sum()}")

df['Last_Updated_Date'] = pd.to_datetime(df['Last Updated'], errors='coerce')


# Days since last update (using dataset : Aug 2018)
snapshot_date = pd.to_datetime('2018-08-08')
df['Days_Since_Update'] = (snapshot_date - df['Last_Updated_Date']).dt.days

# Business flag: is the app abandoned? (no update in 2+ years)
df['Is_Stale'] = np.where(df['Days_Since_Update'] > 730, 1, 0)

print("===== Update freshness created =====")
print(df[['App', 'Last_Updated_Date', 'Days_Since_Update', 'Is_Stale']].head())
print(f"\nStale apps (not updated in 2+ years): {df['Is_Stale'].sum()}")
print(f"Percentage of catalogue that is stale: {df['Is_Stale'].mean()*100:.1f}%")


# I Review per install = how engaged users are
df['Engagement_Rate'] = (df['Reviews'] / df['Installs']) * 100

print("===== Engagement Rate created =====")
print(df['Engagement_Rate'].describe())

print("\nTop 10 most engaged apps (reviews per 100 installs):")
print(df.nlargest(10, 'Engagement_Rate')[['App', 'Category', 'Rating', 'Installs', 'Reviews', 'Engagement_Rate']])

print("===== FINAL CLEAN DATASET =====")
print(f"Shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print("\nData types:")
print(df.dtypes)
print("\nRemaining missing values (intentionally kept):")
print(df.isnull().sum())

# Save the clean dataset
output_path = r'C:\google_play_analytics_project\data\googleplaystore_clean.csv'
df.to_csv(output_path, index=False)
print(f"\n SAVED: {output_path}")

# ===============================================================
# SQL ANALYSIS WITH SQLITE
# PURPOSE: Use SQL to answer business questions about the data
# ===============================================================

import sqlite3

print("\n" + "=" * 50)
print(" SQL ANALYSIS WITH SQLITE")
print("=" * 50)

# Load CLEANED dataframe
df_clean = pd.read_csv(r'C:\google_play_analytics_project\data\googleplaystore_clean.csv')

# Connect to a new database file (this will create it in your project folder)
conn = sqlite3.connect(r'C:\google_play_analytics_project\sql\google_play_apps.db')

# Convert the dataframe to a SQL table named 'apps'
df_clean.to_sql("apps", conn, if_exists="replace", index=False)

print("Database and table created successfully!")

# Question 1: Which categories have the highest number of apps?
query1 = """
SELECT 
    Category,
    COUNT(*) AS app_count,
    ROUND(AVG(Rating), 2) AS avg_rating,
    ROUND(AVG(Engagement_Rate), 4) AS avg_engagement_rate
FROM apps
GROUP BY Category
ORDER BY app_count DESC
LIMIT 10;
"""
result1 = pd.read_sql_query(query1, conn)
print("\nTop 10 Categories by App Count:")
print(result1)

# Question 2: Find 'Hidden Gems' (High Rating, Low Installs)
query2 = """
SELECT 
    App,
    Category,
    Rating,
    Installs,
    Reviews,
    Engagement_Rate
FROM apps
WHERE Rating >= 4.5 AND Installs < 50000
ORDER BY Rating DESC, Engagement_Rate DESC
LIMIT 10;
"""
result2 = pd.read_sql_query(query2, conn)
print("\nTop 10 'Hidden Gem' Apps:")
print(result2)

# Question 3: Compare paid vs free apps
query3 = """
SELECT 
    CASE WHEN Is_Paid = 1 THEN 'Paid' ELSE 'Free' END AS app_type,
    COUNT(*) AS count,
    ROUND(AVG(Rating), 2) AS avg_rating,
    ROUND(AVG(Engagement_Rate), 4) AS avg_engagement_rate,
    ROUND(AVG(Size_MB), 2) AS avg_size_mb
FROM apps
GROUP BY Is_Paid
ORDER BY count DESC;
"""
result3 = pd.read_sql_query(query3, conn)
print("\nPaid vs Free Apps Comparison:")
print(result3)

# Question 4: Find stale apps with high ratings (potential for revival)
query4 = """
SELECT 
    App,
    Category,
    Rating,
    Installs,
    Days_Since_Update
FROM apps
WHERE Is_Stale = 1 AND Rating >= 4.0
ORDER BY Rating DESC, Days_Since_Update DESC
LIMIT 10;
"""
result4 = pd.read_sql_query(query4, conn)
print("\nHigh-Rated Stale Apps (Potential for Revival):")
print(result4)

# Question 5: Categories with highest engagement rates
query5 = """
SELECT 
    Category,
    COUNT(*) AS app_count,
    ROUND(AVG(Engagement_Rate), 4) AS avg_engagement_rate,
    ROUND(AVG(Rating), 2) AS avg_rating
FROM apps
WHERE Installs >= 10000  -- Filter out apps with very few installs
GROUP BY Category
HAVING app_count >= 30  -- Only include categories with enough apps
ORDER BY avg_engagement_rate DESC
LIMIT 10;
"""
result5 = pd.read_sql_query(query5, conn)
print("\nCategories with Highest Engagement Rates:")
print(result5)

# Save all query results to CSV files
result1.to_csv(r'C:\google_play_analytics_project\final_assets\top_categories.csv', index=False)
result2.to_csv(r'C:\google_play_analytics_project\final_assets\hidden_gems.csv', index=False)
result3.to_csv(r'C:\google_play_analytics_project\final_assets\paid_vs_free.csv', index=False)
result4.to_csv(r'C:\google_play_analytics_project\final_assets\stale_apps.csv', index=False)
result5.to_csv(r'C:\google_play_analytics_project\final_assets\engagement_by_category.csv', index=False)

conn.close()



# ============================================================
# CREATE VISUALIZATIONS IN PYTHON
# PURPOSE: Create charts to visualize our key findings
# ============================================================


print("\n" + "=" * 50)
print("CREATING VISUALIZATIONS")
print("=" * 50)

# Set a style for the plots
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12})

# Load query results from the CSV files 
top_categories = pd.read_csv(r'C:\google_play_analytics_project\final_assets\top_categories.csv')
hidden_gems = pd.read_csv(r'C:\google_play_analytics_project\final_assets\hidden_gems.csv')
paid_vs_free = pd.read_csv(r'C:\google_play_analytics_project\final_assets\paid_vs_free.csv')
engagement_by_category = pd.read_csv(r'C:\google_play_analytics_project\final_assets\engagement_by_category.csv')

# Load the clean dataset for additional visualizations
df_clean = pd.read_csv(r'C:\google_play_analytics_project\data\googleplaystore_clean.csv')


# Chart 1: Top Categories by App Count

plt.figure(figsize=(14, 8))
ax = sns.barplot(x='app_count', y='Category', data=top_categories, palette='viridis')
plt.title('Top 10 App Categories on Google Play Store', fontsize=16, fontweight='bold')
plt.xlabel('Number of Apps', fontsize=14)
plt.ylabel('Category', fontsize=14)

# Add the average rating as text on each bar
for i, (count, rating) in enumerate(zip(top_categories['app_count'], top_categories['avg_rating'])):
    ax.text(count + 20, i, f'★ {rating}', va='center', fontsize=11)

plt.tight_layout()
plt.savefig(r'C:\google_play_analytics_project\final_assets\top_categories_chart.png', dpi=300, bbox_inches='tight')
plt.show()


# Chart 2: Rating Distribution
plt.figure(figsize=(12, 6))
sns.histplot(df_clean['Rating'], bins=20, kde=True, color='skyblue')
plt.title('Distribution of App Ratings', fontsize=16, fontweight='bold')
plt.xlabel('Rating', fontsize=14)
plt.ylabel('Number of Apps', fontsize=14)
plt.axvline(df_clean['Rating'].mean(), color='red', linestyle='--', 
            label=f'Mean: {df_clean["Rating"].mean():.2f}')
plt.legend()
plt.tight_layout()
plt.savefig(r'C:\google_play_analytics_project\final_assets\rating_distribution_chart.png', dpi=300, bbox_inches='tight')
plt.show()

# Chart 3: Paid vs Free Apps Comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Subplot 1: Count of Paid vs Free
sns.barplot(x='app_type', y='count', data=paid_vs_free, ax=ax1, palette=['lightgreen', 'lightcoral'])
ax1.set_title('Number of Paid vs Free Apps', fontsize=14, fontweight='bold')
ax1.set_xlabel('App Type', fontsize=12)
ax1.set_ylabel('Count', fontsize=12)

# Added count labels on bars
for i, count in enumerate(paid_vs_free['count']):
    ax1.text(i, count + 50, str(count), ha='center', fontsize=12)

# Subplot 2: Average Rating by App Type
sns.barplot(x='app_type', y='avg_rating', data=paid_vs_free, ax=ax2, palette=['lightgreen', 'lightcoral'])
ax2.set_title('Average Rating by App Type', fontsize=14, fontweight='bold')
ax2.set_xlabel('App Type', fontsize=12)
ax2.set_ylabel('Average Rating', fontsize=12)
ax2.set_ylim(3.5, 4.5)  

for i, rating in enumerate(paid_vs_free['avg_rating']):
    ax2.text(i, rating + 0.02, f'{rating}', ha='center', fontsize=12)

plt.tight_layout()
plt.savefig(r'C:\google_play_analytics_project\final_assets\paid_vs_free_chart.png', dpi=300, bbox_inches='tight')
plt.show()


# Chart 4: Categories with Highest Engagement Rates
plt.figure(figsize=(14, 8))
ax = sns.barplot(x='avg_engagement_rate', y='Category', data=engagement_by_category, palette='plasma')
plt.title('Categories with Highest User Engagement Rates', fontsize=16, fontweight='bold')
plt.xlabel('Average Engagement Rate (%)', fontsize=14)
plt.ylabel('Category', fontsize=14)

# Format x-axis to show percentages
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))

plt.tight_layout()
plt.savefig(r'C:\google_play_analytics_project\final_assets\engagement_by_category_chart.png', dpi=300, bbox_inches='tight')
plt.show()

# Chart 5: App Size Distribution
plt.figure(figsize=(12, 6))
size_data = df_clean[df_clean['Size_MB'].notna()]  # Exclude NaN values
sns.histplot(size_data['Size_MB'], bins=30, kde=True, color='orchid')
plt.title('Distribution of App Sizes (in MB)', fontsize=16, fontweight='bold')
plt.xlabel('Size (MB)', fontsize=14)
plt.ylabel('Number of Apps', fontsize=14)
plt.axvline(size_data['Size_MB'].median(), color='red', linestyle='--', 
            label=f'Median: {size_data["Size_MB"].median():.1f} MB')
plt.legend()
plt.tight_layout()
plt.savefig(r'C:\google_play_analytics_project\final_assets\size_distribution_chart.png', dpi=300, bbox_inches='tight')
plt.show()




