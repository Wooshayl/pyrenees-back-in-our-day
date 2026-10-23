import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

from utils.io import load_witness_daily, load_yearly
from utils.viz import future_chart

# Id of the St Girons station
ST_GIRONS = "09289001"

# Official French projection (TRACC, built on IPCC scenarios), compared with the 1976-2005 average:
# +2.1 °C in 2050 and +3.4 °C in 2100
TRACC_WARMING_2050 = 2.1
TRACC_WARMING_2100 = 3.4


def show():
    st.title("7. And in 2050 and 2100?")
    st.markdown("We now want to check the future, check if, if we stay on this same trajectory, the number of ideal days is destined to drop.")

    st.markdown(
        """
My grandparents can only tell me about the past. To look at the future, I trained a machine learning model,
a linear regression. The goal is to use the data that we collected to predict the temperatures in 2050 and in 2100.
"""
    )

    # St Girons, only the years with at least 330 days of max temperature
    yearly = load_yearly()
    years = yearly[(yearly["station"] == ST_GIRONS) & (yearly["days_tx"] >= 330)]

    # 1. Test the model: learn on 1950-2010, then predict 2011-2025 (years the model has never seen)
    train = years[years["year"] <= 2010]
    test = years[years["year"] >= 2011]
    model = LinearRegression()
    model.fit(train[["year"]], train["tx_mean"])
    error = mean_absolute_error(test["tx_mean"], model.predict(test[["year"]]))

    # 2. Learn on all the years, then predict every year up to 2100
    model.fit(years[["year"]], years["tx_mean"])
    future = pd.DataFrame({"year": range(1950, 2101)})
    future["tx_pred"] = model.predict(future[["year"]])

    # Average temperature of the reference periods, and the model's values for 2050 and 2100
    reference = years[years["year"].between(1976, 2005)]["tx_mean"].mean()
    recent = years[years["year"].between(2011, 2025)]["tx_mean"].mean()
    model_2050 = future[future["year"] == 2050]["tx_pred"].iloc[0]
    model_2100 = future[future["year"] == 2100]["tx_pred"].iloc[0]
    # Temperatures in 2050 and 2100 according to the official projection
    tracc_2050 = reference + TRACC_WARMING_2050
    tracc_2100 = reference + TRACC_WARMING_2100

    # Four KPI: the warming of the model and the official warming, in 2050 and in 2100
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Model: warming in 2050", f"{model_2050 - reference:+.1f} °C")
    col2.metric("Official: warming in 2050", f"{TRACC_WARMING_2050:+.1f} °C")
    col3.metric("Model: warming in 2100", f"{model_2100 - reference:+.1f} °C")
    col4.metric("Official: warming in 2100", f"{TRACC_WARMING_2100:+.1f} °C")
    st.caption("Warming compared with the 1976-2005 average.")

    # Chart: observed years, the model line, and the official stars
    st.plotly_chart(future_chart(years, future, tracc_2050, tracc_2100), width="stretch")
    st.caption(
        "Line chart from 1950 to 2100: grey dots are the observed average max temperature of each year in St Girons, "
        "the blue line is the prediction of the model, the black stars are the official projection for 2050 and 2100."
    )

    st.markdown(
        f"""
On 2011-2025, the model trained only on 1950-2010 makes an average error of **{error:.1f} °C**.
In 2050, its prediction is close to the official French projection (TRACC), built on the IPCC climate scenarios.
In 2100, the model goes higher than the official projection (+{model_2100 - reference:.1f} °C against +{TRACC_WARMING_2100} °C):
a straight line continued for 75 years is much less reliable.
So we can still say that the model is quite correct for the data that we have.
"""
    )

    # 3. Running days in the future: take the real days of 2011-2025 and add the predicted warming
    st.subheader("How many ideal running days in 2050 and 2100?")
    # Real days of St Girons in 2011-2025, with a temperature and a rain value
    daily = load_witness_daily()
    days = daily[(daily["station"] == ST_GIRONS) & daily["year"].between(2011, 2025)]
    days = days[days["TX"].notna() & days["RR"].notna()]
    no_rain = days["RR"] == 0

    # The temperature of each day: today, then with the warming of the model and of the official projection
    tx_today = days["TX"]
    tx_model_2050 = days["TX"] + (model_2050 - recent)
    tx_tracc_2050 = days["TX"] + (tracc_2050 - recent)
    tx_model_2100 = days["TX"] + (model_2100 - recent)
    tx_tracc_2100 = days["TX"] + (tracc_2100 - recent)

    # Ideal day = max temperature between 4 and 10 °C and no rain (as in chapter 6)
    today = (tx_today.between(4, 10) & no_rain).mean() * 365
    days_model_2050 = (tx_model_2050.between(4, 10) & no_rain).mean() * 365
    days_tracc_2050 = (tx_tracc_2050.between(4, 10) & no_rain).mean() * 365
    days_model_2100 = (tx_model_2100.between(4, 10) & no_rain).mean() * 365
    days_tracc_2100 = (tx_tracc_2100.between(4, 10) & no_rain).mean() * 365

    # Five KPI side by side: today, then 2050 and 2100
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Ideal days per year, 2011-2025", f"{today:.0f} days")
    col2.metric("2050, model", f"{days_model_2050:.0f} days", f"{days_model_2050 - today:+.0f} days", delta_color="off")
    col3.metric("2050, official", f"{days_tracc_2050:.0f} days", f"{days_tracc_2050 - today:+.0f} days", delta_color="off")
    col4.metric("2100, model", f"{days_model_2100:.0f} days", f"{days_model_2100 - today:+.0f} days", delta_color="off")
    col5.metric("2100, official", f"{days_tracc_2100:.0f} days", f"{days_tracc_2100 - today:+.0f} days", delta_color="off")

    st.markdown(
        """
In St Girons, the ideal running days go from about 12 per year today to about 10 in 2050,
and to only 6 or 7 in 2100: about half of today.
With the model and with the official projection, the answer is the same: if we stay on this trajectory,
the number of ideal days is destined to drop.

**Conclusion** :So we can  identify a real problem, during this streamlit, I linked climate change to sport to show that it will affect the simple act of walking in the mountains. But the truth is that everyone is concerned, the farmers, the workers and even the tourists. climate change is a real problem and my grandparents are right, the changes that they thought they had seen with their own eyes are real. on the scale of a simple human life they were able to observe major changes in good living and bio diversity. So it becomes urgent to act to save our beautiful planet and to be able to travel it, run on these mountains for many more years.

**Limits:** a model that only knows the past cannot know how much humans will emit in the future: the only real climate
models used by the IPCC simulate the physics of the atmosphere. Our data is raw (not homogenised), and the official
projection is for the average temperature of France, not for the max temperature of St Girons. Nevertheless, we have seen that even with the official projections the result will be terrible.
"""
    )
    st.caption(
        "Official projection: TRACC, the French reference warming trajectory for adaptation (Ministry of Ecological "
        "Transition, 2025), based on IPCC scenarios: +2.1 °C in 2050 and +3.4 °C in 2100 compared with 1976-2005 "
        "(+2.7 °C and +4 °C compared with the pre-industrial era)."
    )
