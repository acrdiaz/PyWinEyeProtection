import threading
import time
from ctypes import windll
from win10toast import ToastNotifier

class BreakTimer:
    _running = True
    _thread = None
    _toaster = ToastNotifier()

    @classmethod
    def start(cls):
        def timer_thread():
            while cls._running:
                time.sleep(1200)  # 20 minutes
                if cls._running:
                    cls._toaster.show_toast(
                        "Eye Break!", 
                        "Look at something 20 feet away for 20 seconds",
                        duration=20,
                        icon_path=None,
                        threaded=True
                    )
                    # Optional: Play a gentle sound
                    windll.kernel32.Beep(750, 800)  # Frequency: 750Hz, Duration: 800ms
        
        cls._thread = threading.Thread(target=timer_thread, daemon=True)
        cls._thread.start()
        return cls._thread

    @classmethod
    def stop(cls):
        cls._running = False