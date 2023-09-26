#MainCode


#Import all needs
import pandas as pd
import requests
import math

#Ask User for inital location
#startloc = input("Please enter your city and state abreviation")

##todo - CHECK that city and state are in a valid format

#pulls starting location for lat/lon

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

place_name = "Dubuque, IA"
lat, lon = geocode_place(place_name)

if lat is not None and lon is not None:
    print(f"Location: {place_name}")
    print(f"Latitude: {lat}")
    print(f"Longitude: {lon}")
    startlat = float(lat)
    startlon = float(lon)
else:
    print(f"Geocoding for {place_name} not found or an error occurred.")
    

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

#calculate home location to acadia national park
acadia_lat = float(44.3386)
acadia_lon = float(-68.2733)


#Todo - Add in the lat/lon of all national parks and find the distances
#Then sort them so only the top three are selected 

distance = haversine_distance(startlat, startlon, acadia_lat, acadia_lon)
print("The distance between", place_name, "and Acadia National park is", distance, "miles")

#read in Nat Park Locations
df = pd.read_csv('npdata.csv')
print(df)

#Enter National Park Name to find location to
park = input("Enter the national park you would like to find the distance to:")

#Testing out pulling locations from csv - FAILING
#nplat = df[df['parklat'] == 'Arches National Park']
#nplon = df[df['parklon'] == 'Arches National Park']

#print(parklat, parklon)
