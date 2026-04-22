import requests
import pandas as pd

"""
Adding a cardinal direction to be put in the wind direction value since its in degrees, 
this function will be used in the output column
"""
def cardinal_degrees(d):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
#each direction is about 22.5 degrees so 16 directions
    dirs = round(d / 22.5)
    return directions[dirs % 16]

def get_cloud_data(lat,lon):
    url = f'https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=geopotential_height_850hPa,cloud_cover_850hPa,cloud_cover_800hPa,geopotential_height_800hPa,relative_humidity_850hPa,relative_humidity_800hPa,wind_speed_850hPa,wind_speed_800hPa,wind_direction_850hPa,wind_direction_800hPa,temperature_800hPa,temperature_850hPa,visibility&past_days=0&forecast_days=7'
    try:
        cloud_response = requests.get(url).json()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    df = pd.DataFrame(cloud_response["hourly"])
    df['datetime_col'] = pd.to_datetime(df['time'])
    df['hour'] = df['datetime_col'].dt.hour
    df['day'] = df['datetime_col'].dt.date

    bins = [0,5,11,17,23]
    lab = ["Night", "Morning", "Afternoon", "Evening"]
    df['window'] = pd.cut(df['hour'], labels=lab, bins= bins, include_lowest=True)

    grouped_Data = df.groupby(['day','window'], observed=True)[['geopotential_height_800hPa','geopotential_height_850hPa','cloud_cover_800hPa','cloud_cover_850hPa','relative_humidity_800hPa','relative_humidity_850hPa','wind_speed_800hPa','wind_speed_850hPa','wind_direction_800hPa','wind_direction_850hPa','temperature_800hPa','temperature_850hPa','visibility' ]].mean()

# Use .apply() to instantly convert the whole column
    grouped_Data['wind_direction_800hPa'] = grouped_Data['wind_direction_800hPa'].apply(cardinal_degrees)
    grouped_Data['wind_direction_850hPa'] = grouped_Data['wind_direction_850hPa'].apply(cardinal_degrees)

    return df, grouped_Data