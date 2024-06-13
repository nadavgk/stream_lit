import os
import tempfile
import streamlit as st
from jpg_coordinates_extractor import get_jpg_coor
from exif import Image


def process_image(file_path):
    try:
        # Read the file
        with open(file_path, 'rb') as file:
            img = Image(file.read())
        # Extract coordinates using your function
        coordinates = get_jpg_coor(img)
        return coordinates
    except Exception as e:
        st.error(f"An error occurred: {e}")


# Streamlit app
st.title("JPG Coordinates Extractor")

# File uploader
uploaded_file = st.file_uploader("Upload JPG File", type=["jpg", "jpeg"])

if uploaded_file:
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    # Define the path to save the uploaded file
    file_path = os.path.join(temp_dir, uploaded_file.name)

    # Write the uploaded file to the temporary directory
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # Process the saved file
    try:
        coordinates = process_image(file_path)
        st.write("Coordinates extracted from the image:", coordinates)
    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Optionally, remove the temporary file after processing
    os.remove(file_path)
