import numpy as np
import tkinter as tk

from gui.config_frame import ConfigFrame
from utils.convolution_utils import build_default_kernel
from utils.gui_utils import DebouncedEntry


class XbyXKernelLayout(tk.Frame):

    def __init__(self, master, kernel_width, separable):
        super().__init__(master=master)

        self.kernel_width = kernel_width
        self.kernel_height = 1 if separable else kernel_width
        self.kernel_values = [tk.StringVar() for _ in range(self.kernel_width * self.kernel_height)]

        kernel = build_default_kernel(kernel_width, separable)
        kernel = kernel.astype('int32')

        for kernel_var, kernel_element in zip(self.kernel_values, kernel.ravel()):
            kernel_var.set(kernel_element)

        for j in range(self.kernel_height):
            for i in range(self.kernel_width):
                entry = DebouncedEntry(
                    master=self,
                    textvariable=self.kernel_values[j * kernel_width + i],
                    width=2,
                    conversion_func=float
                )
                entry.grid(row=j, column=i)

    @property
    def kernel(self):
        kernel = np.array([value.get() for value in self.kernel_values], dtype=np.float32)
        kernel = kernel / max(sum(kernel.ravel()), 1)
        return kernel.reshape((self.kernel_height, self.kernel_width))


class ConvolutionKernelConfig(ConfigFrame):

    def __init__(self, master=None, separable=False, kernel_layout_class=XbyXKernelLayout, kernel_size=3):
        super().__init__(master=master, borderwidth=3)

        self.label = tk.Label(master=self, text="Kernel Konfiguration")
        self.label.pack()

        self.kernel_layout_class = kernel_layout_class

        self.separable = separable

        if master is None:
            self.pack()
            self.master.title("Konfiguration")

        self.kernel_size = tk.IntVar(self, value=3)
        self.kernel_size.trace_add('write', self.build_layout)
        self.build_kernel_size_choice(self.kernel_size)

        self.kernel_layout = None
        self.kernel_size.set(kernel_size)

    def build_kernel_size_choice(self, var):
        kernel_size_frame = tk.Frame(master=self)
        tk.Radiobutton(master=kernel_size_frame, text="3x3", variable=var, value=3).pack(side=tk.LEFT)
        tk.Radiobutton(master=kernel_size_frame, text="5x5", variable=var, value=5).pack(side=tk.RIGHT)
        kernel_size_frame.pack()

    def build_layout(self, varname, elementname, mode):
        if self.kernel_layout is not None:
            self.kernel_layout.pack_forget()

        self.kernel_layout = self.kernel_layout_class(self, self.kernel_size.get(), self.separable)
        self.kernel_layout.pack()

    def get_config(self):
        return self.kernel_layout.kernel


if __name__ == "__main__":
    viewer = ConvolutionKernelConfig(separable=True)
    viewer.wait_window(viewer)
    kernel = viewer.get_kernel()
    print(kernel)
    print(sum(kernel.ravel()))
