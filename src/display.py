import ctypes
from ctypes import wintypes

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