import streamlit as st

from utils.io import load_yearly


# function to delimit what has to be displayed on the page
def show():
    st.title('"Back in our day…": have the Pyrenees really changed?')

    # putting this project in context
    st.markdown(
        """
I love to run, but since I live in Paris, running on the same asphalt roads sometimes gets monotonous. That is why
every holiday I go to my grandparents' place in the south, in the Ariège Pyrenees.

However, every time I come, my grandparents always tell me the same thing: "Back in our day, it wasn't like this."
It was less hot, there was more snow in winter, fewer heatwaves in summer.
So I have always wondered: is it nostalgia, or measured reality?

Because, as you probably know, the climate has a strong effect on sports performance, just as it plays a key role in
the economy and the harvests.

So I wanted to investigate, to check whether they are telling the truth or whether their memory is playing tricks on them.
"""
    )

    st.subheader("A first look: St Girons, 1961-1990 vs 2011-2025")

    # One row per station and per year
    yearly = load_yearly()

    # St Girons, only the years with at least 330 days of temperature
    st_girons = yearly[(yearly["station"] == "09289001") & (yearly["days_tx"] >= 330)]
    # The two periods we compare: 1961-1990 and 2011-2025
    old = st_girons[st_girons["year"].between(1961, 1990)]
    recent = st_girons[st_girons["year"].between(2011, 2025)]

    # will display 3 values to show the difference between the 2 periods on 3 metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average max temperature",
        f"{recent['tx_mean'].mean():.1f} °C",
        f"{recent['tx_mean'].mean() - old['tx_mean'].mean():+.1f} °C since 1961-1990",
        delta_color="inverse",
    )
    col2.metric(
        "Hot days (≥ 30 °C) per year",
        f"{recent['hot_days'].mean():.0f} days",
        f"{recent['hot_days'].mean() - old['hot_days'].mean():+.0f} days since 1961-1990",
        delta_color="inverse",
    )
    col3.metric(
        "Frost days (< 0 °C) per year",
        f"{recent['frost_days'].mean():.0f} days",
        f"{recent['frost_days'].mean() - old['frost_days'].mean():+.0f} days since 1961-1990",
        delta_color="off",
    )

    st.markdown("So, were they right? Use the chapters on the left to find out.")
