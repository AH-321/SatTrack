import os
import gui_v2

if os.name == "nt":
    path_create = 'tracking\\sats.db'
    path_exists = 'tracking\\sats.sql'
else:
    path_create = 'tracking/sats.db'
    path_exists = 'tracking/sats.sql'

if not os.path.exists(path_create):
    print("sats.db not found; creating from sats.sql...")
    os.system(f"sqlite3 {path_create} < {path_exists}")
    print("Done.")
    print("Launching GUI...")
    gui_v2.run()
else:
    print(f"'{path_create}' already exists.")