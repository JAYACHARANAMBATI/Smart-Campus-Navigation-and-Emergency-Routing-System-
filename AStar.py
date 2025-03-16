import requests
import folium
import heapq
from flask import Flask, render_template, request

app = Flask(__name__)

# Google API Key (replace with your actual key)
API_KEY = "AIzaSyAuztYp_zDh2alDvuLf29evH9CS7Ubvn9M"

# Predefined locations (destination options)
locations = {
    "1st block": (9.57451, 77.67424),
    "4th block": (9.57552, 77.67585),
    "5th block": (9.57398, 77.67574),
    "6th block": (9.57246, 77.67586),
    "7th block": (9.57407, 77.67387),
    "8th block": (9.57479, 77.67534),
    "9th block": (9.57447, 77.67464),
    "10th block": (9.57404, 77.67483),
    "11th block": (9.573, 77.67548),
    "staff quarters": (9.57499, 77.67974),
    "ground": (9.57585, 77.67602),
    "temple": (9.57621, 77.67967),
    "mh1": (9.57426, 77.67612),
    "mh3": (9.57141, 77.6753),
    "mh4": (9.57363, 77.67812),
    "mh6": (9.57422, 77.67779),
    "Ladies Hostel": (9.57589, 77.68157),
    "Admin block": (9.57426, 77.67612),
    "Mani mandapam": (9.57504, 77.67668),
    "Library": (9.57453, 77.67873),
    "Polytec": (9.57374, 77.67093),
    "IRC": (9.57418, 77.67878),
    "Swimming Pool": (9.57664, 77.67949),
    "K.S.Auditorium": (9.57505, 77.67732),
    "Hospital": (9.57394, 77.68306)  # Hospital as origin
}

# Set Hospital coordinates as the origin
hospital_coords = locations["Hospital"]

def haversine(coord1, coord2):
    """Calculate the great-circle distance between two points."""
    from math import radians, sin, cos, sqrt, atan2
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371.0  # Radius of the Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def a_star_search(start, goal, locations):
    """A* algorithm to find the shortest path between two points."""
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {location: float('inf') for location in locations.values()}
    g_score[start] = 0
    f_score = {location: float('inf') for location in locations.values()}
    f_score[start] = haversine(start, goal)

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
           
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor_name, neighbor_coords in locations.items():
            tentative_g_score = g_score[current] + haversine(current, neighbor_coords)

            if tentative_g_score < g_score[neighbor_coords]:
                came_from[neighbor_coords] = current
                g_score[neighbor_coords] = tentative_g_score
                f_score[neighbor_coords] = tentative_g_score + haversine(neighbor_coords, goal)
                heapq.heappush(open_set, (f_score[neighbor_coords], neighbor_coords))

    return [] 

def get_live_location(api_key):
    """Fetch live location using Google Geolocation API."""
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}"
    response = requests.post(url)
    if response.status_code == 200:
        location_data = response.json()
        lat = location_data.get('location', {}).get('lat')
        lng = location_data.get('location', {}).get('lng')
        return lat, lng
    else:
        print(f"Error fetching location: {response.status_code}")
        return None, None

def create_map(live_location, hospital_coords, route_points=None, destination_coords=None):
    """Create a map centered on the hospital, with an optional route and live location marker."""
    live_map = folium.Map(location=hospital_coords, zoom_start=15)
    
    
    folium.Marker(hospital_coords, tooltip="Hospital (Origin)", icon=folium.Icon(color="green")).add_to(live_map)
    
    if live_location:
        folium.Marker(live_location, tooltip="Your Live Location", icon=folium.Icon(color="blue")).add_to(live_map)
    
    
    if route_points:
        folium.PolyLine(route_points, color="blue", weight=5, opacity=0.7).add_to(live_map)
        if destination_coords:
            folium.Marker(destination_coords, tooltip="Destination", icon=folium.Icon(color="red")).add_to(live_map)
    
    return live_map

@app.route('/', methods=['GET', 'POST'])
def index():
    
    live_lat, live_lng = get_live_location(API_KEY)
    live_location = (live_lat, live_lng)
    
    
    origin_lat, origin_lng = hospital_coords
    destination_lat = destination_lng = None
    route_points = None
    distance = duration = None
    
    if request.method == 'POST':
        
        destination = request.form.get('destination')
        if destination:
            destination_lat, destination_lng = map(float, destination.split(','))  # Convert destination coordinates to float
            
          
            route_points = a_star_search((origin_lat, origin_lng), (destination_lat, destination_lng), locations)
            
            if route_points:
                print(f"Route Points: {route_points}")  # Debugging route points
                distance = sum(haversine(route_points[i], route_points[i+1]) for i in range(len(route_points) - 1))
                duration = "Unknown duration"  # Placeholder for duration calculation
            else:
                print("No route points found!")

    return render_template('index.html', live_lat=live_lat, live_lng=live_lng,
                           origin_lat=origin_lat, origin_lng=origin_lng, 
                           destination_lat=destination_lat, destination_lng=destination_lng,
                           route_points=route_points, distance=distance, duration=duration,
                           locations=locations)

@app.route('/map')
@app.route('/map')
def map_view():
   
    live_lat, live_lng = get_live_location(API_KEY)
    live_location = (live_lat, live_lng)
    
   
    origin_lat, origin_lng = hospital_coords
    route_points = None
    destination_coords = None
    
    
    destination_lat = request.args.get('destination_lat')
    destination_lng = request.args.get('destination_lng')
    
    if destination_lat and destination_lng:
        try:
            destination_lat = float(destination_lat)
            destination_lng = float(destination_lng)
            
            
            route_points = a_star_search((origin_lat, origin_lng), (destination_lat, destination_lng), locations)
            destination_coords = (destination_lat, destination_lng)
            
            if route_points:
                print(f"Route Points: {route_points}") 
            else:
                print("No route points were found!")
                
        except ValueError:
            print("Invalid destination coordinates provided.")
    
    
    live_map = create_map(live_location, (origin_lat, origin_lng), route_points, destination_coords)
    
 
    print(live_map._repr_html_())
    
    return live_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
