#MainCode


#Import all needs
import pandas as pd
import requests
import math
import matplotlib.pyplot as plt 

#Ask User for inital location
place_name = input("Please enter your city & state abreviation (ie. Ames, IA)")

##todo - CHECK that city and state are in a valid format

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

#place_name = "Dubuque, IA"
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

#read tempdata
dft = pd.read_csv('tempdata.csv')
    
#read precipdata
dfp = pd.read_csv('precipdata.csv')
    

# magSource is the agency (seismic network) that measured the quake's magnitude
cnt = dft["Acadia National Park"]

cnt.plot(   kind='bar',   # vertical
                #kind="barh",  # horizontal 
                ax=None,
                figsize=(10, 5),
                title="Temperature of Acadia National Park" );
fig = p.get_figure()
fig.savefig("acadia.pdf")

    
#read in Nat Park Locations
df = pd.read_csv('npdata.csv')

#create new column to iterate through finding the distance to all parks
df["miles"] = 0

for i,row in df.iterrows(): 
    lat = df.at[i,"parklat"]
    lon = df.at[i,"parklon"]
    distance = haversine_distance(startlat, startlon, lat, lon)
    df.loc[i, "miles"] = distance 

#print(df.nsmallest(3, 'miles'))

#sort by the closests parks and print out those names
sorteddf = df.sort_values(by=['miles'])
nearpark = sorteddf.at[27,"ParkName"] #Fix from hardcode to pull out index values of min
nextpark = sorteddf.at[17,"ParkName"]
farpark = sorteddf.at[28,"ParkName"]

print(sorteddf)
print("The closest parks are:", nearpark, nextpark, farpark)

