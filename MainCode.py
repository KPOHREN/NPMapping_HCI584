#MainCode

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

#calculate distance between two locations
def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Radius of the Earth in kilometers
    earth_radius = 3958.8  # You can also use 3958.8 miles for distance in miles

    #Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate the distance
    distance = round(earth_radius * c)

    return distance

app = Flask(__name__)

#Launch Flask App
@app.route('/', methods=['GET', 'POST'])
def city_location():
    #ask user for location and pull in
    if request.method == 'POST':
        city = request.form.get('city')
        state = request.form.get('state')

        # Use a geocoding service to convert the city and state into coordinates
        response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={city},+{state}")
        data = response.json()

        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            
            #read in Nat Park Locations
            df = pd.read_csv('npdata.csv')

            #create new column to iterate through finding the distance to all parks
            df["miles"] = 0

            for i,row in df.iterrows(): 
                latnew = df.at[i,"parklat"]
                lonnew = df.at[i,"parklon"]
                distance = haversine_distance(lat, lon, latnew, lonnew)
                df.loc[i, "miles"] = distance 

            #sort by the closests parks and print out those names
            sorted_df = df.sort_values(by=['miles'])

            #re-indexing the df so that the closest park is at row 0
            sorted_df = sorted_df.reset_index(drop=True)
            
            # Create a Folium map centered at the city's location
            my_map = folium.Map(location=[lat, lon], zoom_start=5)

            # add a marker for user location
            folium.Marker([lat, lon], popup="Your Location", tooltip="Your Location", icon=folium.Icon(color='purple')).add_to(my_map)
            
            for index, row in sorted_df.iterrows():
                #adding plot
                image_name = row['pname']
                tempplot=row['tname']
                parkname = row['ParkName']
                
                #Popup information for each park
                html = f'<h1> {parkname} </h1>' #ParkName Title
                html += '<p>Link to NP Website: https://www.nps.gov/index.htm </p>' #TODO - add in specific links
                html += '<p>Average Precipitation data: </p>'
                html += f'<img src="static/{image_name}" alt="Precipitation Plot:" width="380">' #Precipitation Plot
                html += '<p>Average Temperature data: </p>'
                html += f'<img src="static/{tempplot}" alt="Temperature Plot:" width="440">' #Temperature Plot
                popup_test = folium.Popup(html, max_width=450)  #Saving popup & determining width
                
                #Marker when hoover over pops up distance
                folium.Marker([row['parklat'], row['parklon']], 
                popup=popup_test, 
                tooltip=(row['ParkName'],": Miles from you:", row['miles']), 
                icon=folium.Icon(color='green')).add_to(my_map)

    
            return my_map._repr_html_()

    return '''
        <form method="post">
            <label for="city">City:</label>
            <input type="text" id="city" name="city" required>
            <br>
            <label for="state">State Abbreviation:</label>
            <input type="text" id="state" name="state" required>
            <br>
            <input type="submit" value="Find National Parks">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=False)
