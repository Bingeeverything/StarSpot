import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from geopy.geocoders import Nominatim
from sections import location_core

st.subheader("Section 1: Core Location Engine")
address =  st.text_input("Enter a place(e.g., Mt Bogong, Victoria)")

try:
    if address:
        geolocator = Nominatim(user_agent="StarSpot_app")
        location = geolocator.geocode(address)

        if location:
            lat, lon =  location.latitude, location.longitude
            elevation = location_core.get_elevation(lat, lon)

            st.write(f"**Location**: {location_core.address}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Latitude", f"{lat:.4f}")
            col2.metric("Longitude", f"{lon:.4f}")
            col3.metric("elevation", f"{elevation}m")
        else:
            st.warning("Could not find that location. Try adding a state or Country name.")

except Exception as e2:
    st.warning(f"{e2}Address wrong, try again")