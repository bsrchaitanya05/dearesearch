import os
import pandas as pd

# --------------------------------------------------
# PATH SETUP
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

clean_data_path = os.path.join(BASE_DIR, "..", "clean_data")

# --------------------------------------------------
# LOAD ALL YEARS
# --------------------------------------------------
years = list(range(2005, 2026))

dfs = []

for year in years:
    file_path = os.path.join(
        clean_data_path,
        f"boxoffice_{year}_clean.csv"
    )
    
    if os.path.exists(file_path):
        df_year = pd.read_csv(file_path)
        dfs.append(df_year)
        print(f"Loaded {year}")
    else:
        print(f"Missing file for {year}")

# --------------------------------------------------
# CONCATENATE INTO MASTER DATASET
# --------------------------------------------------
master_df = pd.concat(dfs, ignore_index=True)

print("\nMaster Dataset Shape:", master_df.shape)

print("\nColumns:")
print(master_df.columns)

# --------------------------------------------------
# REMOVE MISSING CORE VALUES
# --------------------------------------------------
master_df = master_df.dropna(
    subset=["opening_gross", "budget", "domestic_lifetime_gross"]
)

print("\nAfter dropping NA:", master_df.shape)

# --------------------------------------------------
# FINAL NA CLEAN FOR MODEL FEATURES
# --------------------------------------------------
master_df = master_df.dropna()

print("After full NA cleanup:", master_df.shape) 

# --------------------------------------------------
# ENCODE CATEGORICAL VARIABLES
# --------------------------------------------------
master_df = pd.get_dummies(
    master_df,
    columns=["mpaa_rating"],
    drop_first=True
)

print("\nColumns after encoding:")
print(master_df.columns)

# --------------------------------------------------
# DEFINE FEATURES AND TARGET
# --------------------------------------------------
features = [
    "opening_gross",
    "budget",
    "release_month"
]

# Add encoded MPAA columns
features += [col for col in master_df.columns if "mpaa_rating_" in col]

X = master_df[features]
y = master_df["domestic_lifetime_gross"]

print("\nFeature Columns:", features)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print("\nTrain shape:", X_train.shape)
print("Test shape:", X_test.shape)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\nR² Score:", r2_score(y_test, predictions))
print("Mean Absolute Error:", mean_absolute_error(y_test, predictions))