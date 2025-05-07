import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="User Location", layout="wide")
st.title("📍 Get Your Current Location")

# Placeholder for location
location = st.empty()

# Create JS to get location from browser
st.markdown("""
<script>
navigator.geolocation.getCurrentPosition(
    function(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const coords = lat + "," + lon;
        const el = window.parent.document.querySelector('input[data-testid="stTextInput"]');
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
        nativeInputValueSetter.call(el, coords);
        el.dispatchEvent(new Event('input', { bubbles: true }));
    }
);
</script>
""", unsafe_allow_html=True)

# Create hidden text input to receive coords from JS
coords = st.text_input("Your coordinates", label_visibility="collapsed")

if coords:
    lat, lon = map(float, coords.split(","))
    location.success(f"Latitude: {lat}, Longitude: {lon}")

    # Show map
    m = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], tooltip="You are here").add_to(m)
    st_folium(m, width=700, height=500)
else:
    st.info("Waiting for your location... Please allow location access in your browser.")
