#!/usr/bin/env python
"""
================================================
AB Electronics UK ADC Pi 8-Channel ADC GUI demo

https://www.abelectronics.co.uk/p/69/adc-pi

Requires python smbus, tkinter and matplotlib to be installed

Install with: pip install smbus tkinter matplotlib

run with: python3 demo_gui.py
================================================

Create a GUI application to display the voltage from each of the ADC channels

"""

import sys
import collections
import tkinter as tk

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.animation import FuncAnimation
except ImportError:
    raise ImportError("matplotlib is required: pip install matplotlib")

try:
    from ADCPi import ADCPi
except ImportError:
    print("Failed to import ADCPi from python system path")
    print("Importing from parent folder instead")
    try:
        sys.path.append('..')
        from ADCPi import ADCPi
    except ImportError:
        raise ImportError("Failed to import library from parent folder")


HISTORY_LENGTH = 100 # Number of voltage readings to keep in memory and display on screen at once.
UPDATE_INTERVAL_MS = 200 # How often to read the ADC and refresh the chart, in milliseconds.

# One hex colour string per channel.  Hex colours have the form "#RRGGBB"
CHANNEL_COLOURS = [
    "#e6194b",  # Ch 1 – red
    "#3cb44b",  # Ch 2 – green
    "#4363d8",  # Ch 3 – blue
    "#f58231",  # Ch 4 – orange
    "#911eb4",  # Ch 5 – purple
    "#42d4f4",  # Ch 6 – cyan
    "#f032e6",  # Ch 7 – magenta
    "#bfef45",  # Ch 8 – lime
]

