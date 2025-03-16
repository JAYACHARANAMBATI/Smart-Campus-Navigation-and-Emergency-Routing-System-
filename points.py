from flask import Flask
import folium

app = Flask(__name__)

# Hardcoded data
locations = [
    {"name": "1st block", "lat": 9.57451, "lng": 77.67424},
    {"name": "4th block", "lat": 9.57552, "lng": 77.67585},
    {"name": "5th block", "lat": 9.57398, "lng": 77.67574},
    {"name": "6th block", "lat": 9.57246, "lng": 77.67586},
    {"name": "7th block", "lat": 9.57407, "lng": 77.67387},
    {"name": "8th block", "lat": 9.57479, "lng": 77.67534},
    {"name": "9th block", "lat": 9.57447, "lng": 77.67464},
    {"name": "10th block", "lat": 9.57404, "lng": 77.67483},
    {"name": "11th block", "lat": 9.573, "lng": 77.67548},
    {"name": "staff quarters", "lat": 9.57499, "lng": 77.67974},
    {"name": "ground", "lat": 9.57585, "lng": 77.67602},
    {"name": "temple", "lat": 9.57621, "lng": 77.67967},
    {"name": "mh3", "lat": 9.57141, "lng": 77.6753},
    {"name": "mh4", "lat": 9.57363, "lng": 77.67812},
    {"name": "mh6", "lat": 9.57422, "lng": 77.67779},
    {"name": "Ladies Hostel", "lat": 9.57589, "lng": 77.68157},
    {"name": "Admin block", "lat": 9.57426, "lng": 77.67612},
    {"name": "Mani mandapam", "lat": 9.57504, "lng": 77.67668},
    {"name": "Library", "lat": 9.57453, "lng": 77.67873},
    {"name": "Polytec", "lat": 9.57374, "lng": 77.67093},
    {"name": "IRC", "lat": 9.57418, "lng": 77.67878},
    {"name": "Swimming Pool", "lat": 9.57664, "lng": 77.67949},
    {"name": "K.S.Auditorium", "lat": 9.57505, "lng": 77.67732},
    {"name": "Hospital", "lat": 9.57394, "lng": 77.68306},
]

def create_map_with_markers(locations):
    """Create a map and add markers for each location."""
    # Center the map at an average location
    m = folium.Map(location=[9.57451, 77.67424], zoom_start=15)
    
    # Add markers for each location
    for loc in locations:
        folium.Marker(
            [loc['lat'], loc['lng']], 
            popup=loc['name'],
            tooltip=loc['name']
        ).add_to(m)
    
    return m

@app.route('/')
def index():
    # Add a simple link to navigate to the map
    return '<a href="/map">Go to Map</a>'

@app.route('/map')
def map_view():
    # Create map with markers
    map_with_markers = create_map_with_markers(locations)
    
    # Render map as HTML
    return map_with_markers._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)
