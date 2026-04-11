# StarSpot: High-Altitude Atmospheric & Celestial Predictor

**StarSpot** is a specialized decision-support tool designed for high-altitude navigation, stargazing, and camping. It solves the **"Mt Bogong Problem"**—where surface weather forecasts fail to account for cloud bases and atmospheric conditions at 800hPa/850hPa pressure altitudes.

---

## 🚀 Live Prototype
[https://bingeeverything-starspot-app-h6aylw.streamlit.app/]

---

## 🛠 Project Roadmap

I am building this project in 7 distinct sections, mapping my CSE (AI) and DSA studies to real-world geospatial challenges.

### Section 1: Core Location Engine (LIVE ✅)
*   **Geolocation:** Type-to-search place names with automated Lat/Lon extraction.
*   **Visualization:** Interactive mapping and elevation data integration.
*   *Tech: Geopy, Folium, Streamlit-Folium*

### Section 2: Weather & Cloud Cover at Altitude (LIVE ✅)
*   **The Mt Bogong Logic:** Vertical atmospheric profiling (Low/Mid/High cloud layers) at summit-specific geopotential heights.
*   **Summit Metrics:** Wind speed, precip probability, and a custom Visibility Score.
*   *Tech: Requests (Open-Meteo API), Pandas*

### Section 3: Stargazing Conditions (In Development 🏗️)
*   **Celestial Mechanics:** Real-time moon phase tracking and astronomical dark-window calculation.
*   **Go/No-Go Rating:** A weighted algorithm combining cloud interference and lunar luminosity.
*   *Tech: Astral, Requests*

### Section 4: Camping & Resources (Planned 📅)
*   **OSM Integration:** Scraping nearest campsites, water sources, and shelters from the summit.
*   **Navigation:** Calculating distance and bearing for ground-truth planning.
*   *Tech: Overpy (OpenStreetMap)*

### Section 5: Ranking & Smart Search (DSA Focus)
*   **Optimization:** Using **k-d trees** for efficient nearest-neighbor Dark Sky searches.
*   **Priority Queuing:** Ranking spots by multi-parameter scores; caching API calls with **Hash Maps**.
*   *Tech: Scikit-learn, Heapq*

### Section 6: Forecast Intelligence (Deep Learning Focus)
*   **Predictive AI:** Training a classifier on historical weather vs. visual outcomes to predict actual summit clarity.
*   **Validation:** Moving beyond raw API data to "Actual-at-Peak" probability.
*   *Tech: PyTorch, Scikit-learn*

---

## 🏗 Tech Stack
*   **Language:** Python 3.x
*   **Deployment:** Streamlit Cloud
*   **Data:** Pandas, NumPy, Scikit-learn, PyTorch
*   **Geospatial:** Geopy, Folium, Overpy (OpenStreetMap)
