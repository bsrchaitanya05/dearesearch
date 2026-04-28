import os
import pandas as pd

# --------------------------------------------------
# PATH SETUP
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

bo_path = os.path.join(
    BASE_DIR,
    "..",
    "raw_data",
    "boxoffice_mojo",
    "2019",
    "boxoffice_2019_raw.csv"
)

bud_path = os.path.join(
    BASE_DIR,
    "..",
    "raw_data",
    "boxoffice_mojo",
    "2019",
    "bud_mpaa19.csv"
)

open_path = os.path.join(
    BASE_DIR,
    "..",
    "raw_data",
    "boxoffice_mojo",
    "2019",
    "opening.csv"
)

open_df = pd.read_csv(open_path)


clean_path = os.path.join(
    BASE_DIR,
    "..",
    "clean_data",
    "boxoffice_2019_clean.csv"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = pd.read_csv(bo_path, encoding="latin1", engine="python")
bud_df = pd.read_csv(bud_path)

# --------------------------------------------------
# RENAME RAW COLUMNS (Box Office Mojo → clean names)
# --------------------------------------------------
df = df.rename(columns={
    "Release": "movie_title",
    "Gross": "early_gross",
    "Total Gross": "domestic_lifetime_gross",
    "Theaters": "widest_theaters",
    "Distributor": "distributor",
    "Release Date": "release_date"
})

# --------------------------------------------------
# CLEAN CURRENCY COLUMNS
# --------------------------------------------------
for col in ["early_gross", "domestic_lifetime_gross"]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --------------------------------------------------
# CLEAN THEATERS
# --------------------------------------------------
df["widest_theaters"] = (
    df["widest_theaters"]
    .astype(str)
    .str.replace(",", "", regex=False)
)
df["widest_theaters"] = pd.to_numeric(df["widest_theaters"], errors="coerce")

#clean opening
# Standardize titles
open_df["movie_title_clean"] = (
    open_df["movie_title"]
    .str.lower()
    .str.strip()
)

# Clean opening gross
open_df["opening_gross"] = (
    open_df["opening_gross"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

open_df["opening_gross"] = pd.to_numeric(
    open_df["opening_gross"], errors="coerce"
)

# Clean opening share %
open_df["opening_share_pct"] = (
    open_df["opening_share_pct"]
    .astype(str)
    .str.replace("%", "", regex=False)
)

open_df["opening_share_pct"] = pd.to_numeric(
    open_df["opening_share_pct"], errors="coerce"
)


# --------------------------------------------------
# ADD YEAR + MONTH
# --------------------------------------------------
df["release_year"] = 2019

month_map = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

df["release_month"] = (
    df["release_date"]
    .astype(str)
    .str[:3]
    .map(month_map)
)

# --------------------------------------------------
# STANDARDIZE TITLES FOR MERGE
# --------------------------------------------------
df["movie_title_clean"] = df["movie_title"].str.lower().str.strip()
bud_df["movie_title_clean"] = bud_df["movie_title"].str.lower().str.strip()

# --------------------------------------------------
# CLEAN BUDGET
# --------------------------------------------------
bud_df["budget"] = pd.to_numeric(bud_df["budget"], errors="coerce")

# --------------------------------------------------
# MERGE BUDGET + MPAA
# --------------------------------------------------

df["movie_title_clean"] = (
    df["movie_title"]
    .str.lower()
    .str.strip()
)


df = df.merge(
    bud_df[["movie_title_clean", "budget", "mpaa_rating"]],
    on="movie_title_clean",
    how="left"
)

open_df["movie_title_clean"] = (
    open_df["movie_title"]
    .str.lower()
    .str.strip()
)

open_df["opening_gross"] = (
    open_df["opening_gross"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)
open_df["opening_gross"] = pd.to_numeric(open_df["opening_gross"], errors="coerce")

open_df["opening_share_pct"] = (
    open_df["opening_share_pct"]
    .astype(str)
    .str.replace("%", "", regex=False)
)
open_df["opening_share_pct"] = pd.to_numeric(open_df["opening_share_pct"], errors="coerce")

df = df.merge(
    open_df[
        ["movie_title_clean", "opening_gross", "opening_share_pct"]
    ],
    on="movie_title_clean",
    how="left"
)

df["legs_ratio"] = df["domestic_lifetime_gross"] / df["opening_gross"]
df["legs_ratio"] = df["legs_ratio"].round(2)


# --------------------------------------------------
# CLEAN DISTRIBUTOR
# --------------------------------------------------
df["distributor"] = (
    df["distributor"]
    .astype(str)
    .str.strip()
    .str.replace(".", "", regex=False)
)

# --------------------------------------------------
# FINAL CLEAN DATASET (NO OPENING / NO LEGS)
# --------------------------------------------------
df_clean = df[
    [
        "movie_title",
        "release_year",
        "release_month",
        "opening_gross",
        "domestic_lifetime_gross",
        "legs_ratio",
        "budget",
        "mpaa_rating",
        "widest_theaters",
        "distributor"
    ]
]


# --------------------------------------------------
# SAVE
# --------------------------------------------------
df_clean.to_csv(clean_path, index=False)

# --------------------------------------------------
# SANITY CHECK
# --------------------------------------------------
print(df_clean.head(10))
print("\nMPAA ratings:", df_clean["mpaa_rating"].unique())
print("\nTop distributors:", df_clean["distributor"].value_counts().head())
