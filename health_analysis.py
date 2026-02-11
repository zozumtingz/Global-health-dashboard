

#import pandas as pd

#df = pd.read_excel("tobacco_prevalence.xlsx")

#print(df.columns.tolist())

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("tobacco_prevalence.xlsx", header=0)

df.columns = df.columns.str.strip()

print(df.columns.tolist())

smoking = df[
    df["IndicatorCode"].str.contains("TOBACCO", case=False, na=False)
]

print(smoking.shape)

yearly_avg = smoking.groupby("Year")["FactValueNumeric"].mean()

print(smoking["Year"].unique())

plt.scatter(
    smoking["Year"],
    smoking["FactValueNumeric"]
)

plt.show()

""""

life = pd.read_csv("health_data.csv")

life.columns = life.columns.str.strip()

print(life.columns.tolist())

life_exp = life[[
    "Country",
    "Life_Expectancy"
]]

life_exp = life_exp.rename(
    columns={
        "Country": "ParentLocation",
        "Life_Expectancy": "LifeExpectancy"
    }
)

smoking_df = smoking[[
    "ParentLocation",
    "Year",
    "FactValueNumeric"
]]

smoking_df = smoking_df.rename(
    columns={
        "FactValueNumeric": "SmokingRate"
    }
)

merged = pd.merge(
    smoking_df,
    life_exp,
    on=["ParentLocation", "Year"],
    how="inner"
)

country_avg = merged.groupby("ParentLocation").mean(numeric_only=True)

print(country_avg.head())
print(country_avg.shape)

plt.figure(figsize=(10,6))

plt.scatter(
    country_avg["SmokingRate"],
    country_avg["LifeExpectancy"]
)

plt.xlabel("Smoking Prevalence (%)")
plt.ylabel("Life Expectancy (Years)")
plt.title("Smoking vs Life Expectancy (Country Average)")

corr = country_avg["SmokingRate"].corr(
    country_avg["LifeExpectancy"]
)

print("Correlation:", corr)

plt.text(
    country_avg["SmokingRate"].min(),
    country_avg["LifeExpectancy"].max(),
    f"r = {corr:.2f}"
)

import numpy as np

x = country_avg["SmokingRate"]
y = country_avg["LifeExpectancy"]

m, b = np.polyfit(x, y, 1)

plt.plot(x, m*x + b)

plt.show()

#---------------------

# ---------- LIFE EXPECTANCY ----------
life = pd.read_csv("health_data.csv")
life.columns = life.columns.str.strip()

print(life.columns.tolist())

life_exp = life[[
    "Country",
    "Life_Expectancy"
]]

life_exp = life_exp.rename(columns={
    "Country": "ParentLocation",
    "Life_Expectancy": "LifeExpectancy"
})

# ---------- SMOKING ----------
smoking_df = smoking[[
    "ParentLocation",
    "FactValueNumeric"
]]

smoking_df = smoking_df.rename(columns={
    "FactValueNumeric": "SmokingRate"
})

smoking_avg = smoking_df.groupby("ParentLocation").mean().reset_index()

merged = pd.merge(
    smoking_avg,
    life_exp,
    on="ParentLocation",
    how="inner"
)

print(merged.shape)
print(merged.head())

# SCATTER 
plt.figure(figsize=(10,6))

plt.scatter(
    merged["SmokingRate"],
    merged["LifeExpectancy"]
)

plt.xlabel("Smoking Prevalence (%)")
plt.ylabel("Life Expectancy (Years)")
plt.title("Smoking vs Life Expectancy")

# correlation
corr = merged["SmokingRate"].corr(
    merged["LifeExpectancy"]
)

print("Correlation:", corr)

plt.text(
    merged["SmokingRate"].min(),
    merged["LifeExpectancy"].max(),
    f"r = {corr:.2f}"
)

# regression line
import numpy as np

x = merged["SmokingRate"]
y = merged["LifeExpectancy"]

m, b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b)

plt.show()

"""

