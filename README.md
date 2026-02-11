# OptiByte SatTrack

Lightweight Python satellite tracker (GUI + CLI) for computing azimuth, elevation, and distance from TLE data.

## Features
- Computes satellite azimuth/elevation/distance using TLEs and Skyfield.
- Tkinter GUI and a CLI tracker for interactive use.
- Optional serial output for Arduino/servo control (CSV `az,elev\n`).

## Quick start
### Windows

1. Simply run `setup.ps1` (can also be run for repairs)

### Unix-like

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
# If you encounter serial errors, install pyserial explicitly:
# pip install pyserial
```

2. Run setup sript (can also be run for repairs):

```bash
python setup.py
```

3. Run the GUI (v2.0):

```bash
python gui_v2.py
```

4. Or run the CLI tracker:

```bash
python cli.py
```

## Files & Structure
- `gui_v2.py` — Current Tkinter UI implementation (recommended).
- `gui.py` — Legacy GUI implementation (DEPRECATED).
- `cli.py` — CLI tracker entry point for interactive satellite tracking.
- `tracking/tracker.py` — core tracking logic, TLE fetch, and compute loop.
- `tracking/geocode.py` — geocoding and elevation helper.
- `tracking/sats.sql` — SQLite schema and initial satellite list.
- `controller/controller.ino` — Arduino sketch example expecting `az,elev\n` on serial.

## Architecture & Data Flow
- The GUI (`gui_v2.py`) calls `tracker.init()` to start tracking. If no values for `address` or `sat_select` are passed by `gui_v2.py`, you will be prompted for entries.
- The CLI (`cli.py`) provides an interactive command-line interface for tracking.
- `tracker` fetches TLE data from Celestrak and uses Skyfield to compute az/el/distance.
- `geocode` uses `geopy` (Nominatim) and OpenTopoData for elevation.
- Optional serial output sends CSV `az,elev\n` to an Arduino at 9600 baud.

## External Services
- Celestrak TLE URL used: `https://celestrak.org/NORAD/elements/gp.php?CATNR={sat_id}&FORMAT=TLE`
- Nominatim (geopy) for geocoding; OpenTopoData for elevation data.

## Hardware
- The Arduino/servo controller expects CSV `az,elev\n` over serial at 9600.
 - See `controller/controller.ino` for the example sketch.

## Known Issues & Notes
- Interactive flow: `tracker.init()` is interactive using `input()` and may be refactored for non-interactive usage.
- Ensure `tracking/sats.db` exists before running; create it with the setup script mentioned above, or by using this command:
  ```bash
  sqlite3 tracking/sats.db < tracking/sats.sql
  ```
- `requirements.txt` uses `pyserial`; installing it resolves serial issues.
- `gui.py` is deprecated; use `gui_v2.py` instead.

## Development Tips
- To run the tracker headlessly, inspect `tracking/tracker.py` and refactor `tracker.init()` to return `(sat, location, ts, sat_name)`.

## Contributing
- Fork, branch, and open a PR. Keep changes minimal and focused.

## License Summary (ANCSL v1.0)

This project is free to use, modify, and share for non-commercial purposes.

It is intended for learning, experimentation, and collaboration within the
amateur radio community, including individual operators, clubs, and
educational or non-profit organizations.

You are welcome to:
- Run the software for personal or club use
- Study how it works and modify it
- Share it with others, including modified versions

You may NOT:
- Sell this software or modified versions of it
- Include it in a commercial product or paid service
- Use it as part of a for-profit offering without permission

If you are interested in using this project in a commercial context,
please contact the author to discuss licensing options.

This summary is provided for convenience only. The full license terms are
contained in the LICENSE file and are legally binding.
