# ============================================================
# FIFA WORLD CUP 2026 - GOALKEEPING ANALYSIS
# Complete Analysis Script
# ============================================================

from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

GOALKEEPING_FILE = DATA_DIR / "C:\\Users\\bhusa\\OneDrive\\Desktop\\FIFA_Python\\data\\fbref_goalkeeping_stats_2026_raw.csv"
MATCH_FILE = DATA_DIR / "C:\\Users\\bhusa\\OneDrive\\Desktop\\FIFA_Python\\data\\fbref_world_cup_2026_matches_raw.csv"


print("=" * 75)
print("FIFA WORLD CUP 2026 - GOALKEEPING ANALYSIS")
print("=" * 75)


# ============================================================
# STAGE 1 - LOAD RAW DATA
# ============================================================

print("\n" + "=" * 75)
print("STAGE 1: LOAD RAW DATA")
print("=" * 75)


goalkeeping = pd.read_csv(
    GOALKEEPING_FILE,
    header=1
)

matches = pd.read_csv(
    MATCH_FILE
)


print("\nDatasets loaded successfully.")

print("\nGoalkeeping shape:")
print(goalkeeping.shape)

print("\nMatch data shape:")
print(matches.shape)


# ============================================================
# STAGE 2 - DATA CLEANING
# ============================================================

print("\n" + "=" * 75)
print("STAGE 2: DATA CLEANING AND CLASSIFICATION")
print("=" * 75)


goalkeeping_clean = goalkeeping.copy()
matches_clean = matches.copy()


# ------------------------------------------------------------
# Keep relevant goalkeeper columns
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


# ------------------------------------------------------------
# Convert Save% to numeric
# ------------------------------------------------------------

goalkeeping_clean["Save%"] = pd.to_numeric(
    goalkeeping_clean["Save%"],
    errors="coerce"
)


# ------------------------------------------------------------
# Show missing Save%
# ------------------------------------------------------------

print("\nGoalkeepers with missing Save%:")

