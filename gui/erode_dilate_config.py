import numpy as np
import tkinter as tk

from gui.config_frame import ConfigFrame
from gui.conv_kernel_config import ConvolutionKernelConfig
from utils.gui_utils import DebouncedEntry


class ErodeDilateConfig(ConfigFrame):

    def __init__(self, master, kernel_width, kernel_height):
        super().__init__(master=master)

        self.default_kernel_width = kernel_width
        self.default_kernel_height = kernel_height

        self.kernel_width = tk.StringVar()
        self.kernel_width.set(kernel_width)
        self.kernel_height = tk.StringVar()
        self.kernel_height.set(kernel_height)

        width_frame = tk.Frame(master=self)
        tk.Label(master=width_frame, text="Fensterbreite:").pack(side=tk.LEFT)
        DebouncedEntry(master=width_frame, textvariable=self.kernel_width, width=3, min_val=0).pack(side=tk.RIGHT)
        width_frame.pack(fill=tk.X)

        height_frame = tk.Frame(master=self)
        tk.Label(master=height_frame, text="Fensterhöhe:").pack(side=tk.LEFT)
        DebouncedEntry(master=height_frame, textvariable=self.kernel_height, width=3, min_val=0).pack(side=tk.RIGHT)
        height_frame.pack(fill=tk.X)

        if master is None:
            self.pack()
            self.master.title("Konfiguration")

    def get_config(self):
        config_values = []
        for member in ['width', 'height']:
            member = 'kernel_' + member
            try:
                member = int(getattr(self, member).get())
            except ValueError:
                member = getattr(self, 'default_' + member)
            config_values.append(member)

        return config_values


if __name__ == "__main__":
    viewer = ErodeDilateConfig(None, 5, 5)
    viewer.wait_window(viewer)
    kernel = viewer.get_config()
    print(kernel)
