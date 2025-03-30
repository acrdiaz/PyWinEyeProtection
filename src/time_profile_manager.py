from datetime import datetime, time as datetime_time
from typing import Dict, Tuple
from .display_controller import DisplayController

class TimeProfileManager:
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
    def set_time_profile(cls, period: str, start: datetime_time, end: datetime_time, 
                        gamma: Tuple[float, float, float], brightness: int):
        if period in cls._time_settings:
            cls._time_settings[period].update({
                'start': start,
                'end': end,
                'gamma': gamma,
                'brightness': brightness
            })
    
    @classmethod
    def _is_current_time_in_period(cls, current_time: datetime_time, 
                                  start_time: datetime_time, 
                                  end_time: datetime_time) -> bool:
        if end_time < start_time:  # Handle overnight periods
            return current_time >= start_time or current_time <= end_time
        return start_time <= current_time <= end_time

    @classmethod
    def auto_adjust(cls):
        current_time = datetime.now().time()
        
        for period, settings in cls._time_settings.items():
            start = settings['start']
            end = settings['end']
            
            if cls._is_current_time_in_period(current_time, start, end):
                DisplayController.set_gamma(*settings['gamma'])
                DisplayController.set_brightness(settings['brightness'])
                DisplayController.apply_changes()
                break