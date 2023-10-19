#MainCode

# CH this has some edits/suggestions

#Import all needs
import pandas as pd
import folium
import requests
import math
import matplotlib.pyplot as plt 
from IPython.display import display

# CH put all your function defs on top
def geocode_place(place_name):
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

# START of MAIN CODE

#Ask User for initial location
while True:
    place_name = input("Please enter your city & state abbreviation (ie. Ames, IA)")

    ##todo - CHECK that city and state are in a valid format
    # You could do a sanity check on the input sth like a bunch of space separated words, followed by a comma
    # followed by a 2 letter state code but as the geo service will return None if it can't find the place
    # you could just print out an error (and what the correct format needs to be) and the repeat the input

    #place_name = "Dubuque, IA"
    lat, lon = geocode_place(place_name)

    if lat is not None and lon is not None:
        print(f"Location: {place_name}")
        print(f"Latitude: {lat}")
        print(f"Longitude: {lon}")
        startlat = float(lat)
        startlon = float(lon)
        break
    else:
        print(f"Geocoding for {place_name} not found or an error occurred.")
        print("Please try again")


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
    
#read in Nat Park Locations
df = pd.read_csv('npdata.csv')

#create new column to iterate through finding the distance to all parks
df["miles"] = 0

for i,row in df.iterrows(): 
    latnew = df.at[i,"parklat"]
    lonnew = df.at[i,"parklon"]
    distance = haversine_distance(startlat, startlon, latnew, lonnew)
    df.loc[i, "miles"] = distance 

#print(df.nsmallest(3, 'miles'))

#sort by the closests parks and print out those names
sorted_df = df.sort_values(by=['miles'])


# CH re-indexing the df so that the closest park is at row 0
sorted_df = sorted_df.reset_index(drop=True)

'''
# Get the index of rows with the smallest value 
nearpark_index = sorted_df.index[0]
nextpark_index = sorted_df.index[1]
farpark_index = sorted_df.index[2]

#pull out the park names
nearpark = sorted_df.at[nearpark_index,"ParkName"]
nextpark = sorted_df.at[nextpark_index,"ParkName"]
farpark = sorted_df.at[farpark_index,"ParkName"]

#display(sorteddf)

'''
# with the index reset the park names are now at row 0, 1, 2
# you can get a column value for a rown index with iloc
nearpark = sorted_df.iloc[0]['ParkName']
nextpark = sorted_df.iloc[1]['ParkName']
farpark = sorted_df.iloc[2]['ParkName']
print("The closest parks are:", nearpark, ",", nextpark,", and", farpark)

#pull out lat & lon for those parks and add to map
lat1 = sorted_df.iloc[0]['parklat']
lon1 = sorted_df.iloc[0]['parklon']

lat2 = sorted_df.iloc[1]['parklat']
lon2 = sorted_df.iloc[1]['parklon']

lat3 = sorted_df.iloc[2]['parklat']
lon3 = sorted_df.iloc[2]['parklon']

# make a basemap and zoom to an area
m = folium.Map(location=[lat, lon], zoom_start=5)  # Adjust latitude, longitude, and zoom level as needed
folium.Marker([lat, lon], popup="Your Location").add_to(m)
folium.Marker([lat1, lon1], popup="Marker 1").add_to(m)
folium.Marker([lat2, lon2], popup="Marker 2").add_to(m)
folium.Marker([lat3, lon3], popup="Marker 3").add_to(m)

m.save('map.html')