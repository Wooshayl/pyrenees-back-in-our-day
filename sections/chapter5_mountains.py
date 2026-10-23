import pandas as pd
import streamlit as st

from utils.io import WITNESSES, load_yearly
from utils.viz import warming_chart

# From the valley to the summit
STATIONS = ["St Girons (414 m)", "Ascou Lavail (1,090 m)", "Pic du Midi (2,880 m)"]


def show():
    st.title('5. "At least it\'s cooler in the mountains"')

    st.markdown(
        """
When it is too hot in the valley, my grandparents tell me to go and run higher up. But I personally thought that the summits had logically warmed as much as the valleys. let's analyse this :
Each line shows how much warmer each year is than the station's own 1961-1990 average.
"""
    )

    yearly = load_yearly()

    # For each station: how much warmer each year is than its 1961-1990 average
    tables = []
    for name in STATIONS:
        station = WITNESSES[name]
        years = yearly[(yearly["station"] == station) & (yearly["days_tx"] >= 330)].copy()

        reference = years[years["year"].between(1961, 1990)]["tx_mean"].mean()
        years["difference"] = years["tx_mean"] - reference
        years["station_name"] = name
        tables.append(years)

    # Put the tables of the 3 stations together
    warming = pd.concat(tables)

    # One KPI per station: how much warmer is 2011-2025 than 1961-1990?
    columns = st.columns(3)
    for i, name in enumerate(STATIONS):
        station_years = warming[warming["station_name"] == name]
        recent = station_years[station_years["year"].between(2011, 2025)]["difference"].mean()
        columns[i].metric(name, f"{recent:+.1f} °C", "2011-2025 vs 1961-1990", delta_color="off")

    # One line chart per station
    st.plotly_chart(warming_chart(warming), width="stretch")
    st.caption(
        "Three line charts, one per station (St Girons, Ascou Lavail, Pic du Midi). Each line shows how much warmer "
        "each year is than the station's 1961-1990 average: the three lines go up in the same way."
    )

    st.markdown(
        """
The three lines go up together: the Pic du Midi warmed about as much as St Girons, 2,500 m lower.
"""
    )

    st.markdown("So, it seems that my grandparents are right in some proportions, indeed like in their time the summits are colder than the valleys. however they have warmed just as much. Their advice is still good, but the conditions for running have also dropped")
