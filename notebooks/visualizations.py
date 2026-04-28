import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
sns.set(style="whitegrid")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
clean_data_path = os.path.join(BASE_DIR, "..", "clean_data")

years = list(range(2005, 2026))
dfs = []

for year in years:
    file_path = os.path.join(
        clean_data_path,
        f"boxoffice_{year}_clean.csv"
    )
    if os.path.exists(file_path):
        dfs.append(pd.read_csv(file_path))

master_df = pd.concat(dfs, ignore_index=True)

#Opening vs Lifetime Gross
plt.figure(figsize=(8,6))

sns.regplot(
    x="opening_gross",
    y="domestic_lifetime_gross",
    data=master_df,
    scatter_kws={"alpha":0.4},
    line_kws={"color":"red"}
)

plt.title("Opening Gross vs Lifetime Gross")
plt.xlabel("Opening Gross")
plt.ylabel("Domestic Lifetime Gross")
plt.tight_layout()
plt.show()

#budget vs lifetime
plt.figure(figsize=(8,6))

sns.regplot(
    x="budget",
    y="domestic_lifetime_gross",
    data=master_df,
    scatter_kws={"alpha":0.4},
    line_kws={"color":"green"}
)

plt.title("Budget vs Lifetime Gross")
plt.xlabel("Budget")
plt.ylabel("Domestic Lifetime Gross")
plt.tight_layout()
plt.show()

#mpaa vs avg revenue
plt.figure(figsize=(8,6))

sns.barplot(
    x="mpaa_rating",
    y="domestic_lifetime_gross",
    data=master_df,
    estimator="mean"
)

plt.title("Average Lifetime Gross by MPAA Rating")
plt.xlabel("MPAA Rating")
plt.ylabel("Average Lifetime Gross")
plt.tight_layout()
plt.show()

#release month vs revenue (seasonability)
plt.figure(figsize=(10,6))

sns.barplot(
    x="release_month",
    y="domestic_lifetime_gross",
    data=master_df,
    estimator="mean"
)

plt.title("Average Revenue by Release Month")
plt.xlabel("Release Month")
plt.ylabel("Average Lifetime Gross")
plt.tight_layout()
plt.show()

#yearly revenue
# ----------------------------
# YEARLY REVENUE
# ----------------------------

# Create yearly average dataframe
year_avg = master_df.groupby("release_year")["domestic_lifetime_gross"].mean().reset_index()

plt.figure(figsize=(8,6))
plt.plot(year_avg["release_year"], year_avg["domestic_lifetime_gross"])

plt.title("Average Domestic Revenue Over Years")
plt.xlabel("Year")
plt.ylabel("Average Revenue")

import numpy as np
plt.xticks(np.arange(2005, 2026, 1))

plt.show()

#budget vs legs ratio
# Ensure numeric
master_df["opening_gross"] = pd.to_numeric(master_df["opening_gross"], errors="coerce")
master_df["domestic_lifetime_gross"] = pd.to_numeric(master_df["domestic_lifetime_gross"], errors="coerce")

# Remove bad rows
master_df = master_df[
    (master_df["opening_gross"] > 100000) &   # remove tiny openings
    (master_df["budget"] > 0) &
    (master_df["domestic_lifetime_gross"] > 0)
]

# Calculate legs ratio
master_df["legs_ratio"] = (
    master_df["domestic_lifetime_gross"] /
    master_df["opening_gross"]
)

# Remove insane outliers
master_df = master_df[master_df["legs_ratio"] < 10]

master_df["legs_ratio"] = master_df["legs_ratio"].round(2)
plt.figure(figsize=(8,6))
sns.scatterplot(
    x="budget",
    y="legs_ratio",
    data=master_df,
    alpha=0.6
)

plt.title("Budget vs Legs Ratio")
plt.xlabel("Budget")
plt.ylabel("Legs Ratio")
plt.show()


# Select only numeric columns
numeric_df = master_df.select_dtypes(include=['float64', 'int64'])

# Optional: remove very large irrelevant columns
numeric_df = numeric_df[
    [
        "opening_gross",
        "domestic_lifetime_gross",
        "budget",
        "legs_ratio",
        "widest_theaters",
        "release_month",
        "release_year"
    ]
]

corr_matrix = numeric_df.corr()

plt.figure(figsize=(12, 9))

varanasi_colors = [
    "#0b1d2a",  # deep night blue
    "#1f3b4d",  # temple shadow blue
    "#5a7d7c",  # muted teal
    "#f4a261",  # saffron
    "#f77f00",  # temple orange
    "#ffd166"   # golden sunlight
]

varanasi_cmap = LinearSegmentedColormap.from_list("varanasi", varanasi_colors)

plt.figure(figsize=(10,8))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap=varanasi_cmap,
    linewidths=0.5,
    fmt=".2f"
)

plt.title("Correlation Heatmap of Box Office Features", fontsize=16)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()

plt.show()