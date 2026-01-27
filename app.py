import io

import streamlit as st
from streamlit_ace import st_ace

from linter import Linter
from linter.exceptions import LinterSuccess

hide_streamlit_style = """
    <style>
    .stAppHeader {display: none;}
    .stMain .block-container {
      padding-top: 2rem;
    }
    h1 {
        font-size: 28px!important;
    }
    button[aria-label="Fullscreen"] {
      visibility: hidden;
    }
    </style>
"""
_ = st.markdown(hide_streamlit_style, unsafe_allow_html=True)


st.set_page_config(page_title="Vigimare Linter", page_icon="assets/favicon.ico", layout="centered")  # HTML title
cols = st.columns([1, 4, 1])
with cols[1]:
    theme = st.context.theme.type
    logo_path = "assets/logo_dark.png" if theme == "dark" else "assets/logo_light.png"
    _ = st.image(logo_path)


@st.cache_resource
def init_linter():
    return Linter("xsd")


linter = init_linter()


def parse(content: str):
    print("Validating XML")
    xml_file = io.StringIO(content)
    result = linter.validate(xml_file)
    return result


def run_linter_and_display(content: str):
    with st.spinner("Running linter..."):
        result = parse(content)
    if isinstance(result, LinterSuccess):
        with st.expander("✅ Success", expanded=True):
            _ = st.success(str(result))
    else:
        with st.expander("⚠️ Error", expanded=True):
            _ = st.error(str(result))


_ = st.title("VIGIMARE Linter")
st.write(
    "".join(
        [
            "Please paste or upload XML and run linter. Every XML must adhere to the [data model](https://github.com/vigimare/xsd) defined ",
            "in the VIGIMARE project. Errors must me corrected before sent to Kafka.",
        ],
    )
)
option = st.radio("Input type:", ["Paste Text", "Upload File"])


if option == "Upload File":
    file = st.file_uploader("Upload a file")
    if file:
        content = file.read().decode("utf-8", errors="ignore")
        if st.button("Run Linter"):
            run_linter_and_display(content)

elif option == "Paste Text":
    themes = ["Tomorrow Night", "Monokai", "GitHub", "Solarized Light", "Nord Dark"]

    theme = st.radio("Select code box theme", themes, horizontal=True)
    xml = st_ace(
        value="<field>\n    <child>value here</child>\n</field>",
        language="xml",
        theme=theme.lower().replace(" ", "_"),
        key="xml_editor",
        height=320,
        show_gutter=True,  # line numbers
        auto_update=True,  # live updates (no internal Apply button)
    )

    if st.button("Run Linter"):
        run_linter_and_display(xml)
