import ctypes
import math
from ctypes import windll
from datetime import datetime, time as datetime_time

class DisplayController:
    _instance = None
    _initialized = False
    _hdc = None
    _gammas = [1.0, 1.0, 1.0]
    _brightness = 100
    
    @classmethod
    def initialize(cls):
        if cls._initialized:
            return
        
        # Get device context for the entire screen
        cls._hdc = windll.user32.GetDC(0)
        cls._initialized = True

    @classmethod
    def set_gamma(cls, gamma_red: float, gamma_green: float, gamma_blue: float) -> bool:
        cls._gammas[0] = gamma_red
        cls._gammas[1] = gamma_green
        cls._gammas[2] = gamma_blue
        return True

    @classmethod
    def set_brightness(cls, brightness: int) -> bool:
        cls._brightness = max(0, min(100, brightness))
        return True

    @classmethod
    def _update_ramps(cls) -> bool:
        cls.initialize()
        
        brightness = cls._brightness / 100.0
        ramp_array = (ctypes.c_ushort * (3 * 256))()

        for j in range(3):
            for i in range(256):
                array_val = (math.pow(i / 256.0, 1.0 / cls._gammas[j]) * 65535) + 0.5
                array_val *= brightness
                array_val = max(0, min(65535, array_val))
                ramp_array[j * 256 + i] = int(array_val)

        return bool(windll.gdi32.SetDeviceGammaRamp(cls._hdc, ramp_array))

    @classmethod
    def apply_changes(cls) -> bool:
        return cls._update_ramps()

    @classmethod
    def adjust_to_ambient_light(cls):
        try:
            import wmi
            c = wmi.WMI(namespace='root\\WMI')
            # First try to get the ALS information
            try:
                als = c.MSAcpi_ALSensorInformation()[0]
                brightness_level = als.CurrentBrightness
                # Adjust brightness based on ambient light with bounds checking
                adjusted_brightness = min(100, max(0, brightness_level + 20))
                cls.set_brightness(adjusted_brightness)
                cls.apply_changes()
                return True
            except (AttributeError, IndexError):
                # If ALS is not available, try alternative WMI classes for brightness info
                try:
                    monitor = c.WmiMonitorBrightness()[0]
                    current_brightness = monitor.CurrentBrightness
                    cls.set_brightness(current_brightness)
                    cls.apply_changes()
                    return True
                except (AttributeError, IndexError):
                    return False
        except Exception as e:
            print(f"Warning: Could not adjust brightness: {str(e)}")
            return False