"""
------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_excel("tobacco_prevalence.xlsx", header=0)
#df = pd.read_csv("health_data.csv")

df.columns = df.columns.str.strip()

print("Smoking columns:")
print(df.columns.tolist())


# FILTER TOBACCO DATA
smoking = df[
    df["IndicatorCode"].str.contains(
        "TOBACCO",
        case=False,
        na=False
    )
]

print("Smoking shape:", smoking.shape)

# SELECT COLUMNS
smoking_df = smoking[[
    "ParentLocation",
    "FactValueNumeric"
]]

smoking_df = smoking_df.rename(columns={
    "FactValueNumeric": "SmokingRate"
})


# AVERAGE SMOKING BY COUNTRY
smoking_avg = (
    smoking_df
    .groupby("ParentLocation")
    .mean()
    .reset_index()
)

print("Smoking avg shape:", smoking_avg.shape)


# LOAD LIFE EXPECTANCY
life = pd.read_csv("health_data.csv")

life.columns = life.columns.str.strip()

print("\nLife columns:")
print(life.columns.tolist())


# SELECT LIFE EXPECTANCY
life_exp = life[[
    "Country",
    "Life_Expectancy"
]]

life_exp = life_exp.rename(columns={
    "Country": "ParentLocation",
    "Life_Expectancy": "LifeExpectancy"
})


print("Life shape:", life_exp.shape)

# MERGE DATA
merged = pd.merge(
    smoking_avg,
    life_exp,
    on="ParentLocation",
    how="inner"
)

print(merged.shape)
print(merged.head())


# SCATTER PLOT
plt.figure(figsize=(10,6))

plt.scatter(
    merged["SmokingRate"],
    merged["LifeExpectancy"]
)

corr = merged["SmokingRate"].corr(
    merged["LifeExpectancy"]
)

print("Correlation:", corr)

plt.text(
    merged["SmokingRate"].min(),
    merged["LifeExpectancy"].max(),
    f"r = {corr:.2f}"
)

x = merged["SmokingRate"]
y = merged["LifeExpectancy"]

m, b = np.polyfit(x, y, 1)

plt.plot(x, m*x + b)

plt.xlabel("Smoking Prevalence (%)")
plt.ylabel("Life Expectancy (Years)")
plt.title("Smoking vs Life Expectancy")

plt.show()

------------------------------------------------------

plt.xlabel("Smoking Prevalence (%)")
plt.ylabel("Life Expectancy (Years)")
plt.title("Smoking vs Life Expectancy")


# CORRELATION
corr = merged["SmokingRate"].corr(
    merged["LifeExpectancy"]
)

print("\nCorrelation:", corr)

plt.text(
    merged["SmokingRate"].min(),
    merged["LifeExpectancy"].max(),
    f"r = {corr:.2f}"
)

x = df["SmokingRate"]
y = df["LifeExpectancy"]


m, b = np.polyfit(x, y, 1)

plt.plot(x, m*x + b)

plt.show()


------------------------------------------------------------
# =========================
# STEP 0 — IMPORT
# =========================

import os

print(os.listdir())

import pandas as pd

smoking = pd.read_excel("tobacco_prevalence.xlsx")
life = pd.read_csv("health_data.csv")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# STEP 1 — LOAD SMOKING DATA

df = pd.read_excel("tobacco_prevalence.xlsx", header=0)

# ลบช่องว่างชื่อคอลัมน์
df.columns = df.columns.str.strip()

print("Smoking columns:")
print(df.columns.tolist())


# STEP 2 — FILTER TOBACCO
smoking = df[
    df["IndicatorCode"].str.contains(
        "TOBACCO",
        case=False,
        na=False
    )
]

print("Smoking shape:", smoking.shape)


# STEP 3 — SELECT + RENAME
smoking_df = smoking[[
    "ParentLocation",      # ← ใช้ชื่อนี้ ไม่ใช่ ParentLocation (ถ้า error ให้ print columns ดู)
    "FactValueNumeric"
]]

smoking_df = smoking_df.rename(columns={
    "FactValueNumeric": "SmokingRate"
})


# STEP 4 — AVERAGE BY COUNTRY
smoking_avg = (
    smoking_df
    .groupby("ParentLocation")
    .mean()
    .reset_index()
)

print("Smoking avg shape:", smoking_avg.shape)


# STEP 5 — LOAD LIFE EXPECTANCY
life = pd.read_csv("health_data.csv")

life.columns = life.columns.str.strip()

print("\nLife columns:")
print(life.columns.tolist())


# STEP 6 — SELECT + RENAME LIFE
life_exp = life[[
    "Country",
    "Life_Expectancy"
]]

life_exp = life_exp.rename(columns={
    "Country": "ParentLocation",
    "Life_Expectancy": "LifeExpectancy"
})

print("Life shape:", life_exp.shape)


# STEP 7 — MERGE DATA
merged = pd.merge(
    smoking_avg,
    life_exp,
    on="ParentLocation",
    how="inner"
)

print("\nMerged shape:", merged.shape)
print(merged.head())


# STEP 8 — SCATTER PLOT
plt.figure(figsize=(10,6))

plt.scatter(
    merged["SmokingRate"],
    merged["LifeExpectancy"]
)


# STEP 9 — CORRELATION
corr = merged["SmokingRate"].corr(
    merged["LifeExpectancy"]
)

print("\nCorrelation:", corr)

plt.text(
    merged["SmokingRate"].min(),
    merged["LifeExpectancy"].max(),
    f"r = {corr:.2f}"
)



# STEP 10 — REGRESSION LINE
x = merged["SmokingRate"]
y = merged["LifeExpectancy"]

m, b = np.polyfit(x, y, 1)

plt.plot(x, m*x + b)


# STEP 11 — LABEL
plt.xlabel("Smoking Prevalence (%)")
plt.ylabel("Life Expectancy (Years)")
plt.title("Smoking vs Life Expectancy")

plt.show()

"""
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