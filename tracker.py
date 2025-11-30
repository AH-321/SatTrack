from skyfield.api import load, wgs84
import time
import os

def init():

    print('''Available satellites:
          1: NOAA 8
          2: NOAA 19''')
    sat_select = input("Enter selection:")
    
    # Sattellite table
    if sat_select == "1":
        sat_id = 13923
        sat_name = 'NOAA 8'
    elif sat_select == "2":
        sat_id = 33591
        sat_name = 'NOAA 19'

    # Load TLEs
    stations_url = f'https://celestrak.org/NORAD/elements/gp.php?CATNR={sat_id}&FORMAT=TLE'
    sats = load.tle_file(stations_url)
    sat = sats[0]

    # Location
    lat = 50.6949201     # SA
    lon = -119.248787
    elevation = 526
    location = wgs84.latlon(lat, lon, elevation)

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

        print(f"{sat_name}: Azimuth: {az.degrees:.2f}°  Elevation: {alt.degrees:.2f}°")

        time.sleep(0.1)
        os.system('cls' if os.name == 'nt' else 'clear')



if __name__ == "__main__":
    init()

