import requests
import pandas as pd

def get_cloud_data(lat,lon):
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=geopotential_height_850hPa,cloud_cover_850hPa,cloud_cover_800hPa,geopotential_height_800hPa'
    try:
        cloud_response = requests.get(url).json()
        return cloud_response
    except Exception as e:
        print(f"Error: {e}")
        return None
    
yo = get_cloud_data(-36.73236, 147.30597)
df = pd.DataFrame(yo["hourly"])
df['datetime_col'] = pd.to_datetime(df['time'])
df['hour'] = df['datetime_col'].dt.hour

print(df)