import streamlit as st
import requests

def get_elevation(lat, lon):
    url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
    try:
        response = requests.get(url).json()
        return response['elevation'][0]
    except Exception as e:
        st.warning(f"Error: {e}")
        return None