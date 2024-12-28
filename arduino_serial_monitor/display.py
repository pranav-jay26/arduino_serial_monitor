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

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
from typing import Deque, Tuple
import numpy as np


class Display:
    def __init__(self, window_size: int = 100):
        """Initialize the display.

        Args:
            window_size: Number of data points to show in the plot
        """
        self.window_size = window_size
        self.times: Deque[float] = deque(maxlen=window_size)
        self.values: Deque[float] = deque(maxlen=window_size)

        # Setup the plot
        plt.ion()
        self.fig, self.ax = plt.subplots()
        (self.line,) = self.ax.plot([], [])

        # Configure plot appearance
        self.ax.set_title("Arduino Serial Monitor")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Value")
        self.ax.grid(True)

    def update(self, timestamp: float, value: float):
        """Update the plot with new data.

        Args:
            timestamp: Current timestamp
            value: New data value
        """
        self.times.append(timestamp)
        self.values.append(value)

        # Update plot data
        self.line.set_xdata(np.array(self.times) - self.times[0])
        self.line.set_ydata(self.values)

        # Adjust plot limits
        self.ax.relim()
        self.ax.autoscale_view()

        # Redraw the plot
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def close(self):
        """Close the display window."""
        plt.close(self.fig)
