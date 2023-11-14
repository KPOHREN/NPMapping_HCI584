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


#defs at top
def geocode_place(place_name): #MAY NOT NEED ANYMORE
    base_url = "https://geocode.maps.co/search"  # free geocoding service, w/o need for API key!
    params = {"q": place_name}
    
    response = requests.get(base_url, params=params)
    print(response.url)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            # Extract latitude and longitude from the first result
            result = data[0]
            lat = result.get("lat")
            lon = result.get("lon")
            return lat, lon
    
    # Return None if no data or an error occurred
    return None, None

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

@app.route('/', methods=['GET', 'POST'])
def city_location():
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
            
            #html = '<h1>This is your location</h1>'
            #html += '<p>This is a picture of an Excavator.</p>'
            #html += '<img src="/static/test.jpg" alt="excavator image" width="200" height="200">'
            #popup_test = folium.Popup(html, max_width=300)    # Don't use iframe or the img won't work (not sure why)

            # add a marker for user location
            folium.Marker([lat, lon], popup="Your Location", tooltip="Your Location", icon=folium.Icon(color='purple')).add_to(my_map)
            
            for index, row in sorted_df.iterrows():
                #adding plot
                image_name = row['pname']
                parkname = row['ParkName']
                
                html = f'<h1> {parkname} </h1>'
                html += '<p>Link to NP Website: https://www.nps.gov/acad/index.htm .</p>'
                html += '<p>Average Precipitation data: .</p>'
                html += f'<img src="precip/{image_name}" alt="Precipitation Plot:" width="200">'
                html += '<p>Average Temperature data: .</p>'
                html += '<img src="static/precipplot_AcadiaNationalPark.png" alt="Temperature Plot:" width="200">'
                popup_test = folium.Popup(html, max_width=300)  
                
                folium.Marker([row['parklat'], row['parklon']], 
                popup=popup_test, 
                tooltip=(row['ParkName'],"Miles from you:", row['miles']), 
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

    
#read in temp data
dft = pd.read_csv('tempdata.csv')

#comment out as not needed to run everytime
#for index, row in dft.iterrows():
    #category = row['park']
    #values = row.drop('park')
    
    # Create a bar plot for the current row
    #plt.bar(values.index, values)
    #plt.title(f'Temperature in {category}')
    
    # Adjust the plot layout
    #plt.tight_layout()
    
    # Define the filename for the current plot
    #filename = f'plot_{category}.png'
    
    # Save the plot as an image
    #plt.savefig(filename)
    
    # Close the plot to release resources
    #plt.close()
   
#read precipdata
dfp = pd.read_csv('precipdata.csv')

#for index, row in dfp.iterrows():
    #category = row['park']
    #values = row.drop('park')
    
    # Create a bar plot for the current row
    #plt.bar(values.index, values)
    #plt.title(f'Precipitation in inches for {category}')
    
    # Adjust the plot layout
    #plt.tight_layout()
    
    # Define the filename for the current plot
    #filename = f'precipplot_{category}.png'
    
    # Save the plot as an image
    #plt.savefig(filename)
    
    # Close the plot to release resources
    #plt.close()

