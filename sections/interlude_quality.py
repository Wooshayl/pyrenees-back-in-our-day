import pandas as pd
import streamlit as st

from utils.io import load_quality_checks, load_quality_missing, load_stations
from utils.viz import stations_over_time_chart

# Variable code -> readable name
VARIABLE_NAMES = {
    "TX": "Max temperature",
    "TN": "Min temperature",
    "RR": "Rain",
    "NEIGETOTX": "Snow depth",
    "HNEIGEF": "Fresh snow",
}


# Display the content of the page
def show():
    st.title("Interlude: can we trust the thermometers?")
    st.markdown("We did data cleaning and engineering however, there are things that are difficult to analyse like the stations that close or even worse move or change equipment. So we can end up with values that seem correct but that are no longer of the same quality as the previous values of the same station. So it is difficult to analyse the data." \
    "So let's try to redo a global check: ")

    # 1. Validity checks
    st.subheader("1. Validity checks")
    st.markdown("We looked for duplicates and impossible values (for example a temperature above 50 °C).")
    checks = load_quality_checks()
    # Keep the useful columns and give them readable names
    checks = checks[["dept", "rows", "stations", "duplicates", "bad_TX", "bad_TN", "TN_above_TX", "bad_RR", "bad_snow"]]
    checks.columns = ["Department", "Rows (station-days)", "Stations", "Duplicates", "Impossible max temp.",
                      "Impossible min temp.", "Min temp. above max", "Impossible rain", "Impossible snow"]
    st.dataframe(checks, hide_index=True)
    st.markdown("Every check is at 0: no duplicates and no impossible values.")

    # 2. Missing values
    st.subheader("2. Missing values")
    st.markdown("Many values are missing, mostly because small stations only have a rain gauge. We do not fill the holes.")
    missing = load_quality_missing()
    # Replace the codes (TX, RR...) by readable names
    missing["variable"] = missing["variable"].map(VARIABLE_NAMES)
    missing.columns = ["Variable", "Missing values (%)", "Stations that measure it"]
    st.dataframe(missing, hide_index=True)

    # 3. Stations come and go
    st.subheader("3. Stations come and go")
    stations = load_stations()

    # For each year, count the stations that were open
    rows = []
    for year in range(1950, 2027):
        is_open = (stations["first_year"] <= year) & (stations["last_year"] >= year)
        rows.append({"year": year, "stations": is_open.sum()})
    open_stations = pd.DataFrame(rows)

    # Line chart: number of open stations each year
    st.plotly_chart(stations_over_time_chart(open_stations), width="stretch")
    st.markdown("The stations of 1960 are not the ones of today: that is why we follow the same witness stations over time.")

    # 4. Our rules
    st.subheader("4. Our rules")
    st.markdown(
        """
- A year only counts if it has at least 330 days of measures (a winter: 110 days).
- We compare long periods (1961-1990 vs 2011-2025), never two single years.
- The data is raw: it is not corrected for station moves or sensor changes (like Aulus-les-Bains).
"""
    )
