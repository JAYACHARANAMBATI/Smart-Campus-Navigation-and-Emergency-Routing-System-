from flask import Flask, render_template, request, jsonify
import requests
import folium
import smtplib
import os

app = Flask(__name__)

# Load API key from environment variable for security
API_KEY = "AIzaSyAuztYp_zDh2alDvuLf29evH9CS7Ubvn9M"

# Predefined locations on the campus
locations = {
    "Hospital": (9.57394, 77.68306),
    "1st Block": (9.57451, 77.67424),
    "4th Block": (9.57552, 77.67585),
    "5th Block": (9.57398, 77.67574),
    "6th Block": (9.57246, 77.67586),
    "7th Block": (9.57407, 77.67387),
    "8th Block": (9.57479, 77.67534),
    "9th Block": (9.57447, 77.67464),
    "10th Block": (9.57404, 77.67483),
    "11th Block": (9.573, 77.67548),
    "Staff Quarters": (9.57499, 77.67974),
    "Ground": (9.57585, 77.67602),
    "Temple": (9.57621, 77.67967),
    "MH1": (9.57426, 77.67612),
    "MH3": (9.57141, 77.6753),
    "MH4": (9.57363, 77.67812),
    "MH6": (9.57422, 77.67779),
    "Ladies Hostel": (9.57589, 77.68157),
    "Admin Block": (9.57426, 77.67612),
    "Mani Mandapam": (9.57504, 77.67668),
    "Library": (9.57453, 77.67873),
    "Polytec": (9.57374, 77.67093),
    "IRC": (9.57418, 77.67878),
    "Swimming Pool": (9.57664, 77.67949),
    "K.S. Auditorium": (9.57505, 77.67732)
}

hospital_coords = locations["Hospital"]

def get_coordinates_from_address(api_key, address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        geocode_data = response.json()
        if geocode_data['status'] == 'OK':
            location = geocode_data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

def get_route(api_key, origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {"origin": origin, "destination": destination, "key": api_key, "mode": "driving"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        directions_data = response.json()
        if directions_data["status"] == "OK":
            route = directions_data["routes"][0]["legs"][0]
            route_points = [(step["start_location"]["lat"], step["start_location"]["lng"]) for step in route["steps"]]
            route_points.append((route["end_location"]["lat"], route["end_location"]["lng"]))
            distance = route["distance"]["text"]
            duration = route["duration"]["text"]
            return route_points, distance, duration
    return [], None, None

def create_map(origin_coords, live_location=None, route_points=None, destination_coords=None, return_route_points=None):
    map_instance = folium.Map(location=origin_coords, zoom_start=15)
    
    # Marker for origin (Hospital)
    folium.Marker(origin_coords, tooltip="Hospital (Origin)", icon=folium.Icon(color="green")).add_to(map_instance)
    
    # Marker for live location if provided
    if live_location:
        folium.Marker(live_location, tooltip="Your Live Location", icon=folium.Icon(color="blue")).add_to(map_instance)
    
    # Draw outward route in blue
    if route_points:
        folium.PolyLine(route_points, color="blue", weight=5, opacity=0.7, tooltip="Outward Route").add_to(map_instance)
        
    # Draw return route in red if applicable
    if return_route_points:
        folium.PolyLine(return_route_points, color="red", weight=5, opacity=0.7, tooltip="Return Route").add_to(map_instance)
        
    # Marker for destination
    if destination_coords:
        folium.Marker(destination_coords, tooltip="Destination", icon=folium.Icon(color="red")).add_to(map_instance)
    
    # Save the map to a file that will be rendered in the iframe
    map_instance.save("templates/map.html")

def send_email_notification(email_address, email_password, recipient, subject, body):
    try:
        # Establish a secure session with Gmail's outgoing SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login and send email
        server.login(email_address, email_password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(email_address, recipient, message)
        print('Mail sent successfully.')
    except smtplib.SMTPAuthenticationError as e:
        print("Authentication error: Please check your email and password.")
        print("If you have 2-Step Verification enabled, use an App Password instead.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server.quit()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', locations=locations)

@app.route('/get_route', methods=['POST'])
def get_route_ajax():
    destination = request.json.get('destination')
    custom_address = request.json.get('custom_address')
    live_location = request.json.get('live_location')
    return_trip = request.json.get('return_trip', False)

    destination_lat = destination_lng = None
    route_points = distance = duration = None
    return_route_points = None

    # Get destination coordinates from address or pre-defined locations
    if custom_address:
        destination_lat, destination_lng = get_coordinates_from_address(API_KEY, custom_address)
    elif destination in locations:
        destination_lat, destination_lng = locations[destination]

    if destination_lat is not None and destination_lng is not None:
        origin = f"{live_location[0]},{live_location[1]}" if live_location else f"{hospital_coords[0]},{hospital_coords[1]}"
        destination_str = f"{destination_lat},{destination_lng}"

        # Get outward route
        route_points, distance, duration = get_route(API_KEY, origin, destination_str)

        # Get return route if requested
        if return_trip:
            return_route_points, _, _ = get_route(API_KEY, destination_str, origin)

            # Send email notification about the return trip
            email_address = "ambatijayacharan18@gmail.com"
            email_password = "jnzu ewoa orde weyx"  # Keep this in environment variables in production
            recipient = '99220040237@klu.ac.in'
            subject = "Patient is returning"
            body = f"The patient will arrive in approximately {duration} from {destination}."
            send_email_notification(email_address, email_password, recipient, subject, body)

        # Create a map with both outward and return routes
        create_map(hospital_coords, live_location, route_points, (destination_lat, destination_lng), return_route_points)

    return jsonify({
        'distance': distance,
        'duration': duration,
        'route_available': bool(route_points)
    })

@app.route('/map')
def map_view():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
