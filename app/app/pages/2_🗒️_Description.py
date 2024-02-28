import streamlit as st

TITLE = "Description"
ARTICLE_URL = "https://qz.com/583202/you-could-have-turned-1000-into-trillions-by-perfectly-trading-the-sp-500-in-2015"

st.set_page_config(
    page_title=TITLE,
    page_icon=":spiral_note_pad:",
)

st.title(f":spiral_note_pad: {TITLE}")

st.markdown(
    f"""
This app is a simple stock portfolio simulator.
It allows you to simulate trading the S&P500 perfectly over a given period of time.

The source of inspiration is [this Quartz article]({ARTICLE_URL}).
"""
)
