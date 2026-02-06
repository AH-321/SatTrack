# OptiByte SatTrack

Lightweight Python satellite tracker (GUI + CLI) for computing azimuth, elevation, and distance from TLE data.

## Features
- Computes satellite azimuth/elevation/distance using TLEs and Skyfield.
- Tkinter GUI and a CLI tracker for interactive use.
- Optional serial output for Arduino/servo control (CSV `az,elev\n`).

## Quick start
1. Install dependencies:

```bash
python -m pip install -r requirements.txt
# If you encounter serial errors, install pyserial explicitly:
# pip install pyserial
```

2. Create the satellite DB once (sqlite):

```bash
sqlite3 tracking/sats.db < tracking/sats.sql
```

3. Run the GUI:

```bash
python gui.py
```

4. Or run the CLI tracker:

```bash
python cli.py
```

## Files & Structure
- `main.py` — top-level entry (starts the GUI by default). DEPRECATED
- `gui.py` / `gui_v2.py` — Tkinter UI implementations.
 - `gui.py` / `gui_v2.py` — Tkinter UI implementations. Note: `main.py` has been removed; use `gui.py` or `gui_v2.py` to start the GUI.
- `tracking/tracker.py` — core tracking logic, TLE fetch, and compute loop.
- `tracking/geocode.py` — geocoding and elevation helper.
- `tracking/sats.sql` — SQLite schema and initial satellite list.
- `controller/controller.ino` — Arduino sketch example expecting `az,elev\n` on serial.

## Architecture & Data Flow
- The GUI calls `tracker.init()` to select a satellite and start tracking.
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
- Mode selection bug: some code compares `input()` directly to an `int`. If you see incorrect behavior, convert input to int (`mode = int(mode)`) or compare to string (`'1'`).
 - Some legacy code may reference the removed `main.py`; be cautious when refactoring.
- Ensure `tracking/sats.db` exists before running; create it with the `sqlite3` command above.
- `requirements.txt` uses `pyserial`; installing it resolves serial issues.

## Development Tips
- To run the tracker headlessly, inspect `tracking/tracker.py` and refactor `tracker.init()` to return `(sat, location, ts, sat_name)`.
- Add a small bootstrap script to create `tracking/sats.db` from `tracking/sats.sql` for smoother setup.

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
