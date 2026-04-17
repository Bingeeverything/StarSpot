import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from sections import location_core
from sections import weather_cloud
from sections import astronomy_core
import pandas as pd

st.subheader("Section 1: Core Location Engine")
address =  st.text_input("Enter a place(e.g., Mt Bogong, Victoria)")

def calculate_stargazing_rating(cloud_condition, moon_impact):
    """
    Combines atmospheric and astronomical data to give a definitive rating.
    """
    # SCENARIO 1: The skies are totally clear
    if cloud_condition == 'Perfect':
        if moon_impact == 'Low':
            return "🟢 GO: Pristine Dark Skies! Perfect conditions."
        elif moon_impact == 'Medium':
            return "🟢 GO: Clear skies. Some moonlight, but bright stars and planets will look great."
        elif moon_impact == 'High':
            return "🟡 MAYBE: Clear skies, but the Full Moon will wash out the Milky Way and faint stars."
            
    # SCENARIO 2: 50/50 chance of clouds
    elif cloud_condition == 'Gamble':
        if moon_impact == 'High':
            return "🔴 NO: High risk of clouds AND a bright moon. Don't risk the drive."
        else:
            return "🟡 MAYBE: Cloud risk is high, but if it clears, the dark sky will be worth it."
            
    # SCENARIO 3: Clouds are guaranteed
    else: 
        # This catches 'Cloud will Come' regardless of what the moon is doing
        return "🔴 NO: Heavy cloud cover expected. Stay home and save gas."

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

        bins = [0,60,80,100]
        lab = ['Perfect','Gamble','Cloud will Come']
        conditions = pd.cut(day_data[f"Humidity at {mean_height_800:.0f}m"], labels=lab, bins= bins, include_lowest=True)
        day_data['CLoud Conditions'] = conditions
        st.dataframe(day_data)

        m = folium.Map(location=[lat,lon], zoom_start=12)

        folium.Marker(
            [lat,lon],popup=f"{address}: {elevation}m",
            icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        
        st_folium(m, height=700, width=500)
    
    else:
        st.warning("Could not find that location. Try adding a state or Country name.")
    

    astro_data = astronomy_core.get_astro_data(lat, lon, selected_date)

    st.divider()
    st.subheader("Section 3: Astronomical Conditions")

    col_astro1, col_astro2, col_astro3 = st.columns(3)

    # Format the datetime objects so they look clean (e.g., "08:45 PM")
    dusk_str = astro_data['dark_window_start'].strftime("%I:%M %p")
    dawn_str = astro_data['dark_window_end'].strftime("%I:%M %p")

    col_astro1.metric("🌑 Moon Phase", astro_data['moon_status'])
    col_astro2.metric("🌌 Dark Window Starts", dusk_str)
    col_astro3.metric("🌅 Dark Window Ends", dawn_str)

    # The Final Verdict
    # Assume 'current_cloud_status' is the 'Perfect', 'Gamble', etc. variable from your Section 2 pandas logic
    try:
        # If day_data is a DataFrame with one row
        current_cloud_status = str(day_data['CLoud Conditions'].iloc[0])
    except AttributeError:
        # If day_data is a Series (single row already flattened)
        current_cloud_status = str(day_data['CLoud Conditions'])

    # NOW the function has the exact string it needs ('Perfect', 'Gamble', etc.)
    final_rating = calculate_stargazing_rating(current_cloud_status, astro_data['moon_impact'])

    st.markdown("### Final Verdict")
    if "GO" in final_rating:
        st.success(final_rating)
    elif "MAYBE" in final_rating:
        st.warning(final_rating)
    else:
        st.error(final_rating)