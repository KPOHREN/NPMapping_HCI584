from flask import Flask, render_template, request
import folium

app = Flask(__name__)

@app.route('/', methods=['GET'])
def map():
        lat = request.args.get('lat', 40)
        lon = request.args.get('lon', -90)
        map = folium.Map(location=[lat, lon], zoom_start=9)

        # add a marker for user location
        folium.Marker([lat, lon],  tooltip="Your Location", popup=f"{lat}\n{lon}").add_to(map)

        map_as_html = map._repr_html_() # covert to html so it can live in a html file
        
        # this will inline the folium html map and the lat/lon values
        return render_template('map.html', map=map_as_html, lat=lat, lon=lon)

if __name__ == '__main__':
    app.run(debug=False)