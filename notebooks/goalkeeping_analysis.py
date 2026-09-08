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

# ============================================================
# FIFA WORLD CUP 2026 - GOALKEEPING ANALYSIS
# Stage 3: Descriptive Statistics, Visualisation,
#          Confidence Interval and Independent T-Test
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


print("=" * 70)
print("FIFA WORLD CUP 2026 - GOALKEEPING ANALYSIS")
print("STAGE 3: STATISTICAL ANALYSIS")
print("=" * 70)


# ============================================================
# 1. LOAD DATA
# ============================================================

goalkeeping = pd.read_csv(
    "C:\\Users\\bhusa\\OneDrive\\Desktop\\FIFA_Python\\data\\fbref_goalkeeping_stats_2026_raw.csv",
    header=1
)

matches = pd.read_csv(
    "C:\\Users\\bhusa\\OneDrive\\Desktop\\FIFA_Python\\data\\fbref_world_cup_2026_matches_raw.csv"
)


# ============================================================
# 2. CREATE WORKING COPIES
# ============================================================

goalkeeping_clean = goalkeeping.copy()
matches_clean = matches.copy()


# ============================================================
# 3. CLEAN GOALKEEPING DATA
# ============================================================

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


# Convert Save% to numeric
goalkeeping_clean["Save%"] = pd.to_numeric(
    goalkeeping_clean["Save%"],
    errors="coerce"
)


# Remove undefined Save%
goalkeeping_clean = goalkeeping_clean.dropna(
    subset=["Save%"]
).copy()


# ============================================================
# 4. STANDARDISE GOALKEEPER TEAM NAMES
# ============================================================

goalkeeping_clean["Team"] = (
    goalkeeping_clean["Squad"]
    .str.replace(
        r"^[a-z]{2,3}\s",
        "",
        regex=True
    )
    .str.strip()
)


# ============================================================
# 5. CLEAN MATCH DATA
# ============================================================

# Remove completely blank rows
matches_clean = matches_clean.dropna(
    how="all"
).copy()


# Clean Home team names
matches_clean["Home_Team"] = (
    matches_clean["Home"]
    .str.replace(
        r"\s[a-z]{2,3}$",
        "",
        regex=True
    )
    .str.strip()
)


# Clean Away team names
matches_clean["Away_Team"] = (
    matches_clean["Away"]
    .str.replace(
        r"^[a-z]{2,3}\s",
        "",
        regex=True
    )
    .str.strip()
)


# ============================================================
# 6. IDENTIFY KNOCKOUT-STAGE TEAMS
# ============================================================

knockout_matches = matches_clean[
    matches_clean["Round"] != "Group stage"
].copy()


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


# ============================================================
# 7. CLASSIFY GOALKEEPERS
# ============================================================

goalkeeping_clean["Stage"] = np.where(
    goalkeeping_clean["Team"].isin(knockout_teams),
    "Knockout",
    "Group-stage elimination"
)


# ============================================================
# 8. DISPLAY FINAL ANALYSIS DATA
# ============================================================

print("\n" + "=" * 70)
print("FINAL ANALYSIS DATA")
print("=" * 70)

print(
    goalkeeping_clean[
        [
            "Player",
            "Team",
            "Save%",
            "Stage"
        ]
    ].to_string(index=False)
)


# ============================================================
# 9. GROUP COUNTS
# ============================================================

print("\n" + "=" * 70)
print("NUMBER OF GOALKEEPERS IN EACH GROUP")
print("=" * 70)

group_counts = (
    goalkeeping_clean["Stage"]
    .value_counts()
)

print(group_counts)


# ============================================================
# 10. DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("DESCRIPTIVE STATISTICS")
print("=" * 70)


descriptive_stats = (
    goalkeeping_clean
    .groupby("Stage")["Save%"]
    .agg(
        Count="count",
        Mean="mean",
        Median="median",
        Std_Dev="std",
        Minimum="min",
        Maximum="max"
    )
)


print("\nSave% descriptive statistics:")
print(
    descriptive_stats.round(2)
)


# ============================================================
# 11. SEPARATE THE TWO GROUPS
# ============================================================

knockout = goalkeeping_clean[
    goalkeeping_clean["Stage"] == "Knockout"
]["Save%"]


group_elimination = goalkeeping_clean[
    goalkeeping_clean["Stage"] == "Group-stage elimination"
]["Save%"]


print("\n" + "=" * 70)
print("GROUP DATA")
print("=" * 70)


print("\nKnockout-stage goalkeeper Save%:")
print(knockout.to_string(index=False))


print("\nGroup-stage elimination goalkeeper Save%:")
print(group_elimination.to_string(index=False))


# ============================================================
# 12. 95% CONFIDENCE INTERVALS
# ============================================================

print("\n" + "=" * 70)
print("95% CONFIDENCE INTERVALS")
print("=" * 70)


# Function to calculate 95% CI
def confidence_interval(data, confidence=0.95):

    n = len(data)

    mean = np.mean(data)

    standard_error = stats.sem(data)

    margin_of_error = (
        stats.t.ppf(
            (1 + confidence) / 2,
            n - 1
        )
        * standard_error
    )

    lower = mean - margin_of_error
    upper = mean + margin_of_error

    return lower, upper


# Knockout CI
knockout_ci = confidence_interval(knockout)


# Group-stage elimination CI
elimination_ci = confidence_interval(
    group_elimination
)


