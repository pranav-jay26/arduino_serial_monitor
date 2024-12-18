# Arduino Serial Monitor - A real-time serial monitor for Arduino
# Copyright (C) 2024 Pranav Jayakumar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import signal
import sys
from .serial_monitor import SerialMonitor
from .display import Display
import time

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Arduino Serial Monitor')
    parser.add_argument('--port', help='Serial port (e.g., COM3 or /dev/ttyUSB0). '
                       'If not specified, will auto-detect Arduino or Bluetooth connection')
    parser.add_argument('--baud', type=int, default=9600,
                       help='Baud rate (default: 9600)')
    parser.add_argument('--window', type=int, default=100,
                       help='Display window size (default: 100)')
    return parser.parse_args()

def main():
    """Main execution function."""
    args = parse_args()
    
    # Initialize components
    monitor = SerialMonitor(args.port, args.baud)
    display = Display(args.window)
    
    # Setup graceful shutdown
    def signal_handler(sig, frame):
        print("\nShutting down...")
        monitor.close()
        display.close()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Main loop
    if args.port:
        print(f"Connecting to specified port {args.port} at {args.baud} baud...")
    else:
        print(f"Searching for Arduino or Bluetooth device at {args.baud} baud...")
    
    if not monitor.connect():
        sys.exit(1)
    
    print("Monitoring serial data. Press Ctrl+C to exit.")
    while True:
        try:
            timestamp, value = monitor.read_data()
            display.update(timestamp, value)
            time.sleep(0.01)  # Small delay to prevent CPU overload
        except ConnectionError as e:
            print(f"Error: {e}")
            break
        except KeyboardInterrupt:
            break
    
    # Cleanup
    monitor.close()
    display.close()

if __name__ == '__main__':
    main() 