class ADCChartApp:
    # Main application class

    def __init__(self, root):
        """
        __init__ is called when you create an instance of the class.
        """

        # Store the tkinter window so other methods can use it.
        self.root = root

        # Set the text shown in the window's title bar.
        self.root.title("ADC Pi - 8 Channel Voltage Monitor")

        # Tell tkinter to call our _on_close method when the user clicks the
        # window's close (X) button, instead of just quitting immediately.
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Create an ADCPi object.  The two hex values are the I2C addresses
        # of the two MCP3424 chips on the board (set by the address jumpers).
        # 12 is the sample resolution in bits (12, 14, 16 or 18).
        self.adc = ADCPi(0x68, 0x69, 12)

        # Create a list of 8 deques, one per channel.
        self.history = [
            collections.deque([0.0] * HISTORY_LENGTH, maxlen=HISTORY_LENGTH)
            for _ in range(8)
        ]

        # Build all the on-screen widgets (chart, labels, etc.).
        self._build_ui()

        # Start the animation loop.
        self.ani = FuncAnimation(
            self.fig,               # the Figure to animate
            self._update,           # the function to call each frame
            interval=UPDATE_INTERVAL_MS,
            blit=False,             # redraw the whole axes each frame
            cache_frame_data=False, # don't store old frames in memory
        )

    def _build_ui(self):
        """
        Creates and arranges all the visual widgets: the matplotlib chart
        embedded in the tkinter window, plus a row of voltage-value labels
        along the bottom.
        """

        # Create the matplotlib Figure and Axes

        # Figure is the overall drawing canvas.
        self.fig = Figure(figsize=(10, 6), dpi=100, facecolor="#1e1e1e")

        # add_subplot(111) means "1 row, 1 column, subplot 1", i.e. a single
        # chart filling the whole figure.  The Axes object (self.ax) is where
        # lines, labels and grids are drawn.
        self.ax = self.fig.add_subplot(111)

        # Style the chart area.
        self.ax.set_facecolor("#2b2b2b")         # dark grey chart background
        self.ax.set_ylim(-0.1, 5.5)              # Y-axis: -0.1 V to 5.5 V
        self.ax.set_xlim(0, HISTORY_LENGTH - 1)  # X-axis: 0 to 99 samples
        self.ax.set_title("ADC Pi Voltage Channels", color="white", fontsize=13)
        self.ax.set_xlabel("Samples", color="white")
        self.ax.set_ylabel("Voltage (V)", color="white")
        self.ax.tick_params(colors="white")  # make axis tick labels white

        # 'spines' are the four border-lines around the chart area.
        for spine in self.ax.spines.values():
            spine.set_edgecolor("#555555")

        # Add a subtle dashed grid to make values easier to read.
        self.ax.grid(color="#444444", linestyle="--", linewidth=0.5)

        # Automatically adjust the padding so labels aren't clipped.
        self.fig.tight_layout(pad=2)

        # --- Draw one line per channel ---

        # x holds the sample index numbers 0, 1, 2, … 99.
        # These never change, only the Y values (voltages) are updated.
        x = list(range(HISTORY_LENGTH))

        # self.lines will hold a reference to each plotted line, so we can
        # update the Y data later without redrawing the whole chart.
        self.lines = []

        for i in range(8):
            # ax.plot() returns a list of Line2D objects; the comma after
            # 'line' unpacks that single-item list directly into a variable.
            (line,) = self.ax.plot(
                x,                        # X data — sample indices
                list(self.history[i]),    # Y data — all zeros at start
                color=CHANNEL_COLOURS[i],
                linewidth=1.5,
                label=f"Ch {i + 1}",     # f-string: inserts i+1 into the text
            )
            self.lines.append(line)

        # Draw the legend that maps line colours to channel names.
        self.ax.legend(
            loc="upper right",
            fontsize=8,
            facecolor="#333333",
            edgecolor="#555555",
            labelcolor="white",
        )

        # Embed the matplotlib figure in the tkinter window

        # FigureCanvasTkAgg wraps the Figure as a tkinter widget.
        canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        canvas.draw()  # render the initial (all-zeros) chart

        # pack() is tkinter's layout manager.  fill=tk.BOTH and expand=True
        # make the chart resize when the window is resized.
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas = canvas

        # Build the live voltage label bar at the bottom

        # A Frame is an invisible container used to group and position widgets.
        label_frame = tk.Frame(self.root, bg="#1e1e1e")
        label_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=4, pady=4)

        # self.value_labels stores a reference to each channel's value label
        # so _update() can change its text every frame.
        self.value_labels = []

        for i in range(8):
            # One small sunken frame per channel acts as a visual card.
            frame = tk.Frame(label_frame, bg="#2b2b2b", bd=1, relief=tk.SUNKEN)
            frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

            # Static channel-name label coloured to match its chart line.
            tk.Label(
                frame,
                text=f"Ch {i + 1}",
                bg="#2b2b2b",
                fg=CHANNEL_COLOURS[i],
                font=("Helvetica", 9, "bold"),
            ).pack()

            # Dynamic voltage label. Its text is updated in _update().
            lbl = tk.Label(
                frame,
                text="0.000 V",
                bg="#2b2b2b",
                fg="white",
                font=("Helvetica", 9),
            )
            lbl.pack()
            self.value_labels.append(lbl)

    def _update(self, _frame):
        """
        Called automatically by FuncAnimation every UPDATE_INTERVAL_MS ms.
        """

        for i in range(8):
            # Read the voltage on channel i+1 (channels are 1-indexed on the
            # ADC Pi, so channel 1 is i=0, channel 8 is i=7).
            voltage = self.adc.read_voltage(i + 1)

            self.history[i].append(voltage) # Add the new reading to the right of the deque.

            self.lines[i].set_ydata(list(self.history[i])) # Update the chart line's Y data with the new history.

            self.value_labels[i].config(text=f"{voltage:.3f} V") # Update the text label.

        return self.lines # Return the list of lines

    def _on_close(self):
        """
        Called when the user clicks the window's close button.
        """
        self.ani.event_source.stop()
        self.root.destroy()


def main():

    # Tk() creates the top-level window.
    root = tk.Tk()

    # Create the application, set up all widgets and start the animation.
    app = ADCChartApp(root)  # noqa: F841

    # Hand control to tkinter.
    root.mainloop()

if __name__ == "__main__":
    main()
