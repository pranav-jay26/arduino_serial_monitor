# Arduino Serial Monitor

A Python-based real-time serial monitor for Arduino with automatic port detection and real-time plotting capabilities. This tool automatically detects Arduino devices connected via USB or Bluetooth and displays their serial output in a real-time graph.

## Features

- 📊 Real-time data plotting using matplotlib
- 🔍 Automatic Arduino device detection (USB and Bluetooth)
- 🔌 Support for custom serial ports and baud rates
- 📈 Adjustable display window size
- 🛑 Graceful handling of connection issues
- ⌨️ Simple command-line interface

## Installation Using Nix

This project has been packaged as a Nix flake. Here is how to install and run the serial monitor.

### Basic Usage

To run without installing

```
nix run github:pranav-jay26/arduino_serial_monitor
```

Alternatively

```
nix build github:pranav-jay26/arduino_serial_monitor
./result/bin/serial_monitor
```

## Legacy Installation

If you are not comfortable with the Nix package manager, or would like to use the legacy installation method, follow these steps.

### Quick Install (Linux/MacOS)

1. Clone the repository:

```bash
git clone https://github.com/pranav-jay26/arduino_serial_monitor.git/
cd arduino_serial_monitor
```

2. Build the project:
   You can either install this package with `pip`, or you could use the `install.sh` script. To add it to your `PATH` and run the serial monitor anywhere, use the install script.

With `pip`:

```bash
# Create and source the virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate

# Install dependencies

pip install -e .
```

With the install script (recommended):

```bash
./install.sh
```

## Usage

### Basic Usage

Run with automatic device detection:

```bash
serial_monitor
```

### Command-line Options

- Specify a port:

```bash
serial_monitor --port COM3  # Windows
serial_monitor --port /dev/ttyUSB0  # Linux
```

- Set custom baud rate:

```bash
serial_monitor --baud 115200
```

- Adjust display window size:

```bash
serial_monitor --window 200
```

### Arduino Setup

Your Arduino should send numeric values over serial, one per line. Example Arduino sketch:

```cpp
void setup() {
    Serial.begin(9600);
}

void loop() {
    // Send a sine wave
    float value = sin(millis() / 1000.0) * 100;
    Serial.println(value);
    delay(10);
}
```

## Requirements

- Python 3.7 or higher
- pyserial >= 3.5
- matplotlib >= 3.7.0
- numpy >= 1.24.0

## Troubleshooting

1. **No devices found**:

   - Check if your Arduino is properly connected
   - Verify you have permission to access the serial port
   - Try running with sudo on Linux if needed

2. **Permission denied**:
   On Linux, add your user to the dialout group:

```bash
sudo usermod -a -G dialout $USER
```

Then log out and back in.

3. **Display issues**:
   If the plot window doesn't show up, try:

```bash
export MPLBACKEND=TkAgg
```

4. **Connection errors**:
   - Check if another program is using the serial port
   - Verify the baud rate matches your Arduino sketch
   - Try unplugging and reconnecting the Arduino

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Contact

Pranav Jayakumar - <jayakumar.pranav@gmail.com>

Project Link: [https://github.com/pranav-jay26/arduino_serial_monitor](https://github.com/pranav-jay26/arduino_serial_monitor)

```

```
