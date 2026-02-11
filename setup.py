import os
import gui_v2

if not os.path.exists("tracking/sats.db"):
    print("sats.db not found; creating from sats.sql...")
    os.system("sqlite3 tracking/sats.db < tracking/sats.sql")
    print("Done.")
    print("Launching GUI...")
    gui_v2.run()

gui_v2.run()