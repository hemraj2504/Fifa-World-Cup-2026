# ============================================================
# FIFA WORLD CUP 2026 - GOALKEEPING ANALYSIS
# Stage 1: Load and Inspect Raw Data
# ============================================================

# ------------------------------------------------------------
# 1. Import required libraries
# ------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

print("=" * 60)
print("FIFA WORLD CUP 2026 - GOALKEEPING ANALYSIS")
print("=" * 60)

print("\nLibraries loaded successfully.")


# ------------------------------------------------------------
# 2. Load the raw datasets
# ------------------------------------------------------------

# Goalkeeping dataset
goalkeeping = pd.read_csv(
    "C:\\Users\\bhusa\\OneDrive\\Desktop\\FIFA_Python\\data\\fbref_goalkeeping_stats_2026_raw.csv",
    header=1
)

# Match results dataset
matches = pd.read_csv(
    "C:\\Users\\bhusa\\OneDrive\\Desktop\\FIFA_Python\\data\\fbref_world_cup_2026_matches_raw.csv"
)

print("\nRaw datasets loaded successfully.")


# ------------------------------------------------------------
# 3. Create working copies
# ------------------------------------------------------------

# We never modify the original raw data directly.
goalkeeping_clean = goalkeeping.copy()
matches_clean = matches.copy()

print("Working copies created.")


# ------------------------------------------------------------
# 4. Inspect Goalkeeping dataset
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("GOALKEEPING DATASET")
print("=" * 60)

print("\nShape:")
print(goalkeeping_clean.shape)

print("\nColumns:")
print(goalkeeping_clean.columns.tolist())

print("\nFirst 10 rows:")
print(goalkeeping_clean.head(10))


# ------------------------------------------------------------
# 5. Inspect Match Results dataset
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MATCH RESULTS DATASET")
print("=" * 60)

print("\nShape:")
print(matches_clean.shape)

print("\nColumns:")
print(matches_clean.columns.tolist())

print("\nFirst 10 rows:")
print(matches_clean.head(10))


# ------------------------------------------------------------
# 6. Check missing values
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

print("\nGoalkeeping missing values:")
print(goalkeeping_clean.isna().sum())

print("\nMatch results missing values:")
print(matches_clean.isna().sum())


# ------------------------------------------------------------
# 7. Check data types
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)

print("\nGoalkeeping data types:")
print(goalkeeping_clean.dtypes)

print("\nMatch results data types:")
print(matches_clean.dtypes)


# ------------------------------------------------------------
# 8. Check the Save% variable
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("SAVE% INSPECTION")
print("=" * 60)

print("\nSave% values:")
print(goalkeeping_clean["Save%"].head(20))

print("\nSave% data type:")
print(goalkeeping_clean["Save%"].dtype)

print("\nNumber of missing Save% values:")
print(goalkeeping_clean["Save%"].isna().sum())


# ------------------------------------------------------------
# 9. Check goalkeeper team names
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("GOALKEEPER TEAM NAMES")
print("=" * 60)

print(
    goalkeeping_clean["Squad"]
    .dropna()
    .unique()
)


# ------------------------------------------------------------
# 10. Check match team names
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MATCH HOME TEAM NAMES")
print("=" * 60)

print(
    matches_clean["Home"]
    .dropna()
    .unique()
)


print("\n" + "=" * 60)
print("MATCH AWAY TEAM NAMES")
print("=" * 60)

print(
    matches_clean["Away"]
    .dropna()
    .unique()
)


# ------------------------------------------------------------
# 11. Final message
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STAGE 1 COMPLETE")
print("=" * 60)

print(
    "\nThe raw datasets have been loaded and inspected."
)

print(
    "\nNext stage: Data cleaning and team-name standardisation."
)