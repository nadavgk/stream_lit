import streamlit as st
from google_places_finder import load_config, find_nearby_places, open_google_maps
from jpg_coordinates_extractor import process_image
import os
import tempfile

st.title("JPG to Google maps")
st.markdown("Pinpoint the location of your JPG on google maps and find nearby establishments of your choice")

# Step 1: Upload JSON Configuration File (optional)
st.header("Step 1: API Configuration")
uploaded_file = st.file_uploader("Upload JSON File containing your Google **API-KEY** (optional)", type=["json"])
google_api_key = None
if uploaded_file:
    config = load_config(uploaded_file)
    if config:
        google_api_key = config.get('GOOGLE_API_KEY')
        if not google_api_key:
            st.warning("Google API Key not found in the configuration file. You can still proceed without it but the application is limited.")
st.markdown("#without an api-key the web browser will still open Google maps on the specified location but without street-view or nearby establishments")


# Step 2: Ask if the user wants to use a JPG image for coordinates
st.header("Step 2: Coordinates Source")

use_jpg_coords = st.checkbox("**Use coordinates from JPG file**")
st.write("*Not all JPG files have GPS data. good thing you have an app that can check for you!")
# st.markdown("Not all JPG files have GPS data. good thing you have an app that can check for you!")

latitude = None
longitude = None
coordinates_extracted = False

if use_jpg_coords:
    uploaded_jpg = st.file_uploader("Upload JPG File", type=["jpg", "jpeg"])
    if uploaded_jpg:
        try:
            temp_dir = tempfile.mkdtemp() # This creates a temporary directory on a streamlite server so that jpg file can be saved on it and opened to check for its metadata
            jpg_path = os.path.join(temp_dir, uploaded_jpg.name)
            with open(jpg_path, "wb") as f:
                f.write(uploaded_jpg.getbuffer())

            latitude, longitude = process_image(jpg_path)
            st.success(f"Coordinates extracted from JPG: {latitude}, {longitude}")
            coordinates_extracted = True
        except Exception as e:
            st.error(f"Error extracting coordinates: {e}")
else:
    st.markdown("")
    st.markdown("You can also enter coordinates **manually** instead of using a JPG or if you cant find a jpg image with GPS data")
    latitude = st.number_input("**Enter Latitude**", value=40.748817, format="%.6f")
    longitude = st.number_input("**Enter Longitude**", value=-73.985428, format="%.6f")

# Step 3: Select place type and radius
st.header("Step 3: choose a Type of Establishment you would like to find around your specified location")
place_type = st.selectbox(
    "**Select Establishment Type**",
    ["restaurant", "gas_station", "cafe", "hospital", "hotel", "park", "store"]
)

radius = st.number_input("**Enter distance radius from location** (in meters)", value=1500, min_value=100, max_value=50000, step=100)

# Step 4: Find Nearby Places
st.header("Step 4: Open Location on Google maps")
st.markdown("Google maps will open in browser and a list of nearby establishments will appear here")
if st.button("**Open the map**"):
    if not coordinates_extracted and not (latitude and longitude):
        st.error("Please provide coordinates either by uploading a JPG file or by entering them manually.")
    else:
        if google_api_key:
            nearby_places = find_nearby_places(latitude, longitude, place_type, google_api_key)

            if nearby_places:
                st.write(f"Nearby {place_type.capitalize()}s:")
                for place in nearby_places:
                    st.write(f"{place['name']} - {place['vicinity']}")

            else:
                st.write("No nearby places found.")
        else:
            st.warning("No API Key provided. Displaying map only with the provided coordinates.")

        open_google_maps(latitude, longitude, google_api_key)