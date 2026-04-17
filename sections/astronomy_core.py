from astral import LocationInfo
from astral import SunDirection
from astral.sun import sun
from astral.moon import phase
from datetime import timedelta, datetime
import pytz

def get_astro_data(lat, lon, selected_date, tz_string='Australia/Melbourne'):
    "Initializing Observer Location below"
    tz = pytz.timezone(tz_string)
    loc = LocationInfo(name="Target Peak", region="Australia", timezone=tz_string, latitude=lat, longitude=lon)

    "midnight bounday calculation Below"
    next_day = selected_date + timedelta(days=1)

    "Calculating some sun events"
    sun_today = sun(loc.observer, date=selected_date, tzinfo=tz)
    sun_tomorrow = sun(loc.observer, date=next_day, tzinfo=tz)

    astro_dusk = sun_today['dusk']
    astro_dawn = sun_tomorrow['dawn']

    "calculating the moon phases now"
    moon_val = phase(selected_date)
    if 0 <= moon_val < 3 or 25 <= moon_val <= 28:
        moon_status = "New Moon / Very Dark"
        moon_impact = "Low"
    elif 11 <= moon_val <= 17:
        moon_status = "Full Moon / Very Bright"
        moon_impact = "High"
    else:
        moon_status = "Crescent / Quarter"
        moon_impact = "Medium"

    return {
        "dark_window_start": astro_dusk,
        "dark_window_end": astro_dawn,
        "moon_phase_raw": moon_val,
        "moon_status": moon_status,
        "moon_impact": moon_impact
    }