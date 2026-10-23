import streamlit as st

from utils.io import WITNESSES, load_yearly
from utils.viz import yearly_bar_chart

def show():
    st.title('3. "Winters were harsher"')
    st.markdown("We are going to study the evolution of the  number of days below 0degrees in our competing stations.")

    st.markdown(
        """
A "frost day" is a day when the min temperature goes below 0 °C.
For a runner, it means icy trails in the morning.
"""
    )

    # The user chooses a station in the sidebar, and we get its id
    station_name = st.sidebar.selectbox("Station", list(WITNESSES.keys()))
    station = WITNESSES[station_name]

    # Only the years with at least 330 days of min temperature
    yearly = load_yearly()
    years = yearly[(yearly["station"] == station) & (yearly["days_tn"] >= 330)]

    # Split the years into the two periods
    old = years[years["year"].between(1961, 1990)]
    recent = years[years["year"].between(2011, 2025)]

    # Stop here if the station has no data in one of the periods
    if len(old) == 0 or len(recent) == 0:
        st.warning("This station does not have complete years in both periods.")
        return

    # Average number of frost days per year in each period
    old_mean = old["frost_days"].mean()
    recent_mean = recent["frost_days"].mean()

    # COmpare again the 2 periods
    col1, col2 = st.columns(2)
    col1.metric("Frost days per year, 1961-1990", f"{old_mean:.0f}")
    col2.metric("Frost days per year, 2011-2025", f"{recent_mean:.0f}",
                f"{recent_mean - old_mean:+.0f} days", delta_color="off")

    # Warn the user if the station stopped before 2025
    last_year = years["year"].max()
    if last_year < 2025:
        st.caption(f"Note: this station has no complete year after {last_year}, so \"2011-2025\" only covers 2011-{last_year}.")

    # Bar chart: one bar per year, and the average of each period
    fig = yearly_bar_chart(years, "frost_days", "Days with min temperature < 0 °C", "#56B4E9", old_mean, recent_mean)
    st.plotly_chart(fig, width="stretch")

    st.markdown(
        """
At every station except one, there are now 8 to 28 fewer frost days per year.
The exception is Aulus-les-Bains: its frost days jump up suddenly around 1985, while its max temperatures keep rising.
"""
    )

    # The strange case of Aulus-les-Bains, always shown
    aulus = yearly[(yearly["station"] == "09029001") & (yearly["days_tn"] >= 330)]
    aulus_old = aulus[aulus["year"].between(1961, 1990)]["frost_days"].mean()
    aulus_recent = aulus[aulus["year"].between(2011, 2025)]["frost_days"].mean()

    fig = yearly_bar_chart(aulus, "frost_days", "Days with min temperature < 0 °C", "#999999", aulus_old, aulus_recent)
    # Vertical line to show when the sudden change happens
    fig.add_vline(x=1985, line_color="black", annotation_text="Sudden change (~1985)")
    st.plotly_chart(fig, width="stretch")
    st.caption(
        "Bar chart of the frost days per year at Aulus-les-Bains. A black line marks 1985: "
        "after it, the bars are suddenly much higher."
    )

    st.markdown("A climate does not jump overnight: the station has probably moved or changed its sensor. It is something that happens and it is a problem that we will talk about on the next page.")

    st.markdown("Once again we can say that my grandparents seem to be right. The days seem to be hotter and hotter not just in summer but all along the year. But can we really trust the thermometers?")
