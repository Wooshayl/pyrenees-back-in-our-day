import streamlit as st

from utils.io import load_stations, load_winters
from utils.viz import snow_days_chart, snow_network_chart


def show():
    st.title('4. "There was more snow"')
    st.markdown("Now, let's tackle a part that is more complicated to analyse")

    st.markdown(
        """
A "snow day" is a day with at least 1 cm of snow on the ground, between December and March.
For a trail runner, it means the high paths are closed for the winter. So it is an important metric to know.
"""
    )

    # One row per station and per winter (December to March)
    winters = load_winters()
    # Only the complete winters (at least 110 days of measures)
    winters = winters[winters["days_snow"] >= 110]

    # 1. Our best witness: Ascou Lavail
    st.subheader("Our best witness: Ascou Lavail (1,090 m)")
    ascou = winters[winters["station"] == "09023002"]

    st.plotly_chart(snow_days_chart(ascou), width="stretch")

    # Average number of snow days per winter, before 1990 and after 2011
    old = ascou[ascou["winter"] <= 1990]["snow_days"].mean()
    recent = ascou[ascou["winter"] >= 2011]["snow_days"].mean()

    col1, col2 = st.columns(2)
    col1.metric("Snow days per winter, 1972-1990", f"{old:.0f}")
    col2.metric("Snow days per winter, 2011-2023", f"{recent:.0f}", f"{recent - old:+.0f} days", delta_color="off")

    st.markdown(
        """
Snow days change a lot from one winter to another (from 14 to 107 days), with no clear decrease.
But the recent period only has 7 complete winters, which is not enough to conclude. Indeed as said earlier, it is a very difficult metric to get.
"""
    )

    # 2. Why we can't answer
    st.subheader("Why we can't answer")
    st.markdown(
        """
Each row is a snow station above 1,000 m, and each square is a complete winter.
The old stations stopped between 1984 and 2017, and the new automatic ones only started around 1998.
"""
    )

    stations = load_stations()
    # Add the name and the altitude of each station
    network = winters.merge(stations[["station", "name", "altitude"]], on="station")
    # Only the mountain stations (1,000 m and more)
    network = network[network["altitude"] >= 1000]

    # Only keep the stations with at least 15 complete winters
    winter_count = network.groupby("station")["winter"].count()
    long_stations = winter_count[winter_count >= 15].index
    network = network[network["station"].isin(long_stations)]
    network = network.sort_values("altitude")

    # One row per station, one square per complete winter
    st.plotly_chart(snow_network_chart(network), width="stretch")
    st.caption(
        "One row per snow station above 1,000 m, one square per complete winter. "
        "The old stations stop between 1984 and 2017, the new ones start around 1998: no row covers the whole period."
    )

    st.markdown("Conclusion: It is very difficult to conclude for this part, but it seems that it is not the metric the most affected by global warming.")
