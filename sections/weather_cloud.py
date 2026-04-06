import requests
import pandas as pd

def get_cloud_data(lat,lon):
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=geopotential_height_850hPa,cloud_cover_850hPa,cloud_cover_800hPa,geopotential_height_800hPa,relative_humidity_850hPa,relative_humidity_800hPa&timezone=Australia%2FSydney'
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

    grouped_Data = df.groupby(['day','window'], observed=True)[['cloud_cover_850hPa','cloud_cover_800hPa','relative_humidity_850hPa','relative_humidity_800hPa']].mean()
    return df, grouped_Data