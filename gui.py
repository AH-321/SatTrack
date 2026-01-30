from tkinter import *
from tkinter import ttk

class SatTrackUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SatTrack v1.0")
        self.label = Label(root, text="Welcome to SatTrack v1.0", font=("Helvetica", 16))
        self.label.pack(pady=20)


if __name__ == "__main__":
    root = Tk()
    app = SatTrackUI(root)
    root.mainloop()

