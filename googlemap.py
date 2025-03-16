import googlemaps

# Initialize Google Maps Client
API_KEY = "AIzaSyDOudVwAfmvxFGEIfW3PHaVR4X-YOkdldo"
gmaps = googlemaps.Client(key=API_KEY)

# Function to get latitude and longitude of a location
def get_coordinates(state_name):
    geocode_result = gmaps.geocode(state_name)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print("Location not found.")
        return None, None

# Function to generate a Google Maps Developer Mode link
def create_google_maps_link(state_name):
    lat, lng = get_coordinates(state_name)
    if lat and lng:
        # Generate a Google Maps link with latitude and longitude
        maps_link = f"https://www.google.com/maps/@{lat},{lng},10z?hl=en&debug=1"
        print(f"Developer Mode Map Link for {state_name}:")
        print(maps_link)
        return maps_link
    else:
        print("Could not generate a map link for the given state.")
        return None

# Input from user
state_name = input("Enter the name of the state: ")
link = create_google_maps_link(state_name)

# Optional: Open the link in a web browser
if link:
    import webbrowser
    webbrowser.open(link)
