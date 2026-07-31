# Google Play Store Growth Intelligence Analysis

## Project Overview
This project analyzes Google Play Store app data to identify growth opportunities and user engagement patterns. I examined 8,196 apps across multiple categories to discover hidden gems with high ratings but low installs, category performance insights, and opportunities for app revitalization.

## Why This Project Matters
The Google Play Store contains millions of apps, but quality doesn't always correlate with visibility. This analysis reveals opportunities to improve app discovery and user satisfaction by focusing on under-promoted high-quality apps and categories with high engagement rates.

## Key Findings
- Identified 10 "hidden gem" apps with 4.5+ ratings but under 50,000 installs
- Discovered that 15.2% of apps haven't been updated in over 2 years
- Found that EDUCATION and TOOLS categories have higher engagement rates despite fewer apps
- Analyzed differences between paid and free apps (only 7.3% are paid but have slightly higher ratings)

## Technical Skills Demonstrated
- Data cleaning and preprocessing with Python (pandas, numpy)
- SQL database creation and querying with SQLite
- Data visualization with matplotlib and seaborn
- Business intelligence and reporting
- Anomaly detection and handling
- Dashboard creation in Google Sheets

## Project Structure
Google_Play_Analytics_Project/
├── data/ # Raw and cleaned datasets
├── notebooks/ # Python analysis code
├── sql/ # Database files
└── final_assets/ # Charts, CSV files, and report backups

## How to Run This Analysis
1. Clone this repository to your local machine
2. Install required packages: pandas, numpy, matplotlib, seaborn, sqlite3
3. Run the data_analysis.py file in the notebooks folder
4. View the generated charts and CSV files in the final_assets folder
5. Open google_play_analytics_project.xlsx to see the complete analysis dashboard

## Files Included
- `data/googleplaystore.csv` - Raw dataset from Kaggle
- `data/googleplaystore_clean.csv` - Cleaned dataset after preprocessing
- `notebooks/data_analysis.py` - Complete Python analysis code
- `sql/google_play_apps.db` - SQLite database with cleaned data
- `final_assets/` - All generated charts, CSV files, and reports

## Insights and Recommendations
Based on my analysis, I recommend:
1. Creating a "Hidden Gems" section in the Play Store to highlight high-quality, low-install apps
2. Implementing a "Revitalization Program" for high-rated apps that haven't been updated in over 2 years
3. Providing development grants for underserved categories with high engagement rates

## Contact
Ravi Khunt  
LinkedIn - https://www.linkedin.com/in/ravi-khunt01/

## Acknowledgment
- Dataset provided by Kaggle user lava18
