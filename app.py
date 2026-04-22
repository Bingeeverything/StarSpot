import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from sections import location_core
from sections import weather_cloud
from sections import astronomy_core
import pandas as pd

st.set_page_config(page_title="StarSpot Planner", page_icon="🌌", layout="centered", initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center;'>✨ StarSpot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Astrophotography & Dark Sky Forecaster</p>", unsafe_allow_html=True)
st.divider()

address = st.text_input("Enter a place(e.g., Mt Bogong, Victoria)")

# --- HELPER FUNCTIONS ---
def calculate_stargazing_rating(cloud_condition, moon_impact):
    """Combines atmospheric and astronomical data to give a definitive rating."""
    if cloud_condition == 'Perfect':
        if moon_impact == 'Low': return "🟢 GO: Pristine Dark Skies! Perfect conditions."
        elif moon_impact == 'Medium': return "🟢 GO: Clear skies. Some moonlight, but bright stars look great."
        elif moon_impact == 'High': return "🟡 MAYBE: Clear skies, but the Full Moon washes out faint stars."
    elif cloud_condition == 'Gamble':
        if moon_impact == 'High': return "🔴 NO: High risk of clouds AND a bright moon. Don't risk the drive."
        else: return "🟡 MAYBE: Cloud risk is high, but if it clears, the dark sky will be worth it."
    else: 
        return "🔴 NO: Heavy cloud cover expected. Stay home and save gas."

def format_col_name(df, old_col, new_name, h_800, h_850):
    """Safely renames columns using DRY principles"""
    if '800hPa' in old_col:
        formatted_name = f"{new_name} at {h_800:.0f}m" 
    else:
        formatted_name = f"{new_name} at {h_850:.0f}m"
        
    df.rename(columns={old_col: formatted_name}, inplace=True)


if address:
    geolocator = Nominatim(user_agent="StarSpot_app")
    location = geolocator.geocode(address, exactly_one=False)

    if location:
        choosen = st.selectbox('Choose the right address', [i.address for i in location])
        for i in location:
            if i.address == choosen:
                coords = i
        selected_date = st.date_input('Input a date')

        lat, lon = coords.latitude, coords.longitude
        elevation = location_core.get_elevation(lat, lon)

        st.write(f"**Location**: {coords.address}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Latitude", f"{lat:.4f}")
        col2.metric("Longitude", f"{lon:.4f}")
        col3.metric("Elevation", f"{elevation}m")

        # Fetch Weather Data
        df, grouped_data = weather_cloud.get_cloud_data(lat,lon)
        mean_height_800 = df[df['day'] == selected_date]['geopotential_height_800hPa'].mean().round(2)
        mean_height_850 = df[df['day'] == selected_date]['geopotential_height_850hPa'].mean().round(2)
        day_data = grouped_data.loc[selected_date]
        
        format_col_name(day_data, 'cloud_cover_800hPa', 'Cloud Cover', mean_height_800, mean_height_850)
        format_col_name(day_data, 'cloud_cover_850hPa', 'Cloud Cover', mean_height_800, mean_height_850)
        format_col_name(day_data, 'relative_humidity_800hPa', 'Humidity', mean_height_800, mean_height_850)
        format_col_name(day_data, 'relative_humidity_850hPa', 'Humidity', mean_height_800, mean_height_850)
        format_col_name(day_data, 'wind_speed_800hPa', 'Wind Speed', mean_height_800, mean_height_850)
        format_col_name(day_data, 'wind_speed_850hPa', 'Wind Speed', mean_height_800, mean_height_850)
        format_col_name(day_data, 'wind_direction_800hPa', 'Wind Dir', mean_height_800, mean_height_850)
        format_col_name(day_data, 'wind_direction_850hPa', 'Wind Dir', mean_height_800, mean_height_850)

        day_data.drop('geopotential_height_800hPa', axis=1, inplace=True)
        day_data.drop('geopotential_height_850hPa', axis=1, inplace=True)
        day_data['Visibility (km)'] = (day_data['visibility'] / 1000).round(1)
        day_data.drop('visibility', axis=1, inplace=True)

        bins = [0,60,80,100]
        lab = ['Perfect','Gamble','Cloud will Come']
        conditions = pd.cut(day_data[f"Humidity at {mean_height_800:.0f}m"], labels=lab, bins= bins, include_lowest=True)
        day_data['Cloud Conditions'] = conditions
        
        st.markdown("### Atmospheric Conditions")
        st.dataframe(day_data, hide_index=False, use_container_width=True)

        #SECTION 3: ASTRONOMY
        astro_data = astronomy_core.get_astro_data(lat, lon, selected_date)

        st.divider()
        st.subheader("Section 3: Astronomical Conditions")

        col_astro1, col_astro2, col_astro3 = st.columns(3)
        dusk_str = astro_data['dark_window_start'].strftime("%I:%M %p")
        dawn_str = astro_data['dark_window_end'].strftime("%I:%M %p")

        col_astro1.metric("🌑 Moon Phase", astro_data['moon_status'])
        col_astro2.metric("🌌 Dark Window Starts", dusk_str)
        col_astro3.metric("🌅 Dark Window Ends", dawn_str)

        # Calculate Final Verdict
        try:
            current_cloud_status = str(day_data['Cloud Conditions'].iloc[0])
        except AttributeError:
            current_cloud_status = str(day_data['Cloud Conditions'])

        final_rating = calculate_stargazing_rating(current_cloud_status, astro_data['moon_impact'])

        st.markdown("### Final Verdict")
        if "GO" in final_rating:
            st.success(final_rating)
        elif "MAYBE" in final_rating:
            st.warning(final_rating)
        else:
            st.error(final_rating)

        #MAP RENDERING
        st.divider()
        st.markdown("### Target Location")
        m = folium.Map(location=[lat,lon], zoom_start=12, tiles="OpenStreetMap")

        folium.Marker(
            [lat,lon],
            popup=f"{address}: {elevation}m",
            icon=folium.Icon(color='purple', icon='info-sign')
        ).add_to(m)

        st_folium(m, height=500, width=700, returned_objects=[])
    
    else:
        st.warning("Could not find that location. Try adding a state or Country name.")