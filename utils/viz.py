import plotly.express as px

# Okabe-Ito palette: colors that people with color blindness can tell apart
BLUE = "#0072B2"
ORANGE = "#E69F00"
RED = "#D55E00"
LIGHT_BLUE = "#56B4E9"
GREY = "#999999"


def stations_map(stations):
    """Map of the stations, colored by altitude."""
    # One point per station, the color shows the altitude
    fig = px.scatter_map(
        stations,
        lat="lat",
        lon="lon",
        color="altitude",
        hover_name="name",
        hover_data={"altitude": True, "first_year": True, "last_year": True, "lat": False, "lon": False},
        labels={"altitude": "Altitude (m)", "first_year": "First year", "last_year": "Last year"},
        color_continuous_scale="Viridis",
        zoom=6.5,
        height=550,
    )
    return fig


def hot_days_map(table):
    """Map of the stations, colored by the change in hot days between 1961-1990 and 2011-2025."""
    # One point per station, the color shows the extra hot days per year
    fig = px.scatter_map(
        table,
        lat="lat",
        lon="lon",
        color="difference",
        hover_name="name",
        hover_data={"altitude": True, "old": ":.0f", "recent": ":.0f", "difference": ":+.0f", "lat": False, "lon": False},
        labels={
            "difference": "Extra hot days per year",
            "old": "Hot days per year, 1961-1990",
            "recent": "Hot days per year, 2011-2025",
            "altitude": "Altitude (m)",
        },
        color_continuous_scale="YlOrRd",
        zoom=6.5,
        height=550,
    )
    # Bigger points, easier to see and to hover
    fig.update_traces(marker_size=15)
    return fig


def yearly_bar_chart(years, column, axis_label, color, old_mean, recent_mean):
    """Bar chart of one value per year, with the average of the two periods."""
    fig = px.bar(
        years,
        x="year",
        y=column,
        labels={"year": "Year", column: axis_label},
        color_discrete_sequence=[color],
    )
    # Reference lines: average of each period
    fig.add_hline(y=old_mean, line_dash="dash", line_color=BLUE,
                  annotation_text=f"1961-1990 average: {old_mean:.0f} days")
    fig.add_hline(y=recent_mean, line_dash="dash", line_color=RED,
                  annotation_text=f"2011-2025 average: {recent_mean:.0f} days")
    return fig


def stations_over_time_chart(table):
    """Line chart of the number of stations open each year."""
    fig = px.line(
        table,
        x="year",
        y="stations",
        markers=True,
        labels={"year": "Year", "stations": "Number of open stations"},
        color_discrete_sequence=[BLUE],
    )
    return fig


def snow_days_chart(winters):
    """Bar chart of the snow days per winter."""
    fig = px.bar(
        winters,
        x="winter",
        y="snow_days",
        labels={"winter": "Winter (2024 = winter 2023-2024)", "snow_days": "Days with at least 1 cm of snow (Dec-Mar)"},
        color_discrete_sequence=[LIGHT_BLUE],
    )
    return fig


def snow_network_chart(table):
    """One row per snow station, one point per complete winter."""
    fig = px.scatter(
        table,
        x="winter",
        y="name",
        color="altitude",
        color_continuous_scale="Viridis",
        labels={"winter": "Winter", "name": "Station", "altitude": "Altitude (m)"},
        height=700,
    )
    # Small squares instead of round points
    fig.update_traces(marker_symbol="square", marker_size=7)
    return fig


def warming_chart(table):
    """Small multiples: one line chart per station, difference with its own 1961-1990 average."""
    fig = px.line(
        table,
        x="year",
        y="difference",
        facet_row="station_name",
        color="station_name",
        color_discrete_sequence=[ORANGE, BLUE, RED],
        labels={"year": "Year", "difference": "Difference (°C)", "station_name": "Station"},
        height=650,
    )
    # Horizontal line at 0 = same temperature as in 1961-1990
    fig.add_hline(y=0, line_color=GREY)
    return fig


def ideal_days_chart(table):
    """Grouped bar chart: share of ideal running days per month, for the two periods."""
    fig = px.bar(
        table,
        x="month_name",
        y="ideal_pct",
        color="period",
        barmode="group",
        color_discrete_sequence=[BLUE, RED],
        labels={"month_name": "Month", "ideal_pct": "Ideal running days (% of days)", "period": "Period"},
    )
    return fig


def future_chart(observed, predictions, tracc_2050, tracc_2100):
    """Observed yearly temperature, the prediction of the model up to 2100, and the official projection."""
    fig = px.line(
        predictions,
        x="year",
        y="tx_pred",
        color_discrete_sequence=[BLUE],
        labels={"year": "Year", "tx_pred": "Average max temperature of the year (°C)"},
    )
    # Name of the model line in the legend
    fig.update_traces(name="Model (linear regression)", showlegend=True)
    # Grey points: the real observed years
    fig.add_scatter(x=observed["year"], y=observed["tx_mean"], mode="markers",
                    marker_color=GREY, name="Observed (St Girons)")
    # Black stars: the official projection for 2050 and 2100
    fig.add_scatter(x=[2050, 2100], y=[tracc_2050, tracc_2100], mode="markers", marker_symbol="star", marker_size=16,
                    marker_color="black", name="Official projection (TRACC)")
    return fig
