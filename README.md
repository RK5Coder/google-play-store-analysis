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
```
google-play-store-analysis/
├── data/
│   └── googleplaystore_clean.csv
├── notebooks/
│   └── data_analysis.py
├── final_assets/
│   ├── engagement_by_category_chart.png
│   ├── paid_vs_free_chart.png
│   ├── rating_distribution_chart.png
│   ├── size_distribution_chart.png
│   ├── top_categories_chart.png
│   ├── Google Play Store Growth Intelligence Report.pdf
│   └── google_play_dashboard.xlsx
└── README.md
```

## How to Run This Analysis
1. Clone this repository to your local machine
2. Install required packages: pandas, numpy, matplotlib, seaborn, sqlite3
3. Run the data_analysis.py file in the notebooks folder
4. View the generated charts and report in the final_assets folder

## Files Included
- `data/googleplaystore_clean.csv` - Cleaned dataset after preprocessing
- `notebooks/data_analysis.py` - Complete Python analysis code
- `final_assets/google_play_dashboard.xlsx` - Complete dashboard with data, KPIs, charts, and hidden gems
- `final_assets/` - All generated charts and final report

## Insights and Recommendations
Based on my analysis, I recommend:
1. Creating a "Hidden Gems" section in the Play Store to highlight high-quality, low-install apps
2. Implementing a "Revitalization Program" for high-rated apps that haven't been updated in over 2 years
3. Providing development grants for underserved categories with high engagement rates

## Contact
Ravi Khunt  
LinkedIn - https://www.linkedin.com/in/ravi-khunt01/

## Acknowledgment
Dataset provided by Kaggle user lava18
