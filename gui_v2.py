from tkinter import *
from tracking import tracker
import sqlite3


class SatTrackUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SatTrack v0.5 Alpha")
        self.root.geometry("900x500")
        self.root.minsize(700, 400)

        # ----- Root layout -----
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=0)  # title
        root.rowconfigure(1, weight=1)  # main content
        root.rowconfigure(2, weight=0)  # footer

        # ----- Title -----
        title_frame = Frame(root)
        title_frame.grid(row=0, column=0, pady=15, sticky="n")

        Label(
            title_frame,
            text="Welcome to SatTrack",
            font=("Helvetica", 16, "bold"),
        ).pack()

        # ----- Main content -----
        main_frame = Frame(root)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Data input label
        Label(
            main_frame,
            text="Data Input",
            font=("Helvetica", 12),
        ).grid(row=0, column=0, columnspan=2, pady=(0, 5))

        # Address input
        self.address_input = Text(main_frame, height=4)
        self.address_input.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=(0, 15),
        )

        # Satellite selection
        Label(
            main_frame,
            text="Select Satellite:",
            font=("Helvetica", 12),
        ).grid(row=2, column=0, sticky="e", padx=10)

        # Populate satellite options from database
        try:
            conn = sqlite3.connect('tracking/sats.db')
            cursor = conn.cursor()
        except FileNotFoundError:
            self.panic("sats.db not found; make sure it exists by running "
            "'sqlite3 tracking/sats.db < tracking/sats.sql' in the tracking directory.")
            
        cursor.execute("SELECT sat_select, sat_name FROM satellites ORDER BY sat_select")
        options = [row[1] for row in cursor.fetchall()]
        conn.close()

        self.default_option = StringVar(root)
        self.default_option.set(options[0])

        self.satellite_dropdown = OptionMenu(
            main_frame,
            self.default_option,
            *options,
        )
        self.satellite_dropdown.grid(row=2, column=1, sticky="w", padx=10)

        # Start tracking
        self.start_tracking = Button(
            main_frame,
            text="Start Tracking",
            width=20,
            command=lambda: self.start(),
        )
        self.start_tracking.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=20,
        )

        # ----- Footer -----
        footer_frame = Frame(root)
        footer_frame.grid(row=2, column=0, sticky="se", padx=15, pady=10)

        Label(
            footer_frame,
            text="Version 0.5 Alpha\n2026 OptiByte Systems",
            font=("Helvetica", 10),
            justify="right",
        ).pack()

    def start(self):
        tracker.init(
            self.address_input.get("1.0", "end-1c").strip() or None
        )
        self.root.destroy()

    def panic(self, message):
        panic_window = Toplevel(self.root)
        panic_window.title("Error")
        panic_window.geometry("300x150")
        panic_window.resizable(False, False)

        Label(
            panic_window,
            text=message,
            font=("Helvetica", 12),
            fg="red",
            wraplength=280,
            justify="center",
        ).pack(expand=True, fill="both", padx=10, pady=10)

        Button(
            panic_window,
            text="Close",
            command=panic_window.destroy,
        ).pack(pady=(0, 10))


def init():
    root = Tk()
    app = SatTrackUI(root)
    root.mainloop()


if __name__ == "__main__":
    init()
