import streamlit as st
from streamlit_js_eval import get_geolocation


if st.checkbox("Check my location"):
    loc = get_geolocation()
    st.write(f"Your coordinates are {loc}")

print(loc)
