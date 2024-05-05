import json
import folium
import requests

# Read the JSON lines file and parse data
data = []
with open('bookings.jsonl', 'r') as file:
    for line in file:
        record = json.loads(line)
        data.append(record)

# Extract arrest locations
arrest_locations = [record["arrest location"] for record in data]

# Initialize a map centered at the first arrest location
mymap = folium.Map(location=[35.7796, -78.6382], zoom_start=10)

# Function to geocode address using Google Maps Geocoding API
def geocode_address(address):
    api_key = 'YOUR_GOOGLE_MAPS_API_KEY'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        if result['status'] == 'OK':
            location = result['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None

# Add markers for each arrest location
for address in arrest_locations:
    location = geocode_address(address)
    if location:
        folium.Marker(location=[location[0], location[1]], popup=address).add_to(mymap)

# Save the map to an HTML file
mymap.save("arrest_locations_map.html")
