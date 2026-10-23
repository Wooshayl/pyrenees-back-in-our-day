import streamlit as st

# Import one file per page of the story
from sections import (
    chapter1_witnesses,
    chapter2_summers,
    chapter3_winters,
    chapter4_snow,
    chapter5_mountains,
    chapter6_running,
    chapter7_future,
    interlude_quality,
    intro,
)
# Text of the data source, shown at the bottom of the sidebar
from utils.io import SOURCE

# Page title in the browser tab, and use the full width of the screen
st.set_page_config(page_title="Back in our day", layout="wide")

# Top of the sidebar: school logo and information about the project
st.sidebar.image("images/efrei_logo.png")
st.sidebar.markdown(
    """
**Lilian Cao** - Program: DAI

Email: lilian.cao@efrei.net

LinkedIn: [Lilian Cao](https://www.linkedin.com/in/lilian-cao-8a9b60291/)

GitHub: [Wooshayl](https://github.com/Wooshayl)

**Course:** Data Analysis and Visualization

**Professor:** Mano Joseph Mathew

Email: mano.mathew@efrei.fr

**Project proposed:** 75 years of climate change in the Pyrenees, seen through the eyes of a trail runner
"""
)
# A horizontal line to separate the information from the chapters
st.sidebar.divider()

# The rest of the sidebar is the table of contents of the story
CHAPTERS = [
    "Prologue: Back in our day…",
    "1. The witnesses",
    "2. \"Summers weren't this hot\"",
    "3. \"Winters were harsher\"",
    "Interlude: Can we trust the thermometers?",
    "4. \"There was more snow\"",
    "5. \"At least it's cooler in the mountains\"",
    "6. So when should I run?",
    "7. And in 2050 and 2100?",
]

st.sidebar.title('"Back in our day…"')
# key="chapter": the chosen chapter is saved in st.session_state["chapter"]
chapter = st.sidebar.radio("Chapters", CHAPTERS, key="chapter")
# Small grey text with the source of the data
st.sidebar.caption(SOURCE)

# Show the page that matches the chapter chosen in the sidebar
if chapter == "Prologue: Back in our day…":
    intro.show()
elif chapter == "1. The witnesses":
    chapter1_witnesses.show()
elif chapter == "2. \"Summers weren't this hot\"":
    chapter2_summers.show()
elif chapter == "3. \"Winters were harsher\"":
    chapter3_winters.show()
elif chapter == "Interlude: Can we trust the thermometers?":
    interlude_quality.show()
elif chapter == "4. \"There was more snow\"":
    chapter4_snow.show()
elif chapter == "5. \"At least it's cooler in the mountains\"":
    chapter5_mountains.show()
elif chapter == "6. So when should I run?":
    chapter6_running.show()
elif chapter == "7. And in 2050 and 2100?":
    chapter7_future.show()


# "Next" button at the bottom of each page (except the last one)
def go_to_next_chapter():
    # Find the number of the current chapter, then go to the next one
    position = CHAPTERS.index(st.session_state["chapter"])
    st.session_state["chapter"] = CHAPTERS[position + 1]


# No "Next" button on the last chapter
if chapter != CHAPTERS[-1]:
    st.divider()
    st.button("Next chapter →", on_click=go_to_next_chapter)
