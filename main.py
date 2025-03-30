from datetime import time
import time as time_module
from src import DisplayController, TimeProfileManager, BreakTimer

def main():
    # Initialize display controller
    display = DisplayController()
    
    # Customize time profiles
    TimeProfileManager.set_time_profile(
        'daytime',
        time(6, 0),      # Start at 6:00 AM
        time(17, 0),     # End at 5:00 PM
        (1.0, 1.0, 1.0), # Normal colors
        70                # Bright for daytime
    )

    TimeProfileManager.set_time_profile(
        'evening',
        time(17, 0),     # Start at 5:00 PM
        time(20, 0),     # End at 8:00 PM
        (0.9, 0.9, 1.2), # Balanced warm effect
        50                # Medium brightness
    )

    TimeProfileManager.set_time_profile(
        'night',
        time(20, 0),     # Start at 8:00 PM
        time(6, 0),      # End at 6:00 AM
        (0.8, 0.8, 1.4), # Warmer, more blue reduction
        30                # Dimmer for night
    )
    
    # Start break timer
    BreakTimer.start()
    
    # Initial adjustments
    TimeProfileManager.auto_adjust()
    DisplayController.adjust_to_ambient_light()
    
    try:
        print("Eye protection running. Press Ctrl+C to exit...")
        while True:
            time_module.sleep(60)  # Check every minute
            TimeProfileManager.auto_adjust()
            DisplayController.adjust_to_ambient_light()
    except KeyboardInterrupt:
        print("\nShutting down eye protection...")
        BreakTimer.stop()
        # Reset display to default settings
        DisplayController.set_gamma(1.0, 1.0, 1.0)
        DisplayController.set_brightness(100)
        DisplayController.apply_changes()

if __name__ == "__main__":
    main()