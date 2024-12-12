import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here
from pandaslib import clean_country_usa, clean_currency

CACHE_DIR = "cache"

# Load data
states_data = pd.read_csv(f"{CACHE_DIR}/states.csv")
survey_data = pd.read_csv(f"{CACHE_DIR}/survey.csv")

# Combine COL data
years = survey_data["year"].unique()
col_data = pd.concat(
    [pd.read_csv(f"{CACHE_DIR}/col_{year}.csv") for year in years], ignore_index=True
)

# Clean and merge survey data
survey_data["_country"] = survey_data["Which country do you work in?"].apply(clean_country_usa)
survey_states_combined = survey_data.merge(
    states_data, left_on="If you're in the U.S., what state do you work in?", right_on="State", how="inner"
)
survey_states_combined["_full_city"] = survey_states_combined["City"] + ", " + survey_states_combined["Abbreviation"] + ", " + survey_states_combined["_country"]

# Combine with COL data
combined = survey_states_combined.merge(col_data, on=["year", "_full_city"])

# Normalize salary
combined["__annual_salary_cleaned"] = combined["Annual salary"].apply(clean_currency)
combined["_annual_salary_adjusted"] = combined["__annual_salary_cleaned"] / (combined["COL"] / 100)

# Save engineered dataset
combined.to_csv(f"{CACHE_DIR}/survey_dataset.csv", index=False)

# Create reports
report_age = combined.pivot_table(
    values="_annual_salary_adjusted", index="_full_city", columns="How old are you?", aggfunc="mean"
)
report_age.to_csv(f"{CACHE_DIR}/annual_salary_adjusted_by_location_and_age.csv")

report_education = combined.pivot_table(
    values="_annual_salary_adjusted", index="_full_city", columns="What is your highest level of education?", aggfunc="mean"
)
report_education.to_csv(f"{CACHE_DIR}/annual_salary_adjusted_by_location_and_education.csv")

