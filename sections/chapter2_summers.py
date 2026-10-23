import pandas as pd
import streamlit as st

from utils.io import WITNESSES, load_stations, load_yearly
from utils.viz import hot_days_map, yearly_bar_chart


# Everything this page shows
def show():
    st.title('2. "Summers weren\'t this hot"')
    st.markdown("**In St Girons, there are now twice as many days above 30 °C as in the 1960s-1980s.**")

    st.markdown(
        """
A "hot day" is a day when the max temperature reaches 30 °C or more.
Back to running: on such days, high-intensity exercise can be extremely dangerous for a runner.
So let's look at how big the changes have been.
"""
    )

    # The user chooses a station in the sidebar, and we get its id
    station_name = st.sidebar.selectbox("Station", list(WITNESSES.keys()))
    station = WITNESSES[station_name]

    # Only the years with at least 330 days of max temperature
    yearly = load_yearly()
    years = yearly[(yearly["station"] == station) & (yearly["days_tx"] >= 330)]

    # Split the years into the two periods
    old = years[years["year"].between(1961, 1990)]
    recent = years[years["year"].between(2011, 2025)]

    # Stop here if the station has no data in one of the periods
    if len(old) == 0 or len(recent) == 0:
        st.warning("This station does not have complete years in both periods.")
        return

    # Average number of hot days per year in each period
    old_mean = old["hot_days"].mean()
    recent_mean = recent["hot_days"].mean()

    # compare the 2 periods
    col1, col2 = st.columns(2)
    col1.metric("Hot days per year, 1961-1990", f"{old_mean:.0f}")
    col2.metric("Hot days per year, 2011-2025", f"{recent_mean:.0f}",
                f"{recent_mean - old_mean:+.0f} days", delta_color="inverse")

    # Warn the user if the station stopped before 2025a
    last_year = years["year"].max()
    if last_year < 2025:
        st.caption(f"Note: this station has no complete year after {last_year}, so \"2011-2025\" only covers 2011-{last_year}.")

    # Bar chart: one bar per year, and the average of each period
    fig = yearly_bar_chart(years, "hot_days", "Days with max temperature ≥ 30 °C", "#E69F00", old_mean, recent_mean)
    st.plotly_chart(fig, width="stretch")

    st.markdown(
        """
You can try several stations and see that there have been major changes at every one of them, with the number of
hot days doubling or even tripling at some.
"""
    )

    # Map: the change of hot days at every station with a long series, not only our witnesses
    st.subheader("And everywhere else in the Pyrenees?")
    st.markdown(
        "Every station with a long series gained hot days: the most in the plains (Toulouse, Perpignan: +20 to +30 days "
        "per year), the least on the Atlantic coast and on the summits."
    )

    # Only the complete years, split into the two periods
    valid_years = yearly[yearly["days_tx"] >= 330]
    old_years = valid_years[valid_years["year"].between(1961, 1990)]
    recent_years = valid_years[valid_years["year"].between(2011, 2025)]

    # One row per station: average hot days in each period, and number of complete years
    change = pd.DataFrame({
        "old": old_years.groupby("station")["hot_days"].mean(),
        "old_count": old_years.groupby("station")["hot_days"].count(),
        "recent": recent_years.groupby("station")["hot_days"].mean(),
        "recent_count": recent_years.groupby("station")["hot_days"].count(),
    })
    # Only the stations with at least 15 complete years in 1961-1990 and 10 in 2011-2025
    change = change[(change["old_count"] >= 15) & (change["recent_count"] >= 10)]
    change["difference"] = change["recent"] - change["old"]

    # Add the name, the position and the altitude of each station
    change = change.reset_index().merge(load_stations(), on="station")

    st.plotly_chart(hot_days_map(change), width="stretch")
    st.caption(
        f"Map of the {len(change)} stations with a long temperature series. The color shows how many more hot days "
        "(≥ 30 °C) per year there are in 2011-2025 than in 1961-1990: from light yellow (few more) to dark red (many more)."
    )

    st.markdown("So we can first of all say that my grandparents were indeed right. Summers are hotter and hotter and this surely has an impact in many areas. " \
    "" \
    "Nevertheless, a year does not last 3 months so let's look at the other periods.")
