import pandas as pd
import streamlit as st

# Folder with the files made by prepare_data.ipynb
DATA_FOLDER = "data/processed/"

# Source of the data, shown in the sidebar
SOURCE = "Source: Météo-France, daily climatological data (data.gouv.fr), Licence Ouverte 2.0"

# The 5 "witness" stations of the story: name -> station id
WITNESSES = {
    "St Girons (414 m)": "09289001",
    "Aulus-les-Bains (733 m)": "09029001",
    "Ascou Lavail (1,090 m)": "09023002",
    "L'Hospitalet (1,425 m)": "09139001",
    "Pic du Midi (2,880 m)": "65059001",
}


# st.cache_data: the file is read only once, then kept in memory
@st.cache_data
def load_stations():
    return pd.read_csv(DATA_FOLDER + "stations.csv", dtype={"station": str, "dept": str})


# One row per station and per year
@st.cache_data
def load_yearly():
    return pd.read_csv(DATA_FOLDER + "yearly.csv", dtype={"station": str})


# One row per station and per winter
@st.cache_data
def load_winters():
    return pd.read_csv(DATA_FOLDER + "winters.csv", dtype={"station": str})


# One row per day, for the 5 witness stations
@st.cache_data
def load_witness_daily():
    return pd.read_csv(DATA_FOLDER + "witness_daily.csv", dtype={"station": str})


# Results of the quality checks, per department
@st.cache_data
def load_quality_checks():
    return pd.read_csv(DATA_FOLDER + "quality_checks.csv", dtype={"dept": str})


# Share of missing values, per variable
@st.cache_data
def load_quality_missing():
    return pd.read_csv(DATA_FOLDER + "quality_missing.csv")
