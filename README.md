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

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PyWinEyeProtection.git
cd PyWinEyeProtection
```

## Requirements

```bash
pip install win10toast wmi
```