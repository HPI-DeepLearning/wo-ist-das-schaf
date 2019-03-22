import tkinter as tk


class ToleranceChooser(tk.Frame):

    def __init__(self, parent, tolerance_components, **kwargs):
        super().__init__(parent, **kwargs)

        self.color_components = tolerance_components

        for name, component in tolerance_components.items():
            setattr(self, name, component)
            scale_component = tk.Scale(master=self, length=300, tickinterval=10, variable=component, orient=tk.HORIZONTAL)
            scale_component.pack()
            scale_component.bind('<ButtonRelease-1>', lambda e: self.event_generate("<<Redraw>>"))
            setattr(self, f'{name}_scale', scale_component)
