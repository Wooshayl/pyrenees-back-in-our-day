import streamlit as st

from utils.io import WITNESSES, load_stations
from utils.viz import stations_map

# link the departments and their numbers
DEPARTMENTS = {
    "Ariège": "09",
    "Haute-Garonne": "31",
    "Pyrénées-Atlantiques": "64",
    "Hautes-Pyrénées": "65",
    "Pyrénées-Orientales": "66",
}



def show():
    st.title("1. The witnesses")
    st.markdown("594 weather stations have watched the Pyrenees since 1950, some of them for more than 70 years.")

    st.markdown(
        """
They lived through the same years as my grandparents, and they never forgot a single day.
Each point on the map is a station.
You can see the key information on this chart by hovering over it with your mouse.
"""
    )

    # One row per station: name, position, altitude, first and last year
    all_stations = load_stations()

    # Filter by department
    chosen_names = st.multiselect("Departments", list(DEPARTMENTS.keys()), default=list(DEPARTMENTS.keys()))
    # Turn the chosen department names into department numbers
    chosen_codes = []
    for name in chosen_names:
        chosen_codes.append(DEPARTMENTS[name])
    # Keep only the stations of the chosen departments
    stations = all_stations[all_stations["dept"].isin(chosen_codes)]

    # Map of the stations
    st.plotly_chart(stations_map(stations), width="stretch")
    st.caption(
        "Map of the Pyrenees with one point per weather station. The color shows the altitude: "
        "dark purple for the valleys, yellow for the high mountains."
    )

    st.subheader("Our 5 main witnesses")
    st.markdown("We follow these stations in the next chapters: they go from the valley to the summits.")

    # Table of the 5 witness stations, from the lowest to the highest
    witnesses = all_stations[all_stations["station"].isin(WITNESSES.values())]
    witnesses = witnesses[["name", "altitude", "first_year", "last_year"]].sort_values("altitude")
    # Nicer column names for the table
    witnesses.columns = ["Station", "Altitude (m)", "First year", "Last year"]
    st.dataframe(witnesses, hide_index=True)
