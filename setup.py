import os
import gui_v2

if os.name == "nt":
    path = 'tracking\\sats.db'
else:
    path = 'tracking/sats.db'

if not os.path.exists(path):
    print("sats.db not found; creating from sats.sql...")
    os.system(f"sqlite3 {path} < tracking\\sats.sql")
    print("Done.")
    print("Launching GUI...")
    gui_v2.run()

gui_v2.run()