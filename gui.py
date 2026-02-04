from tkinter import *
from tracking import tracker

class SatTrackUI:
    def __init__(self, root):
        self.root = root
        root.columnconfigure(0, weight=0)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=0)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(3, weight=1)
        root.rowconfigure(4, weight=1)
        root.rowconfigure(5, weight=0)

        # title
        self.root.title("SatTrack v1.0")
        self.title_label = Label(root, text="Welcome to SatTrack", font=("Helvetica", 16))
        self.title_label.grid(row=0, column=1)
        # version
        self.version_label = Label(root, text="Version 1.0\n© 2026 OptiByte Systems", font=("Helvetica", 10))
        self.version_label.grid(row=5, column=2)
        # data input
        self.input_label = Label(root, text="Data Input", font=("Helvetica", 12))
        self.input_label.grid(row=1, column=1)

        self.address_input = Text(root, width=30, height=2)
        self.address_input.grid(row=2, column=1)

        # start tracking: read the address from the widget when the button is clicked
        self.start_tracking = Button(
            root,
            text="Start Tracking",
            command=lambda: tracker.init(self.address_input.get("1.0", "end-1c").strip() or None),
        )
        self.start_tracking.grid(row=3, column=1)
        #self.data_label = Label(root, text=f"Azimuth: {tracker.az.degrees:.2f}°  Elevation: {tracker.el.degrees:.2f}°", font=("Helvetica", 12))
        #self.data_label.grid(row=2, column=1)

        self.root.geometry("900x500")

def init():
    root = Tk()
    app = SatTrackUI(root)
    root.mainloop()

if __name__ == "__main__":
    init()
