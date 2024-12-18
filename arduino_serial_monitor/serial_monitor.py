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

import serial
import serial.tools.list_ports
from typing import Optional, Tuple, List
import time
import re

class SerialMonitor:
    def __init__(self, port: Optional[str] = None, baud_rate: int = 9600):
        """Initialize the serial monitor.
        
        Args:
            port: Serial port name (e.g., 'COM3' or '/dev/ttyUSB0'). 
                 If None, will auto-detect
            baud_rate: Baud rate for serial communication
        """
        self.port = port
        self.baud_rate = baud_rate
        self.serial: Optional[serial.Serial] = None
        self.connected = False

    @staticmethod
    def find_arduino_ports() -> List[str]:
        """Find all potential Arduino ports.
        
        Returns:
            List of port names that might be Arduino devices
        """
        arduino_ports = []
        
        # Common Arduino USB-Serial identifiers
        arduino_identifiers = [
            'Arduino',
            'CH340',        # Common Arduino clone chip
            'USB Serial',
            'ttyACM',       # Arduino Uno and Mega on Linux
            'ttyUSB',       # Other Arduino boards on Linux
            'usbmodem'      # Arduino on macOS
        ]
        
        for port in serial.tools.list_ports.comports():
            # Check if any identifier matches the port description
            if any(id in port.description for id in arduino_identifiers):
                arduino_ports.append(port.device)
            # Also check manufacturer
            elif hasattr(port, 'manufacturer') and port.manufacturer and 'Arduino' in port.manufacturer:
                arduino_ports.append(port.device)
                
        return arduino_ports

    @staticmethod
    def find_bluetooth_ports() -> List[str]:
        """Find all potential Bluetooth serial ports."""
        bluetooth_ports = []
        bluetooth_identifiers = [
            'Bluetooth',
            'BT',
            'RFCOMM'
        ]
        
        for port in serial.tools.list_ports.comports():
            if any(id in port.description for id in bluetooth_identifiers):
                bluetooth_ports.append(port.device)
                
        return bluetooth_ports

    def auto_detect_port(self) -> Optional[str]:
        """Automatically detect the appropriate port.
        
        First tries USB Arduino ports, then falls back to Bluetooth.
        """
        # Try Arduino USB ports first
        arduino_ports = self.find_arduino_ports()
        if arduino_ports:
            return arduino_ports[0]
            
        # Fall back to Bluetooth
        bluetooth_ports = self.find_bluetooth_ports()
        if bluetooth_ports:
            return bluetooth_ports[0]
            
        return None

    def connect(self) -> bool:
        """Establish serial connection."""
        # Auto-detect port if none specified
        if self.port is None:
            self.port = self.auto_detect_port()
            if self.port is None:
                print("No Arduino or Bluetooth devices found")
                return False
            print(f"Auto-detected port: {self.port}")

        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                timeout=1
            )
            self.connected = True
            return True
        except serial.SerialException as e:
            print(f"Error connecting to {self.port}: {e}")
            self.connected = False
            return False

    def read_data(self) -> Tuple[float, float]:
        """Read data from serial port.
        
        Returns:
            Tuple of (timestamp, value)
        """
        if not self.connected or not self.serial:
            raise ConnectionError("Serial port not connected")

        try:
            if self.serial.in_waiting:
                line = self.serial.readline().decode('utf-8').strip()
                return time.time(), float(line)
            return time.time(), 0.0
        except serial.SerialException as e:
            self.connected = False
            raise ConnectionError(f"Lost connection to {self.port}: {e}")
        except ValueError as e:
            print(f"Invalid data received: {e}")
            return time.time(), 0.0

    def close(self):
        """Close the serial connection."""
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.connected = False 