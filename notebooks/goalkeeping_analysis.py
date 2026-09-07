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

# ============================================================
# FIFA WORLD CUP 2026 - GOALKEEPING ANALYSIS
# Stage 2: Data Cleaning and Group Classification
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


print("=" * 70)
print("FIFA WORLD CUP 2026 - GOALKEEPING ANALYSIS")
print("STAGE 2: DATA CLEANING AND GROUP CLASSIFICATION")
print("=" * 70)


# ============================================================
# 1. LOAD RAW DATA
# ============================================================

goalkeeping = pd.read_csv(
    "C:\\Users\\bhusa\\OneDrive\\Desktop\\FIFA_Python\\data\\fbref_goalkeeping_stats_2026_raw.csv",
    header=1
)

matches = pd.read_csv(
    "C:\\Users\\bhusa\\OneDrive\\Desktop\\FIFA_Python\\data\\fbref_world_cup_2026_matches_raw.csv"
)

print("\nRaw datasets loaded successfully.")


# ============================================================
# 2. CREATE WORKING COPIES
# ============================================================

goalkeeping_clean = goalkeeping.copy()
matches_clean = matches.copy()

print("Working copies created.")


# ============================================================
# 3. CLEAN GOALKEEPING DATA
# ============================================================

print("\n" + "=" * 70)
print("CLEANING GOALKEEPING DATA")
print("=" * 70)


# ------------------------------------------------------------
# 3.1 Keep only the columns required for this analysis
# ------------------------------------------------------------

goalkeeping_clean = goalkeeping_clean[
    [
        "Player",
        "Pos",
        "Squad",
        "MP",
        "Starts",
        "Min",
        "SoTA",
        "Saves",
        "Save%",
        "W",
        "D",
        "L",
        "CS",
        "CS%"
    ]
].copy()

print("\nRelevant columns selected.")


# ------------------------------------------------------------
# 3.2 Standardise the Save% variable
# ------------------------------------------------------------

goalkeeping_clean["Save%"] = pd.to_numeric(
    goalkeeping_clean["Save%"],
    errors="coerce"
)

print("\nSave% converted to numeric format.")


# ------------------------------------------------------------
# 3.3 Inspect missing Save% values
# ------------------------------------------------------------

missing_save = goalkeeping_clean[
    goalkeeping_clean["Save%"].isna()
]

print("\nGoalkeepers with missing Save%:")
print(
    missing_save[
        ["Player", "Squad", "SoTA", "Saves", "Save%"]
    ]
)


# ------------------------------------------------------------
# 3.4 Remove records where Save% is undefined
# ------------------------------------------------------------

before_save_cleaning = len(goalkeeping_clean)

goalkeeping_clean = goalkeeping_clean.dropna(
    subset=["Save%"]
).copy()

after_save_cleaning = len(goalkeeping_clean)

print(
    f"\nRecords before removing missing Save%: "
    f"{before_save_cleaning}"
)

print(
    f"Records after removing missing Save%: "
    f"{after_save_cleaning}"
)

print(
    f"Records removed: "
    f"{before_save_cleaning - after_save_cleaning}"
)


# ============================================================
# 4. STANDARDISE GOALKEEPER TEAM NAMES
# ============================================================

print("\n" + "=" * 70)
print("STANDARDISING GOALKEEPER TEAM NAMES")
print("=" * 70)


# Goalkeeping Squad values look like:
# "au Australia"
# "br Brazil"
# "eng England"

# Remove the country code from the beginning.

goalkeeping_clean["Team"] = (
    goalkeeping_clean["Squad"]
    .str.replace(
        r"^[a-z]{2,3}\s",
        "",
        regex=True
    )
    .str.strip()
)

print("\nCleaned goalkeeper team names:")
print(
    sorted(goalkeeping_clean["Team"].unique())
)


# ============================================================
# 5. CLEAN MATCH RESULTS
# ============================================================

print("\n" + "=" * 70)
print("CLEANING MATCH RESULTS")
print("=" * 70)


# ------------------------------------------------------------
# 5.1 Remove completely blank rows
# ------------------------------------------------------------

before_match_cleaning = len(matches_clean)

matches_clean = matches_clean.dropna(
    how="all"
).copy()

after_match_cleaning = len(matches_clean)

print(
    f"\nMatch rows before removing blank rows: "
    f"{before_match_cleaning}"
)

print(
    f"Match rows after removing blank rows: "
    f"{after_match_cleaning}"
)

print(
    f"Blank rows removed: "
    f"{before_match_cleaning - after_match_cleaning}"
)


# ------------------------------------------------------------
# 5.2 Standardise Home team names
# ------------------------------------------------------------

# Home teams look like:
# "Mexico mx"
# "Brazil br"
# "Australia au"