print(
    goalkeeping_clean.loc[
        goalkeeping_clean["Save%"].isna(),
        ["Player", "Squad", "Min", "SoTA", "Saves", "Save%"]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# Remove undefined Save%
# ------------------------------------------------------------

raw_count = len(goalkeeping_clean)

goalkeeping_clean = goalkeeping_clean.dropna(
    subset=["Save%"]
).copy()

valid_count = len(goalkeeping_clean)


print("\nGoalkeepers before removing undefined Save%:")
print(raw_count)

print("\nValid goalkeepers after cleaning:")
print(valid_count)

print("\nGoalkeepers removed:")
print(raw_count - valid_count)


# ------------------------------------------------------------
# Clean goalkeeper team names
# ------------------------------------------------------------

goalkeeping_clean["Team"] = (
    goalkeeping_clean["Squad"]
    .str.replace(
        r"^[a-z]{2,3}\s",
        "",
        regex=True
    )
    .str.strip()
)


# ------------------------------------------------------------
# Remove completely blank match rows
# ------------------------------------------------------------

matches_clean = matches_clean.dropna(
    how="all"
).copy()


# ------------------------------------------------------------
# Clean home team names
# ------------------------------------------------------------

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
# Clean away team names
# ------------------------------------------------------------

matches_clean["Away_Team"] = (
    matches_clean["Away"]
    .str.replace(
        r"^[a-z]{2,3}\s",
        "",
        regex=True
    )
    .str.strip()
)


# ------------------------------------------------------------
# Validate team matching
# ------------------------------------------------------------

goalkeeper_teams = set(
    goalkeeping_clean["Team"].dropna()
)

match_teams = set(
    matches_clean["Home_Team"].dropna()
).union(
    set(matches_clean["Away_Team"].dropna())
)


print("\nNumber of teams in goalkeeper data:")
print(len(goalkeeper_teams))

print("\nNumber of teams in match data:")
print(len(match_teams))

print("\nGoalkeeper teams not found in match data:")
print(sorted(goalkeeper_teams - match_teams))

print("\nMatch teams not found in goalkeeper data:")
print(sorted(match_teams - goalkeeper_teams))


# ------------------------------------------------------------
# Identify knockout-stage teams
# ------------------------------------------------------------

knockout_matches = matches_clean[
    matches_clean["Round"] != "Group stage"
].copy()


knockout_teams = set(
    knockout_matches["Home_Team"].dropna()
).union(
    set(knockout_matches["Away_Team"].dropna())
)


print("\nNumber of knockout-stage teams:")
print(len(knockout_teams))


# ------------------------------------------------------------
# Classify goalkeepers
# ------------------------------------------------------------

goalkeeping_clean["Stage"] = np.where(
    goalkeeping_clean["Team"].isin(knockout_teams),
    "Knockout",
    "Group-stage elimination"
)


print("\nEligible goalkeeper population by group:")

print(
    goalkeeping_clean["Stage"]
    .value_counts()
)


# ============================================================
# STAGE 3 - STRATIFIED RANDOM SAMPLING
# ============================================================

print("\n" + "=" * 75)
print("STAGE 3: STRATIFIED RANDOM SAMPLING")
print("=" * 75)


RANDOM_SEED = 42
SAMPLE_SIZE_PER_GROUP = 15


# ------------------------------------------------------------
# Split into strata
# ------------------------------------------------------------

knockout_population = goalkeeping_clean[
    goalkeeping_clean["Stage"] == "Knockout"
].copy()

elimination_population = goalkeeping_clean[
    goalkeeping_clean["Stage"] == "Group-stage elimination"
].copy()


print("\nPopulation sizes before sampling:")

print(
    f"Knockout: {len(knockout_population)}"
)

print(
    f"Group-stage elimination: {len(elimination_population)}"
)


# ------------------------------------------------------------
# Take random sample from each stratum
# ------------------------------------------------------------

knockout_sample = knockout_population.sample(
    n=SAMPLE_SIZE_PER_GROUP,
    random_state=RANDOM_SEED
)

elimination_sample = elimination_population.sample(
    n=SAMPLE_SIZE_PER_GROUP,
    random_state=RANDOM_SEED
)


# ------------------------------------------------------------
# Combine samples
# ------------------------------------------------------------

sample_data = pd.concat(
    [
        knockout_sample,
        elimination_sample
    ],
    ignore_index=True
)


print("\nSampling method:")
print("Equal-allocation stratified random sampling")

print("\nRandom seed:")
print(RANDOM_SEED)

print("\nSample size per group:")
print(SAMPLE_SIZE_PER_GROUP)

print("\nTotal sample size:")
print(len(sample_data))

print("\nSample group counts:")

print(
    sample_data["Stage"]
    .value_counts()
)


print("\nSelected random sample:")

print(
    sample_data[
        [
            "Player",
            "Team",
            "Save%",
            "Stage"
        ]
    ]
    .sort_values(
        ["Stage", "Team"]
    )
    .to_string(index=False)
)


# ============================================================
# STAGE 4 - STATISTICAL ANALYSIS
# ============================================================

print("\n" + "=" * 75)
print("STAGE 4: STATISTICAL ANALYSIS")
print("=" * 75)


# ------------------------------------------------------------
# Descriptive statistics
# ------------------------------------------------------------

descriptive_stats = (
    sample_data
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


print("\nDescriptive statistics:")

print(
    descriptive_stats.round(2)
)


# ------------------------------------------------------------
# Separate groups
# ------------------------------------------------------------

knockout = sample_data.loc[
    sample_data["Stage"] == "Knockout",
    "Save%"
]

group_eliminated = sample_data.loc[
    sample_data["Stage"] == "Group-stage elimination",
    "Save%"
]


# ------------------------------------------------------------
# Means
# ------------------------------------------------------------

knockout_mean = knockout.mean()
eliminated_mean = group_eliminated.mean()

mean_difference = (
    knockout_mean - eliminated_mean
)


print("\nMean Save% - Knockout:")
print(f"{knockout_mean:.2f}%")

print("\nMean Save% - Group-stage elimination:")
print(f"{eliminated_mean:.2f}%")

print("\nDifference in means:")
print(
    f"{mean_difference:.2f} percentage points"
)


# ------------------------------------------------------------
# 95% confidence interval function
# ------------------------------------------------------------

def calculate_ci(data, confidence=0.95):

    n = len(data)

    mean = data.mean()

    standard_error = stats.sem(data)

    t_critical = stats.t.ppf(
        (1 + confidence) / 2,
        df=n - 1
    )

    margin_error = (
        t_critical * standard_error
    )

    lower = mean - margin_error
    upper = mean + margin_error

    return lower, upper


knockout_ci = calculate_ci(
    knockout
)

eliminated_ci = calculate_ci(
    group_eliminated
)


print("\n95% confidence intervals:")

print(
    f"Knockout: "
    f"{knockout_ci[0]:.2f}% to {knockout_ci[1]:.2f}%"
)

print(
    f"Group-stage elimination: "
    f"{eliminated_ci[0]:.2f}% to {eliminated_ci[1]:.2f}%"
)


# ------------------------------------------------------------
# Hypotheses
# ------------------------------------------------------------

print("\nHypotheses:")

print(
    "H0: Mean Save% is equal between knockout-stage "
    "goalkeepers and group-stage eliminated goalkeepers."
)

print(
    "H1: Mean Save% differs between knockout-stage "
    "goalkeepers and group-stage eliminated goalkeepers."
)


# ------------------------------------------------------------
# Welch independent two-sample t-test
# ------------------------------------------------------------

t_statistic, p_value = stats.ttest_ind(
    knockout,
    group_eliminated,
    equal_var=False
)


print("\nWelch independent two-sample t-test:")

print(
    f"T-statistic: {t_statistic:.4f}"
)

print(
    f"P-value: {p_value:.4f}"
)


# ------------------------------------------------------------
# Statistical decision
# ------------------------------------------------------------

alpha = 0.05


print("\nSignificance level:")
print(alpha)


if p_value < alpha:

    print(
        "\nDecision: Reject the null hypothesis."
    )

    print(
        "There is statistically significant evidence "
        "that mean Save% differs between the two groups."
    )

else:

    print(
        "\nDecision: Fail to reject the null hypothesis."
    )

    print(
        "There is insufficient statistical evidence "
        "to conclude that mean Save% differs between "
        "the two groups."
    )


# ------------------------------------------------------------
# Final interpretation
# ------------------------------------------------------------

print("\n" + "-" * 75)
print("FINAL INTERPRETATION")
print("-" * 75)


print(
    f"\nThe knockout-stage sample had an average Save% "
    f"of {knockout_mean:.2f}%, while the group-stage "
    f"elimination sample had an average Save% of "
    f"{eliminated_mean:.2f}%."
)


print(
    f"The observed difference was "
    f"{mean_difference:.2f} percentage points."
)


print(
    f"Welch's independent two-sample t-test produced "
    f"t = {t_statistic:.2f} and p = {p_value:.4f}."
)


if p_value < alpha:

    print(
        "At the 5% significance level, the result is "
        "statistically significant."
    )

else:

    print(
        "At the 5% significance level, the result is "
        "not statistically significant."
    )


# ============================================================
# VISUALISATION 1 - BAR CHART
# ============================================================

print("\nCreating bar chart...")


bar_data = (
    sample_data
    .groupby("Stage")["Save%"]
    .mean()
    .reset_index()
)


plt.figure(
    figsize=(9, 6)
)


sns.barplot(
    data=bar_data,
    x="Stage",
    y="Save%"
)


plt.title(
    "Average Goalkeeper Save% by Tournament Progression"
)

plt.xlabel(
    "Tournament progression"
)

plt.ylabel(
    "Average Save Percentage (%)"
)

plt.ylim(
    0,
    100
)

plt.tight_layout()


bar_chart_path = (
    PROJECT_ROOT
    / "goalkeeper_save_percentage_bar_chart.png"
)

plt.savefig(
    bar_chart_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# VISUALISATION 2 - BOX PLOT
# ============================================================

print("\nCreating box plot...")


plt.figure(
    figsize=(9, 6)
)


sns.boxplot(
    data=sample_data,
    x="Stage",
    y="Save%"
)


sns.stripplot(
    data=sample_data,
    x="Stage",
    y="Save%",
    color="black",
    alpha=0.65
)


plt.title(
    "Distribution of Goalkeeper Save% by Tournament Progression"
)

plt.xlabel(
    "Tournament progression"
)

plt.ylabel(
    "Save Percentage (%)"
)

plt.ylim(
    0,
    100
)

plt.tight_layout()


boxplot_path = (
    PROJECT_ROOT
    / "goalkeeper_save_percentage_boxplot.png"
)

plt.savefig(
    boxplot_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# SAVE OUTPUT DATA
# ============================================================

sample_output_path = (
    PROJECT_ROOT
    / "goalkeeper_random_sample.csv"
)

stats_output_path = (
    PROJECT_ROOT
    / "goalkeeper_descriptive_statistics.csv"
)


sample_data.to_csv(
    sample_output_path,
    index=False
)


descriptive_stats.to_csv(
    stats_output_path
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 75)
print("ANALYSIS COMPLETE")
print("=" * 75)


print("\nRaw goalkeeper observations:")
print(raw_count)

print("\nEligible observations:")
print(valid_count)

print("\nFinal random sample:")
print(len(sample_data))

print("\nSampling method:")
print(
    "Equal-allocation stratified random sampling "
    "(15 per group)"
)

print("\nOutput files created:")

print(
    bar_chart_path
)

print(
    boxplot_path
)

print(
    sample_output_path
)

print(
    stats_output_path
)