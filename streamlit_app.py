import streamlit as st

def main_page():
    st.markdown("# Home 🎈")
    st.sidebar.markdown("# Home 🎈")

def page2():
    st.markdown("# Analyse reading habits ❄️")
    st.sidebar.markdown("# Page 2 ❄️")

def page3():
    st.markdown("# Page 5 🎉")
    st.sidebar.markdown("# Page 5 🎉")

page_names_to_funcs = {
    "Home": main_page,
    "Analyse reading habits": page2,
    "Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()