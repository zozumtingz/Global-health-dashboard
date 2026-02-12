
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

#Automated File Discovery. Avoid FileNotFoundError
files = os.listdir()
try:
    smoke_file = [f for f in files if "tobacco" in f.lower() and (f.endswith('.csv') or f.endswith('.xlsx'))][0]
    life_file = [f for f in files if "health_data" in f.lower() and f.endswith('.csv')][0]
    print(f"File status: Found {smoke_file} and {life_file}")
except IndexError:
    print("Error: Required data files not found in the current directory.")
    exit()

# Acquisition Function 
def load_dataset(file_path):
    #CSV XLSX Encoding
    if file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    try:
        return pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        # Encoding error -> latin1 
        return pd.read_csv(file_path, encoding='latin1')

# Preprocessing 
df_smoke = load_dataset(smoke_file)
df_life = load_dataset(life_file)

df_smoke.columns = df_smoke.columns.str.strip()
df_life.columns = df_life.columns.str.strip()

# Data Cleaning:
df_smoke['FactValueNumeric'] = pd.to_numeric(df_smoke['FactValueNumeric'], errors='coerce')
df_smoke = df_smoke.dropna(subset=['FactValueNumeric'])

# Aggregation
smoking_avg = df_smoke.groupby("SpatialDimValueCode")["FactValueNumeric"].mean().reset_index()
smoking_avg.columns = ["CountryCode", "SmokingRate"]

# Transformation & Merging 
# Dictionary for Maping country name into ISO Country Code
country_mapping = {
    "USA": "USA", "UK": "GBR", "Thailand": "THA", 
    "Japan": "JPN", "Germany": "DEU", "Australia": "AUS", 
    "India": "IND", "Brazil": "BRA"
}
df_life["CountryCode"] = df_life["Country"].map(country_mapping)

# Dataset
merged_data = pd.merge(smoking_avg, df_life, on="CountryCode", how="inner")

# Visualization
if not merged_data.empty:
    plt.figure(figsize=(10, 6))
    
    x_val = merged_data["SmokingRate"]
    y_val = merged_data["Life_Expectancy"]
    
    # Scatter Plot
    plt.scatter(x_val, y_val, s=100, color='#1f77b4', edgecolors='black', alpha=0.7)
    
    # Label country into Data Point
    for i in range(len(merged_data)):
        plt.annotate(merged_data["Country"].iloc[i], 
                     (x_val.iloc[i], y_val.iloc[i]),
                     xytext=(8, 5), textcoords='offset points', fontsize=10)

    # Linear Regression Line
    correlation = x_val.corr(y_val)
    m, b = np.polyfit(x_val, y_val, 1)
    plt.plot(x_val, m*x_val + b, color='#d62728', linestyle='--', linewidth=2, label=f'Linear Fit (r={correlation:.2f})')

    # Graph
    plt.title("Correlation: Smoking Prevalence vs Life Expectancy", fontsize=14)
    plt.xlabel("Smoking Prevalence (%)", fontsize=12)
    plt.ylabel("Life Expectancy (Years)", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    
    plt.show()
    print("Process completed: Visualization generated successfully.")
else:

    print("Warning: No matching data found during the merge process.")
