#Import all needs
import pandas as pd
import folium
import requests
import math
import matplotlib.pyplot as plt 
from IPython.display import display
from flask import Flask, render_template, request
import folium
from folium import IFrame
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#read in temp data
dft = pd.read_csv('tempdata.csv')

# Get unique locations in the DataFrame
locations = dft['park'].unique()

# Set the width of each bar
bar_width = 0.4  # Adjust as needed

# Iterate through each location
for location in locations:
    location_df = dft[dft['park'] == location]

    # Create a single plot for each location
    plt.figure(figsize=(10, 6))  # Adjust figure size as needed

    # Get unique months for x-axis positions
    unique_months = location_df['month'].unique()

    # Create x-axis positions for each month
    x_positions = np.arange(len(unique_months))

    # Iterate through each month for the current location
    for i, month in enumerate(unique_months):
        month_df = location_df[location_df['month'] == month]
        high_temp = month_df['hightemp'].values[0]
        low_temp = month_df['lowtemp'].values[0]

        # Create overlapping bars for high and low temperatures
        plt.bar(x_positions[i] - bar_width / 2, high_temp, width=bar_width, color='red')
        plt.bar(x_positions[i] + bar_width / 2, low_temp, width=bar_width, color='blue')

    # Customize the plot
    plt.xlabel('Month')
    plt.ylabel('Temperature (Degrees F)')
    plt.title(f'Average High & Low Temperature for {location} by Month')
    plt.xticks(x_positions, unique_months)  # Set x-axis ticks to month names
    plt.legend()

    # Save each plot as an image
    plt.savefig(f'plot_{location}.png')

    # Close the plot to release resources
    plt.close()