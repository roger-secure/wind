import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime, timedelta
import time

# Function to extract wind data from XML
def extract_wind_data():
    while True:
        try:
            # Parse the XML file
            tree = ET.parse("IDV60920.xml")
            root = tree.getroot()

            # Initialize dictionary to store wind data
            wind_data = {"stations": []}

            # Find St Kilda Harbour station
            st_kilda_station = root.find(".//station[@stn-name='ST KILDA HARBOUR - RMYS']")

            if st_kilda_station is not None:
                # Get the local time
                local_time = st_kilda_station.find(".//period").attrib.get("time-local", "")

                # Get description
                description = st_kilda_station.attrib.get("description", "")

                # Get wind gust
                wind_gust_speed_kmh = st_kilda_station.find(".//element[@type='gust_kmh']").text
                wind_gust_speed_knots = st_kilda_station.find(".//element[@type='wind_gust_spd']").text
                wind_gust_direction = st_kilda_station.find(".//element[@type='wind_dir']").text
                wind_gust_direction_degrees = st_kilda_station.find(".//element[@type='wind_dir_deg']").text
                wind_gust = {
                    "speed_kmh": wind_gust_speed_kmh,
                    "speed_knots": wind_gust_speed_knots,
                    "direction": wind_gust_direction,
                    "direction_degrees": wind_gust_direction_degrees
                }

                # Get wind speed
                wind_speed_speed_kmh = st_kilda_station.find(".//element[@type='wind_spd_kmh']").text
                wind_speed_speed_knots = st_kilda_station.find(".//element[@type='wind_spd']").text
                wind_speed_direction = st_kilda_station.find(".//element[@type='wind_dir']").text
                wind_speed_direction_degrees = st_kilda_station.find(".//element[@type='wind_dir_deg']").text
                wind_speed = {
                    "speed_kmh": wind_speed_speed_kmh,
                    "speed_knots": wind_speed_speed_knots,
                    "direction": wind_speed_direction,
                    "direction_degrees": wind_speed_direction_degrees
                }

                # Append data to the dictionary
                wind_data["stations"].append({
                    "local_time": local_time,
                    "description": description,
                    "wind_gust": wind_gust,
                    "wind_speed": wind_speed
                })
            else:
                print("St. Kilda Harbour station not found in the XML.")
            return wind_data
        except Exception as e:
            print(f"Error parsing XML: {e}")
            print("Retrying in 1 minute...")
            time.sleep(60)


# Function to check if it's time to clear observation data
def should_clear_observation_data():
    now = datetime.now()
    return now.hour == 23 and now.minute == 55

# Function to clear observation data from JSON file
def clear_observation_data():
    with open("wind_st.json", "w") as f:
        json.dump({"stations": []}, f, indent=2)
    print("Observation data cleared at 23:55 local time.")



# Main loop for adding data every 1 minute
while True:
    # Extract wind data from XML
    new_data = extract_wind_data()

 # Check if it's time to clear observation data (00:20 local time)
    if datetime.now().hour == 00 and datetime.now().minute == 20:
        clear_observation_data()

    # Load existing data from JSON file if it exists
    existing_data = {}
    if os.path.exists("wind_st.json"):
        with open("wind_st.json", "r") as f:
            existing_data = json.load(f)

    # Check if new data already exists in existing data
    for station_data in new_data["stations"]:
        new_local_time = station_data["local_time"]
        if any(existing_data_station["local_time"] == new_local_time for existing_data_station in existing_data.get("stations", [])):
            print("Data already exists for local time:", new_local_time)
        else:
            # Append new data to existing data
            existing_data["stations"].append(station_data)
            print("New data added for local time:", new_local_time)

    # Write updated data to JSON file
    with open("wind_st.json", "w") as f:
        json.dump(existing_data, f, indent=2)

    # Wait for 1 minute before repeating
    time.sleep(60)  # 1 minute in seconds

