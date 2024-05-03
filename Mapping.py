import json
import requests
import folium

# Function to get latitude and longitude of an address using OpenStreetMap API
def get_lat_lon(address):
    url = f'https://nominatim.openstreetmap.org/search?q={address}&format=json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    return None, None

def main():
    # Read the bookings.jsonl file and extract addresses
    residence_addresses = []    
    arrest_addresses = []
    with open('bookings.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line)
            residence_addresses.append(data['residence address'])
            arrest_addresses.append(data['arrest location'])

    # Create a map objects
    residence_map = folium.Map(location=[0, 0], zoom_start=2)
    arrest_map = folium.Map(location=[0, 0], zoom_start=2)

    # Plot each address on the residence map
    for address in residence_addresses:
        lat, lon = get_lat_lon(address)
        if lat is not None and lon is not None:
            folium.Marker([lat, lon], popup=address).add_to(residence_map)

    # Plot each address on the arrest map
    for address in arrest_addresses:
        lat, lon = get_lat_lon(address)
        if lat is not None and lon is not None:
            folium.Marker([lat, lon], popup=address).add_to(arrest_map)

    # Save the maps to an HTML file
    residence_map.save('residence_map.html')
    arrest_map.save('arrest_map.html')
    print("maps made")

if __name__ == '__main__': 
    main()
