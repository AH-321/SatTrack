from geopy.geocoders import Nominatim
import requests

def geocode_address(address=None):
    if not address:
        address = input("Enter address: ")

    geolocator = Nominatim(user_agent="OptiByte-SatTrack")
    location = geolocator.geocode(address)

    if not location:
        print("Location not found.")
        return None

    lat = location.latitude
    lon = location.longitude
    elev = get_elevation(lat, lon)

    return lat, lon, elev


def get_elevation(lat, lon):
    url = f"https://api.opentopodata.org/v1/aster30m?locations={lat},{lon}"

    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        return data['results'][0]['elevation']
    except Exception as e:
        print(f"Elevation error: {e}")
        return 0
    