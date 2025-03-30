import ctypes
from ctypes import wintypes
import tkinter as tk
from tkinter import ttk

class Display:
    def __init__(self):
        self._gammas = [1.0, 1.0, 1.0]
        self._brightness = 100
        self._initialized = False
        self._hdc = None
        self._gdi32 = ctypes.windll.gdi32

    def _initialize(self):
        if self._initialized:
            return
        
        # Get the device context for the entire screen
        user32 = ctypes.windll.user32
        self._hdc = user32.GetDC(None)
        self._initialized = True

    def set_gamma(self, gamma_red, gamma_green, gamma_blue):
        self._gammas = [gamma_red, gamma_green, gamma_blue]
        return self._update_ramps()

    def set_brightness(self, brightness):
        brightness = max(0, min(100, brightness))
        self._brightness = brightness
        return self._update_ramps()

    def _update_ramps(self):
        self._initialize()
        brightness = self._brightness / 100.0

        # Create ramp arrays (256 entries for each RGB channel)
        ramp_array = (ctypes.c_ushort * 768)()

        for channel in range(3):
            for i in range(256):
                # Gamma calculation
                array_val = int((pow(i / 256.0, 1.0 / self._gammas[channel]) * 65535) + 0.5)
                array_val = int(array_val * brightness)

                # Clamp values
                array_val = max(0, min(65535, array_val))
                ramp_array[channel * 256 + i] = array_val

        # Set the gamma ramp
        result = self._gdi32.SetDeviceGammaRamp(self._hdc, ctypes.byref(ramp_array))
        return bool(result)

    def restore(self):
        """Restore default brightness"""
        return self.set_brightness(100)

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

if __name__ == "__main__":
    app = BrightnessControl()
    app.run()