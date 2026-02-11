from skyfield.api import load, wgs84
import time
import os
import sqlite3
from . import geocode

def init(address=None, sat_select=None, stop_event=None):
 
    try:
        os.remove('gp.php')
    except FileNotFoundError:
        print("gp.php not found; proceeding...")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "sats.db")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Show available satellites dynamically
    print("Available satellites:")
    cursor.execute("SELECT sat_select, sat_name FROM satellites ORDER BY sat_select")

    
    if not sat_select:
        sat_select = input("Enter selection: ")
    else:
        print(f"Using provided satellite selection: {sat_select}")

    # Database lookup
    cursor.execute(
        "SELECT sat_id, sat_name FROM satellites WHERE sat_select = ?",
        (sat_select,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        print("Invalid selection.")
        return

    sat_id, sat_name = row

    # Load TLEs
    stations_url = (
        f'https://celestrak.org/NORAD/elements/gp.php?CATNR={sat_id}&FORMAT=TLE'
    )
    sats = load.tle_file(stations_url)
    sat = sats[0]

    # Location
    try:
        if not address:
            res = geocode.geocode_address()
        else:
            res = geocode.geocode_address(address)
    except TypeError:
        # Some runtime versions of the module may have a no-argument geocode_address;
        # fall back to calling it without parameters and notify the user.
        print("Note: geocode.geocode_address() does not accept an address argument in this process; prompting for address.")
        res = geocode.geocode_address()

    if not res:
        print("Unable to determine location; aborting.")
        return

    lat, lon, elev = res
    location = wgs84.latlon(lat, lon, elev)
    
    ts = load.timescale()
    mainloop(sat, location, ts, sat_name, lat, lon, elev, stop_event)


def mainloop(sat, location, ts, sat_name, lat, lon, elev, stop_event):
    print("Commencing tracking...")
    time.sleep(2)
    clear()
    
    while not stop_event.is_set():
        t = ts.now()
        difference = sat - location
        topocentric = difference.at(t)

        elevation, azimuth, distance = topocentric.altaz()

        print(f"{sat_name}: Azimuth: {azimuth.degrees:.2f}°  Elevation: {elevation.degrees:.2f}° Distance: {distance.km:.2f} km")
        print(f"Time (UTC): {t.utc_strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Location: Lat {lat:.6f}°, Lon {lon:.6f}°, Elev {elev} m")
        time.sleep(0.5)
        clear()
    print("Tracking stopped.")

def fetch(sat, location, ts, sat_name):
    t = ts.now()
    difference = sat - location
    topocentric = difference.at(t)

    elevation, azimuth, distance = topocentric.altaz()

    return elevation, azimuth, distance, sat_name

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    init()