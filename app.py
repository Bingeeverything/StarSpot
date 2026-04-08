import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from geopy.geocoders import Nominatim
from sections import location_core
from sections import weather_cloud

st.subheader("Section 1: Core Location Engine")
address =  st.text_input("Enter a place(e.g., Mt Bogong, Victoria)")

try:
    if address:
        geolocator = Nominatim(user_agent="StarSpot_app")
        location = geolocator.geocode(address, exactly_one=False)

        if location:
            choosen = st.selectbox('Choose the right adress',(i.address for i in location))
            for i in location:
                if i.address == choosen:
                    coords = i
            selected_date = st.date_input('input a date')

            lat, lon =  coords.latitude, coords.longitude
            elevation = location_core.get_elevation(lat, lon)

            st.write(f"**Location**: {coords.address}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Latitude", f"{lat:.4f}")
            col2.metric("Longitude", f"{lon:.4f}")
            col3.metric("elevation", f"{elevation}m")

            df, grouped_data = weather_cloud.get_cloud_data(lat,lon)
            mean_height_800 = df[df['day'] == selected_date]['geopotential_height_800hPa'].mean().round(2)
            mean_height_850 = df[df['day'] == selected_date]['geopotential_height_850hPa'].mean().round(2)
            day_data = grouped_data.loc[selected_date]
            
            day_data.rename(columns={'cloud_cover_800hPa': f"Cloud Cover at {mean_height_800:.0f}m"}, inplace=True)
            day_data.rename(columns={'cloud_cover_850hPa': f"Cloud Cover at {mean_height_850:.0f}m"}, inplace=True)
            day_data.rename(columns={'relative_humidity_800hPa': f"Humidity at {mean_height_800:.0f}m"}, inplace=True)
            day_data.rename(columns={'relative_humidity_850hPa': f"Humidity at {mean_height_850:.0f}m"}, inplace=True)

            day_data.drop('geopotential_height_800hPa', axis=1, inplace=True)
            day_data.drop('geopotential_height_850hPa', axis=1, inplace=True)

            st.dataframe(day_data)

            m = folium.Map(location=[lat,lon], zoom_start=12)

            folium.Marker(
                [lat,lon],popup=f"{address}: {elevation}m",
                icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)
            
            st_folium(m, height=700, width=500)
        
        else:
            st.warning("Could not find that location. Try adding a state or Country name.")

except Exception as e2:
    st.warning(f"{e2}Address wrong, try again")