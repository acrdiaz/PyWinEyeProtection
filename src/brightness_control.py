import tkinter as tk
from tkinter import ttk
from .display import Display

class BrightnessControl:
    def __init__(self):
        self.display = Display()
        self.root = tk.Tk()
        self.root.title("Brightness Control")
        self.root.geometry("300x100")

        # Create and pack widgets
        self.label = ttk.Label(self.root, text="Brightness: 100")
        self.label.pack(pady=10)

        self.slider = ttk.Scale(
            self.root,
            from_=0,
            to=100,
            orient="horizontal",
            command=self.on_slider_change
        )
        self.slider.set(100)
        self.slider.pack(fill="x", padx=20)

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_slider_change(self, value):
        brightness = int(float(value))
        self.label.config(text=f"Brightness: {brightness}")
        self.display.set_brightness(brightness)

    def on_closing(self):
        self.display.restore()
        self.root.destroy()

    def run(self):
        self.root.mainloop()