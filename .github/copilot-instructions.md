# OptiByte-SatTrack AI Agent Instructions

## Project Overview

OptiByte-SatTrack is a **real-time satellite tracking system** that calculates azimuth and elevation angles for weather satellites (NOAA 8/19) and sends corrections to a motorized antenna controller via serial communication.

**Architecture Flow:** `tracker.py` (orbital calculations) → `main.py` (serial output) → Hardware controller

## Core Components & Responsibilities

### `tracker.py` - Orbital Mechanics Engine
- **Purpose:** Real-time satellite position calculations using Skyfield library
- **Key Pattern:** Interactive user selection (1=NOAA 8, 2=NOAA 19) at startup; TLE data fetched dynamically from CelesTrak API
- **Critical Functions:**
  - `init()` - User menu, TLE loading, observer location setup, loop initiation
  - `main(sat, location, ts, sat_name)` - Continuous tracking loop (0.1s refresh rate), topocentric coordinate calculations
- **Hardcoded Location:** Latitude 50.6949201, Longitude -119.248787, Elevation 526m (Kelowna, Canada area)
- **Data Flow:** Skyfield objects (`sat`, `location`, `ts`) → topocentric difference → altaz() conversion → degree values

### `main.py` - Serial Communication Bridge
- **Purpose:** Transmits calculated angles to antenna controller (COM3, 9600 baud)
- **Message Format:** `"{azimuth_degrees},{elevation_degrees}\n"` (two floats, comma-separated, newline-terminated)
- **Execution Pattern:** Imports `az` and `alt` from `tracker` module, runs in infinite loop
- **Hardware Assumption:** Expects COM3 to be available; no error handling currently

### `gp.php` - TLE Data File
- **Purpose:** Cached/fallback TLE (Two-Line Element) data for NOAA 19
- **Format:** Standard NASA TLE format (name, line 1, line 2)
- **Current Data:** NOAA 19 TLE from around day 333 of 2025

### `satellites.sql` - Reserved
- Empty; likely intended for future database integration of satellite catalog

## Development Workflows

### Running the System
1. **Full tracking:** `python main.py` (requires hardware on COM3)
2. **Calculations only:** `python tracker.py` (outputs angles to console, no serial dependency)

### Dependency Management
- Install via: `pip install -r requirements.txt`
- Key libraries: `skyfield` (orbital mechanics), `pyserial` (COM communication)
- **Note:** `requirements.txt` lists `serial` (incorrect); should be `pyserial`

### Satellite Updates
- TLEs are fetched live from CelesTrak API in `tracker.init()`
- Fallback: TLE data exists in `gp.php` for manual updates if API unavailable

## Key Patterns & Conventions

### Coordinate System
- **Azimuth:** Degrees (0°=North, 90°=East, 180°=South, 270°=West)
- **Elevation:** Degrees above horizon (0°=horizon, 90°=zenith)
- **Precision:** `.2f` formatting (2 decimal places) in all outputs

### Loop Timing
- 0.1-second refresh rate in `tracker.main()` for smooth tracking
- Message transmission matches calculation frequency in `main.py`
- Screen clearing logic: `os.system('cls')` for Windows, `clear` for Unix (but may not be critical for serial variant)

### Satellite Selection
- Hardcoded satellite ID mapping: 13923 (NOAA 8), 33591 (NOAA 19)
- User input validation: None currently (assumes valid input 1 or 2)

## Common Issues & Debugging

- **SerialException on COM3:** Verify antenna controller is connected and powered; check Device Manager for correct COM port
- **API failures:** `load.tle_file()` will raise exception if CelesTrak unreachable; consider `gp.php` fallback implementation
- **Timing drift:** Serial buffer might accumulate if hardware controller slower than 0.1s messages

## When Modifying This Codebase

- **Location updates:** Change hardcoded lat/lon in `tracker.init()`, not in separate config (current pattern)
- **Serial format changes:** Update format string in `main.py` AND message parsing expectations in hardware controller firmware
- **New satellites:** Add to satellite selection menu in `tracker.init()` with NORAD catalog number
- **Testing without hardware:** Use `tracker.py` standalone; mock serial output before integrating with `main.py`

## File Relationships

```
main.py
  └─ imports: tracker
  └─ uses: tracker.az, tracker.alt (module-level objects)
  
tracker.py
  └─ imports: skyfield, serial, time, os
  └─ sets global: az, alt (azimuth/elevation angle objects)
  └─ fetches: CelesTrak TLE API, reads gp.php as reference
```

**Important:** `tracker.py` expects to be run as `__main__`, but `main.py` relies on side effects of `tracker.init()` and module-level variable assignments. This coupling should be formalized if extending the codebase.
