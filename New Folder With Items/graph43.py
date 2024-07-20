import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import os
import time

# Function to read JSON file and return data
def read_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

# Function to generate and save plot
def generate_and_save_plot(data, save_dir):
    if data is not None:
        # Extract relevant information
        timestamps = [entry["local_time"] for entry in data["stations"]]
        wind_speeds_kt = [int(entry["wind_speed"]["speed_knots"]) for entry in data["stations"]]
        wind_directions = [int(entry["wind_speed"]["direction_degrees"]) for entry in data["stations"]]
        description = data["stations"][0]["description"]

        # Convert timestamps to datetime objects
        times = [datetime.fromisoformat(ts) for ts in timestamps]

        # Create a DataFrame for easy sorting
        df = pd.DataFrame({'Time': times, 'Wind Speed (kt)': wind_speeds_kt, 'Wind Direction (degrees)': wind_directions})

        # Sort DataFrame by time
        df = df.sort_values(by='Time')

        # Plotting
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Plot the wind speed data
        color = 'tab:blue'
      
        latest_observation_time = max(df['Time']).strftime("%H:%M")
        ax1.set_xlabel(f'Latest Observation at {latest_observation_time}: {wind_speeds_kt[-1]} knots, {data["stations"][-1]["wind_speed"]["direction"]}')


        ax1.set_ylabel('Wind Speed (kt)', color=color)
        ax1.plot(df['Time'], df['Wind Speed (kt)'], marker='o', linestyle='-', color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        # Create a secondary y-axis for wind direction
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Wind Direction', color=color)
        ax2.plot(df['Time'], df['Wind Direction (degrees)'], marker='x', linestyle='', color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        # Set x-axis limits
        start_time = min(df['Time'])
        end_time = max(df['Time']) + timedelta(minutes=50)
        ax1.set_xlim(min(df['Time']).replace(hour=0, minute=0), min(df['Time']).replace(hour=23, minute=50))



        # Set y-axis limits
        ax1.set_ylim(0, 30)
        ax2.set_ylim(0, 360)

        # Add grid lines
        ax1.grid(True)

        # Set fixed increments for secondary y-axis
        ax2.yaxis.set_major_locator(ticker.FixedLocator([0, 45, 90, 135, 180, 225, 270, 315, 360]))

        # Add custom labels for secondary y-axis
        custom_labels = {0: 'N', 45: 'NE', 90: 'E', 135: 'SE', 180: 'S', 225: 'SW', 270: 'W', 315: 'NW', 360: 'N'}
        ax2.yaxis.set_major_formatter(ticker.FixedFormatter([custom_labels.get(tick, '') for tick in [0, 45, 90, 135, 180, 225, 270, 315, 360]]))

        # Set title
        plt.title(f"{description} Wind Speed/Direction for {datetime.now().strftime('%d %B')}")

        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save plot to folder
        save_path = os.path.join(save_dir, "st_wind_png.png")
        plt.savefig(save_path)
        plt.close()
    else:
        print("Data is not available. Skipping plot generation.")

# Main loop to run every minute
current_dir = os.getcwd()
if not os.path.exists("plots_folder"):
    os.makedirs("plots_folder")

while True:
    # Read JSON file
    data = read_json_file(os.path.join(current_dir, "wind_st.json"))

    # Generate and save plot
    generate_and_save_plot(data, "plots_folder")

    # Wait for 1 minute
    time.sleep(60)

