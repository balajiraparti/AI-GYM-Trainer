from pathlib import Path
import base64

import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent

CSS_FILE = BASE_DIR /"static"/ "style.css"
FONT_FILE = BASE_DIR / "static" / "uni-sans.heavy-caps.otf"


@st.cache_data
def load_css():
    return CSS_FILE.read_text(encoding="utf-8")


@st.cache_data
def load_font():
    return base64.b64encode(
        FONT_FILE.read_bytes()
    ).decode("utf-8")


def load_styles():

    css = load_css()
    font = load_font()

    st.markdown(
        f"""
        <style>

        @font-face {{
            font-family: "uni-sans.heavy-caps";
            src: url("data:font/otf;base64,{font}")
                 format("opentype");

            font-weight: 900;
            font-style: normal;
            font-display: swap;
        }}

        {css}

        </style>
        """,
        unsafe_allow_html=True,
    )