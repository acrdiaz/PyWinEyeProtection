# pip install win10toast wmi

import ctypes
import math
from ctypes import windll
from typing import List
from datetime import datetime, time as datetime_time  # Rename time to avoid conflict
import time as time_module  # Rename time module to avoid conflict
import threading
from win10toast import ToastNotifier

class Display:
    _instance = None
    _initialized = False
    _hdc = None
    _gammas = [1.0, 1.0, 1.0]
    _brightness = 100
    _running = True
    
    # Add this time settings dictionary back
    _time_settings = {
        'daytime': {
            'start': datetime_time(6, 0),
            'end': datetime_time(17, 0),
            'gamma': (1.0, 1.0, 1.0),  # Normal during day
            'brightness': 70
        },
        'evening': {
            'start': datetime_time(17, 0),
            'end': datetime_time(20, 0),
            'gamma': (0.9, 0.9, 1.2),  # Slightly warmer, less blue tinting
            'brightness': 50
        },
        'night': {
            'start': datetime_time(20, 0),
            'end': datetime_time(6, 0),
            'gamma': (0.8, 0.8, 1.4),  # Warmer, reduced blue without color artifacts
            'brightness': 30
        }
    }
    
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
    def auto_adjust(cls):
        current_time = datetime.now().time()
        
        for period, settings in cls._time_settings.items():
            start = settings['start']
            end = settings['end']
            
            if end < start:  # Handle overnight periods
                if current_time >= start or current_time <= end:
                    cls.set_gamma(*settings['gamma'])
                    cls.set_brightness(settings['brightness'])
                    cls.apply_changes()  # Apply both gamma and brightness at once
                    break
            else:
                if start <= current_time <= end:
                    cls.set_gamma(*settings['gamma'])
                    cls.set_brightness(settings['brightness'])
                    cls.apply_changes()  # Apply both gamma and brightness at once
                    break

    @classmethod
    def start_break_timer(cls):
        def timer_thread():
            toaster = ToastNotifier()
            while cls._running:
                time_module.sleep(1200)  # 20 minutes
                if cls._running:
                    toaster.show_toast("Eye Break!", 
                                     "Look at something 20 feet away for 20 seconds",
                                     duration=20,
                                     icon_path=None,  # Can add custom icon
                                     threaded=True)   # Non-blocking notification
                    # Optional: Play a gentle sound
                    windll.kernel32.Beep(750, 800)  # Frequency: 750Hz, Duration: 800ms
        
        thread = threading.Thread(target=timer_thread, daemon=True)
        thread.start()
        return thread  # Return thread for management

    @classmethod
    def stop(cls):
        cls._running = False

    @classmethod
    def set_time_profile(cls, period: str, start: datetime_time, end: datetime_time, 
                        gamma: tuple, brightness: int):
        if period in cls._time_settings:
            cls._time_settings[period].update({
                'start': start,
                'end': end,
                'gamma': gamma,
                'brightness': brightness
            })
            
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
                    # If no brightness sensors are available, use time-based defaults
                    current_time = datetime.now().time()
                    # Use existing time settings for brightness
                    for period, settings in cls._time_settings.items():
                        if cls._is_current_time_in_period(current_time, settings['start'], settings['end']):
                            cls.set_brightness(settings['brightness'])
                            cls.apply_changes()
                            return True
                    return False
        except Exception as e:
            print(f"Warning: Could not adjust brightness: {str(e)}")
            return False

    @classmethod
    def _is_current_time_in_period(cls, current_time, start_time, end_time):
        if end_time < start_time:  # Handle overnight periods
            return current_time >= start_time or current_time <= end_time
        return start_time <= current_time <= end_time

# Main execution block
if __name__ == "__main__":
    display = Display()
    
    # Customize all time profiles
    Display.set_time_profile(
        'daytime',
        datetime_time(6, 0),    # Start at 6:00 AM
        datetime_time(17, 0),   # End at 5:00 PM
        (1.0, 1.0, 1.0),       # Normal colors
        70                      # Bright for daytime
    )

    Display.set_time_profile(
        'evening',
        datetime_time(17, 0),   # Start at 5:00 PM
        datetime_time(20, 0),   # End at 8:00 PM
        (0.9, 0.9, 1.2),       # Balanced warm effect
        50                      # Medium brightness
    )

    Display.set_time_profile(
        'night',
        datetime_time(20, 0),   # Start at 8:00 PM
        datetime_time(6, 0),    # End at 6:00 AM
        (0.8, 0.8, 1.4),       # Warmer, more blue reduction
        30                      # Dimmer for night
    )
    
    timer_thread = display.start_break_timer()
    display.auto_adjust()
    display.adjust_to_ambient_light()
    
    try:
        print("Eye protection running. Press Ctrl+C to exit...")
        while True:
            time_module.sleep(60)  # Check every minute instead of every second
            display.auto_adjust()  # Continuously adjust based on time
            display.adjust_to_ambient_light()  # Also check ambient light periodically
    except KeyboardInterrupt:
        print("\nShutting down eye protection...")
        display.stop()
        display.set_gamma(1.0, 1.0, 1.0)
        display.set_brightness(100)
        display.apply_changes()  # Apply final changes