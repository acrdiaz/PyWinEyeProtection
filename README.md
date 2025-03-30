# PyWinEyeProtection

A Python application for protecting your eyes while working on Windows computers. It automatically adjusts screen brightness and color temperature based on time of day, and reminds you to take regular breaks.

## Features

- **Automatic Time-based Adjustments**
  - Daytime (6:00 AM - 5:00 PM): Normal colors, bright display
  - Evening (5:00 PM - 8:00 PM): Reduced blue light, medium brightness
  - Night (8:00 PM - 6:00 AM): Minimum blue light, low brightness

- **20-20-20 Rule Reminder**
  - Every 20 minutes
  - Look at something 20 feet away
  - For 20 seconds

- **Smart Features**
  - Ambient light detection (if supported by hardware)
  - Smooth transitions between time periods
  - Graceful shutdown with automatic reset

## Project Structure

```
.
├── main.py              # Application entry point
└── src/                 # Source code directory
    ├── __init__.py
    ├── brightness_control.py  # Brightness control UI
    └── display.py            # Display management functions
```

## Requirements

- Python 3.6 or higher
- Windows 10/11
- Required Python packages:
  ```bash
  pip install win10toast wmi
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PyWinEyeProtection.git
   cd PyWinEyeProtection
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Use the slider to adjust screen brightness manually
3. The application will automatically adjust brightness and color temperature based on time of day
4. Regular break reminders will appear according to the 20-20-20 rule

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.