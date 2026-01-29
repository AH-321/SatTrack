from skyfield.api import load, wgs84
import time
import os
import sqlite3
import geocode

def init():

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
    for sat_select, sat_name in cursor.fetchall():
        print(f"  {sat_select}: {sat_name}")

    sat_select = input("Enter selection: ")

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
    lat, lon, elev = geocode.geocode_address()
    location = wgs84.latlon(lat, lon, elev)

    ts = load.timescale()

    print("Commencing tracking...")
    time.sleep(2)
    main(sat, location, ts, sat_name)


def main(sat, location, ts, sat_name):
    while True:
        t = ts.now()
        difference = sat - location
        topocentric = difference.at(t)

        alt, az, distance = topocentric.altaz()

        print(f"{sat_name}: Azimuth: {az.degrees:.2f}°  Elevation: {alt.degrees:.2f}° Distance: {distance.km:.2f} km")

        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    init()