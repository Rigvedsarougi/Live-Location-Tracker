import streamlit as st
from streamlit_javascript import st_javascript
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="User Location App", layout="wide")

st.title("📍 Show Your Current Location on Map")

# Get user coordinates using JS
coords = st_javascript("""
    async () => {
        const getPosition = () =>
            new Promise((resolve, reject) =>
                navigator.geolocation.getCurrentPosition(resolve, reject)
            );

        try {
            const position = await getPosition();
            return {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            };
        } catch (err) {
            return null;
        }
    }
""", key="get_location")

# Display map with user location
if coords:
    st.success(f"Your Location:\nLatitude: {coords['latitude']}, Longitude: {coords['longitude']}")

    # Create map centered at user location
    m = folium.Map(location=[coords["latitude"], coords["longitude"]], zoom_start=15)
    folium.Marker(
        [coords["latitude"], coords["longitude"]],
        popup="You are here",
        tooltip="Your Location",
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(m)

    st_folium(m, width=700, height=500)
else:
    st.warning("Waiting for location access... Please allow it in your browser.")