matches_clean["Home_Team"] = (
    matches_clean["Home"]
    .str.replace(
        r"\s[a-z]{2,3}$",
        "",
        regex=True
    )
    .str.strip()
)


# ------------------------------------------------------------
# 5.3 Standardise Away team names
# ------------------------------------------------------------

# Away teams look like:
# "za South Africa"
# "cz Czechia"
# "ma Morocco"

matches_clean["Away_Team"] = (
    matches_clean["Away"]
    .str.replace(
        r"^[a-z]{2,3}\s",
        "",
        regex=True
    )
    .str.strip()
)


print("\nHome and Away team names standardised.")


# ============================================================
# 6. CHECK TEAM NAME MATCHING
# ============================================================

print("\n" + "=" * 70)
print("CHECKING TEAM NAME MATCHING")
print("=" * 70)


goalkeeping_teams = set(
    goalkeeping_clean["Team"].dropna()
)

match_home_teams = set(
    matches_clean["Home_Team"].dropna()
)

match_away_teams = set(
    matches_clean["Away_Team"].dropna()
)

match_teams = (
    match_home_teams.union(match_away_teams)
)


print("\nNumber of teams in goalkeeping dataset:")
print(len(goalkeeping_teams))

print("\nNumber of teams in match dataset:")
print(len(match_teams))


# ------------------------------------------------------------
# Teams in goalkeeping but not matches
# ------------------------------------------------------------

goalkeeping_only = (
    goalkeeping_teams - match_teams
)

print(
    "\nTeams found in goalkeeping data "
    "but not in match data:"
)

print(
    sorted(goalkeeping_only)
)


# ------------------------------------------------------------
# Teams in matches but not goalkeeping
# ------------------------------------------------------------

matches_only = (
    match_teams - goalkeeping_teams
)

print(
    "\nTeams found in match data "
    "but not in goalkeeping data:"
)

print(
    sorted(matches_only)
)


# ============================================================
# 7. IDENTIFY KNOCKOUT-STAGE TEAMS
# ============================================================

print("\n" + "=" * 70)
print("IDENTIFYING KNOCKOUT-STAGE TEAMS")
print("=" * 70)


# Any team appearing in a match after the Group Stage
# progressed to the knockout stage.

knockout_matches = matches_clean[
    matches_clean["Round"] != "Group stage"
].copy()


# Get teams appearing in knockout-stage matches.

knockout_home_teams = set(
    knockout_matches["Home_Team"].dropna()
)

knockout_away_teams = set(
    knockout_matches["Away_Team"].dropna()
)

knockout_teams = (
    knockout_home_teams.union(knockout_away_teams)
)


print("\nNumber of knockout-stage teams:")
print(len(knockout_teams))


print("\nKnockout-stage teams:")

for team in sorted(knockout_teams):
    print("-", team)


# ============================================================
# 8. CLASSIFY GOALKEEPERS INTO TWO GROUPS
# ============================================================

print("\n" + "=" * 70)
print("CLASSIFYING GOALKEEPERS")
print("=" * 70)


goalkeeping_clean["Stage"] = np.where(
    goalkeeping_clean["Team"].isin(knockout_teams),
    "Knockout",
    "Group-stage elimination"
)


# ============================================================
# 9. DISPLAY CLASSIFICATION RESULTS
# ============================================================

print("\nGoalkeeper classification:")

print(
    goalkeeping_clean[
        [
            "Player",
            "Team",
            "Save%",
            "Stage"
        ]
    ].sort_values(
        by="Team"
    ).to_string(index=False)
)


# ============================================================
# 10. CHECK GROUP COUNTS
# ============================================================

print("\n" + "=" * 70)
print("GROUP COUNTS")
print("=" * 70)

group_counts = (
    goalkeeping_clean["Stage"]
    .value_counts()
)

print(group_counts)


# ============================================================
# 11. CHECK SAVE% BY GROUP
# ============================================================

print("\n" + "=" * 70)
print("SAVE% BY GROUP")
print("=" * 70)


print(
    goalkeeping_clean
    .groupby("Stage")["Save%"]
    .describe()
)


# ============================================================
# 12. FINAL DATASET CHECK
# ============================================================

print("\n" + "=" * 70)
print("FINAL CLEAN DATASET CHECK")
print("=" * 70)


print("\nFinal number of goalkeeper observations:")
print(len(goalkeeping_clean))

print("\nMissing values in key variables:")

print(
    goalkeeping_clean[
        ["Player", "Team", "Save%", "Stage"]
    ].isna().sum()
)


print("\nStage 2 completed successfully.")

print(
    "\nNext stage: Descriptive statistics, "
    "visualisation, confidence interval, "
    "and independent two-sample t-test."
)