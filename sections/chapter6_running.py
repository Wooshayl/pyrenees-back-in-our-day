import streamlit as st

from utils.io import WITNESSES, load_witness_daily
from utils.viz import ideal_days_chart

# link the month to its number
MONTHS = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
}


def show():
    st.title("6. So when should I run?")
    st.markdown("**In St Girons, the \"perfect\" running days of the scientists have become rarer: about 18 per year in 1961-1990, about 12 today.**")

    st.markdown(
        """
Back to the trails. According to scientists, runners are at their best when the air is **between 4 and 10 °C**
(El Helou et al., 2012, a study of 1.8 million marathon results), and of course with **no rain**.
These are the default settings below, for St Girons. Change them to test your own ideal day,
and see in which months it happened in 1961-1990 and in 2011-2025.
You can for example observe that by increasing the range of degrees example (3 to 20) we lose this time 12 optimal days in the year.
"""
    )

    # The user chooses a station in the sidebar, and we get its id
    station_name = st.sidebar.selectbox("Station", list(WITNESSES.keys()))
    station = WITNESSES[station_name]

    # Two sliders: the temperature range and the maximum rain
    col1, col2 = st.columns(2)
    temp_range = col1.slider("Max temperature of the day between (°C)", -10, 40, (4, 10))
    max_rain = col2.slider("Rain during the day: at most (mm)", 0, 20, 0)

    # One row per day, only the days with a temperature and a rain value
    daily = load_witness_daily()
    days = daily[(daily["station"] == station) & daily["TX"].notna() & daily["RR"].notna()].copy()

    # A day is ideal if the temperature AND the rain are good
    good_temperature = (days["TX"] >= temp_range[0]) & (days["TX"] <= temp_range[1])
    good_rain = days["RR"] <= max_rain
    days["ideal"] = good_temperature & good_rain

    # Give each day its period, and remove the days outside the two periods
    days["period"] = None
    days.loc[days["year"].between(1961, 1990), "period"] = "1961-1990"
    days.loc[days["year"].between(2011, 2025), "period"] = "2011-2025"
    days = days[days["period"].notna()]

    # Stop here if the station has no data in one of the periods
    if days["period"].nunique() < 2:
        st.warning("This station does not have data in both periods.")
        return

    # Share of ideal days, per period and per month
    result = days.groupby(["period", "month"])["ideal"].mean().reset_index()
    result["ideal_pct"] = result["ideal"] * 100
    result["month_name"] = result["month"].map(MONTHS)

    # Share of ideal days x 365 = number of ideal days in an average year
    old = days[days["period"] == "1961-1990"]["ideal"].mean() * 365
    recent = days[days["period"] == "2011-2025"]["ideal"].mean() * 365

    # Two KPI side by side
    col1, col2 = st.columns(2)
    col1.metric("Ideal days per year, 1961-1990", f"{old:.0f} days")
    col2.metric("Ideal days per year, 2011-2025", f"{recent:.0f} days", f"{recent - old:+.0f} days", delta_color="off")

    # Bar chart: share of ideal days for each month
    st.plotly_chart(ideal_days_chart(result), width="stretch")
    st.caption(
        "Grouped bar chart: share of ideal running days for each month, in blue for 1961-1990 and in red for 2011-2025, "
        "with the settings chosen above."
    )

    st.markdown(
        """
With the scientists' settings (4-10 °C, no rain), the ideal days in St Girons only happen from November to March.
They have become rarer, mostly in February, March and November: winters are warmer, so the days are now often above 10 °C.


Conclusion: the "perfect" cold and dry running day is becoming rarer in the valley. So it seems that my grandparents are right and that the climate conditions have changed a lot. Which greatly affects sports performance. So we can wonder if we are destined to reduce this performance scale even more with time.
"""
    )
