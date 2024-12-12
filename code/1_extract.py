import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
import os
  

#TODO Write your extraction code here
from pandaslib import extract_year_mdy

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# Extract states
states_url = "https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv"
states_data = pd.read_csv(states_url)
states_data.to_csv(f"{CACHE_DIR}/states.csv", index=False)

# Extract survey
survey_url = "https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv"
survey_data = pd.read_csv(survey_url)
survey_data["year"] = survey_data["Timestamp"].apply(extract_year_mdy)
survey_data.to_csv(f"{CACHE_DIR}/survey.csv", index=False)

# Extract cost of living for each year
years = survey_data["year"].unique()
for year in years:
    col_url = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0")
    col_data = pd.read_csv(col_url)
    col_data["year"] = year
    col_data.to_csv(f"{CACHE_DIR}/col_{year}.csv", index=False)
