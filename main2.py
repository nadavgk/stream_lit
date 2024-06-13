import streamlit as st
from google_places_finder2 import load_config, find_nearby_places, open_google_maps
from jpg_coordinates_extractor2 import process_image
import os
import tempfile

st.title("Google Places Finder")

# Step 1: Upload JSON Configuration File (optional)
st.header("Step 1: API Configuration")
uploaded_file = st.file_uploader("Upload JSON Configuration File (optional)", type=["json"])
google_api_key = None
if uploaded_file:
    config = load_config(uploaded_file)
    if config:
        google_api_key = config.get('GOOGLE_API_KEY')
        if not google_api_key:
            st.warning("Google API Key not found in the configuration file. You can still proceed without it.")

# Step 2: Ask if the user wants to use a JPG image for coordinates
st.header("Step 2: Coordinates Source")
use_jpg_coords = st.checkbox("Use coordinates from JPG file")

latitude = None
longitude = None
coordinates_extracted = False

if use_jpg_coords:
    uploaded_jpg = st.file_uploader("Upload JPG File", type=["jpg", "jpeg"])
    if uploaded_jpg:
        try:
            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()
            # Define the path to save the uploaded JPG file
            jpg_path = os.path.join(temp_dir, uploaded_jpg.name)
            # Write the uploaded JPG file to the temporary directory
            with open(jpg_path, "wb") as f:
                f.write(uploaded_jpg.getbuffer())

            latitude, longitude = process_image(jpg_path)
            st.success(f"Coordinates extracted from JPG: {latitude}, {longitude}")
            coordinates_extracted = True
        except Exception as e:
            st.error(f"Error extracting coordinates: {e}")
else:
    # Step 3: Enter coordinates manually if not using JPG
    st.header("Step 3: Enter Coordinates Manually")
    latitude = st.number_input("Enter Latitude", value=40.748817, format="%.6f")
    longitude = st.number_input("Enter Longitude", value=-73.985428, format="%.6f")

# Step 4: Select place type and radius
st.header("Step 4: Establishment Type and Radius")
place_type = st.selectbox(
    "Select Place Type",
    ["restaurant", "gas_station", "cafe", "hospital", "hotel", "park", "store"]
)

radius = st.number_input("Enter Radius (in meters)", value=1500, min_value=100, max_value=50000, step=100)

# Step 5: Find Nearby Places
st.header("Step 5: Find Nearby Places")

if st.button("Find Nearby Places"):
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
