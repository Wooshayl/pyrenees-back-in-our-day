# "Back in our day…": have the Pyrenees really changed?

A data storytelling app made with Streamlit.

My grandparents in the Ariège Pyrenees always say: *"Back in our day, it wasn't like this."*
This app checks their memories against 75 years of Météo-France weather records, from the point of view
of a trail runner: hotter summers, milder winters, less snow, warming mountains, fewer ideal running days,
and a simple machine learning forecast for 2050 and 2100.

**Author:** Lilian Cao (DAI), Efrei Paris Panthéon-Assas

**Course:** Data Analysis and Visualization, Mano Joseph Mathew

**Live app:** https://pyrenees-back-in-our-day-uc8hbxj8yymohmlsijzh2q.streamlit.app/

## Data

- **Source:** Météo-France, *Données climatologiques de base - quotidiennes*, on data.gouv.fr:
  https://www.data.gouv.fr/datasets/6569b51ae64326786e4e8e1a
- **License:** Licence Ouverte / Open Licence 2.0
- **Scope:** the 5 Pyrenean departments (09, 31, 64, 65, 66), 1950 to 2026, one row per station and per day.
- **Official projection used in chapter 7:** TRACC, the French reference warming trajectory for adaptation
  (Ministry of Ecological Transition, 2025).

## How to run the app

Tested with Python 3.12 (on Streamlit Community Cloud, choose Python 3.12 in "Advanced settings").

```
pip install -r requirements.txt
python -m streamlit run app.py
```

The app only needs the small files in `data/processed/`, which are included.

## How to rebuild the data (optional)

1. Download the raw files (about 1.2 GB, into `data/raw/`):
   ```
   python download_data.py
   ```
   Files that are already there are not downloaded again. Use `python download_data.py --force` to download everything again.
2. Run the notebook `prepare_data.ipynb` (needs Jupyter). It cleans the raw files and writes the files of `data/processed/`.

## Project structure

```
app.py               the app: sidebar, table of contents, "Next" button
sections/            one file per chapter of the story
utils/io.py          reads the processed files (with st.cache_data)
utils/viz.py         all the Plotly charts and maps
download_data.py     downloads the raw data
prepare_data.ipynb   cleaning and aggregation of the raw data
data/processed/      small files used by the app
images/              Efrei logo
```

## Limits

- The data is raw, not homogenised: some stations moved or changed sensors (Aulus-les-Bains around 1985).
- Stations open and close: a year only counts if it has at least 330 days of measures (a winter: 110 days).
- The forecast is a simple linear regression: it is not a climate model, and a local trend does not prove anything
  about the global climate.