print(
    f"\nKnockout-stage 95% CI: "
    f"{knockout_ci[0]:.2f}% to {knockout_ci[1]:.2f}%"
)


print(
    f"Group-stage elimination 95% CI: "
    f"{elimination_ci[0]:.2f}% to {elimination_ci[1]:.2f}%"
)


# ============================================================
# 13. DIFFERENCE IN MEANS
# ============================================================

print("\n" + "=" * 70)
print("DIFFERENCE IN MEAN SAVE%")
print("=" * 70)


mean_difference = (
    knockout.mean()
    - group_elimination.mean()
)


print(
    f"\nMean Save% - Knockout: "
    f"{knockout.mean():.2f}%"
)

print(
    f"Mean Save% - Group-stage elimination: "
    f"{group_elimination.mean():.2f}%"
)

print(
    f"\nDifference in mean Save%: "
    f"{mean_difference:.2f} percentage points"
)


# ============================================================
# 14. INDEPENDENT TWO-SAMPLE T-TEST
# ============================================================

print("\n" + "=" * 70)
print("INDEPENDENT TWO-SAMPLE T-TEST")
print("=" * 70)


# Welch's independent two-sample t-test
# equal_var=False is used because the two groups
# may have different variances.

t_statistic, p_value = stats.ttest_ind(
    knockout,
    group_elimination,
    equal_var=False
)


print(
    f"\nT-statistic: "
    f"{t_statistic:.4f}"
)

print(
    f"P-value: "
    f"{p_value:.4f}"
)


# ============================================================
# 15. STATISTICAL DECISION
# ============================================================

alpha = 0.05


print("\n" + "=" * 70)
print("STATISTICAL DECISION")
print("=" * 70)


print(
    f"\nSignificance level (alpha): "
    f"{alpha}"
)


if p_value < alpha:

    print(
        "\nDecision: Reject the null hypothesis."
    )

    print(
        "There is statistically significant evidence "
        "of a difference in average Save% between "
        "the two groups."
    )

else:

    print(
        "\nDecision: Fail to reject the null hypothesis."
    )

    print(
        "There is not statistically significant evidence "
        "of a difference in average Save% between "
        "the two groups."
    )


# ============================================================
# 16. RESEARCH QUESTION INTERPRETATION
# ============================================================

print("\n" + "=" * 70)
print("RESEARCH QUESTION INTERPRETATION")
print("=" * 70)


print(
    "\nResearch question:"
)

print(
    "Do goalkeepers from teams that progressed to "
    "the knockout stage differ significantly in "
    "average Save% from goalkeepers whose teams "
    "were eliminated in the group stage?"
)


if p_value < alpha:

    print(
        "\nConclusion:"
    )

    print(
        f"The results indicate that average Save% "
        f"differs significantly between the two groups "
        f"(t = {t_statistic:.2f}, p = {p_value:.4f}). "
        f"The knockout-stage group had a mean Save% "
        f"of {knockout.mean():.2f}%, compared with "
        f"{group_elimination.mean():.2f}% for the "
        f"group-stage elimination group."
    )

else:

    print(
        "\nConclusion:"
    )

    print(
        f"The results do not provide sufficient evidence "
        f"that average Save% differs significantly between "
        f"the two groups "
        f"(t = {t_statistic:.2f}, p = {p_value:.4f}). "
        f"The knockout-stage group had a mean Save% "
        f"of {knockout.mean():.2f}%, compared with "
        f"{group_elimination.mean():.2f}% for the "
        f"group-stage elimination group."
    )


# ============================================================
# 17. VISUALISATION 1 - BAR CHART
# ============================================================

print("\n" + "=" * 70)
print("CREATING BAR CHART")
print("=" * 70)


plt.figure(figsize=(8, 6))


bar_data = (
    goalkeeping_clean
    .groupby("Stage")["Save%"]
    .mean()
    .reset_index()
)


sns.barplot(
    data=bar_data,
    x="Stage",
    y="Save%"
)


plt.title(
    "Average Goalkeeper Save% by Team Progression"
)

plt.xlabel(
    "Team progression"
)

plt.ylabel(
    "Average Save%"
)

plt.ylim(0, 100)

plt.tight_layout()

plt.show()


# ============================================================
# 18. VISUALISATION 2 - BOX PLOT
# ============================================================

print("\n" + "=" * 70)
print("CREATING BOX PLOT")
print("=" * 70)


plt.figure(figsize=(8, 6))


sns.boxplot(
    data=goalkeeping_clean,
    x="Stage",
    y="Save%"
)


sns.stripplot(
    data=goalkeeping_clean,
    x="Stage",
    y="Save%",
    color="black",
    alpha=0.6
)


plt.title(
    "Distribution of Goalkeeper Save% by Team Progression"
)

plt.xlabel(
    "Team progression"
)

plt.ylabel(
    "Save%"
)

plt.ylim(0, 100)

plt.tight_layout()

plt.show()


# ============================================================
# 19. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("STAGE 3 COMPLETE")
print("=" * 70)

print(
    "\nStatistical analysis completed."
)

print(
    "\nThe analysis includes:"
)

print("- Descriptive statistics")
print("- Group means")
print("- Median")
print("- Standard deviation")
print("- 95% confidence intervals")
print("- Difference in means")
print("- Independent two-sample t-test")
print("- Bar chart")
print("- Box plot")

print(
    "\nSave the terminal output and the two charts "
    "for your assignment."
)