# -*- coding: utf-8 -*-
"""
tkcolorpicker - Alternative to colorchooser for Tkinter.
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

tkcolorpicker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkcolorpicker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

HSV gradient bar
"""

from .functions import tk, round2, rgb_to_hexa, hsv_to_rgb


class GradientBar(tk.Canvas):
    """HSV gradient colorbar with selection cursor."""

    def __init__(self, parent, name, variables, max_val=360, height=11, width=256, **kwargs):
        """
        Create a GradientBar.

        Keyword arguments:
            * parent: parent window
            * hue: initially selected hue value
            * variable: IntVar linked to the alpha value
            * height, width, and any keyword argument accepted by a tkinter Canvas
        """

        tk.Canvas.__init__(self, parent, width=width, height=height, **kwargs)

        self.max_val = max_val
        self.name = name
        self.variables = variables

        main_variable = self.variables[name]

        value = main_variable.get()
        if value > max_val:
            value = max_val
        elif value < 0:
            value = 0
        main_variable.set(value)

        for variable in self.variables.values():
            variable.trace_add('write', self.update_var)

        self.gradient = tk.PhotoImage(master=self, width=width, height=height)

        self.bind('<Configure>', lambda e: self._draw_gradient())
        self.bind('<ButtonPress-1>', self._on_click)
        self.bind('<B1-Motion>', self._on_move)

    def _draw_gradient(self):
        """Draw the gradient and put the cursor on hue."""
        self.delete("gradient")
        self.delete("cursor")
        del self.gradient
        width = self.winfo_width()
        height = self.winfo_height()

        self.gradient = tk.PhotoImage(master=self, width=width, height=height)

        line = []
        color_components = [component.get() for component in self.variables.values()]
        for i in range(width):
            color_components = [
                component if self.name != color_name else (float(i) / width * self.max_val)
                for color_name, component in zip(self.variables.keys(), color_components)
            ]
            line.append(rgb_to_hexa(*hsv_to_rgb(*color_components)))
        line = "{" + " ".join(line) + "}"
        self.gradient.put(" ".join([line for j in range(height)]))
        self.create_image(0, 0, anchor="nw", tags="gradient",
                          image=self.gradient)
        self.lower("gradient")

        x = self.variables[self.name].get() / self.max_val * width
        self.create_line(x, 0, x, height, width=2, tags='cursor')

    def _on_click(self, event):
        """Move selection cursor on click."""
        x = event.x
        self.coords('cursor', x, 0, x, self.winfo_height())
        self.variables[self.name].set(round2((self.max_val * x) / self.winfo_width()))

    def _on_move(self, event):
        """Make selection cursor follow the cursor."""
        w = self.winfo_width()
        x = min(max(event.x, 0), w)
        self.coords('cursor', x, 0, x, self.winfo_height())
        self.variables[self.name].set(round2((self.max_val * x) / w))

    def update_var(self, *args):
        name = args[0]
        var = self.variables[name]
        if name == self.name:
            value = int(var.get())
            if value > self.max_val:
                value = self.max_val
            elif value < 0:
                value = 0
            self.set(value)
            var.set(value)
            return
        self._draw_gradient()

    def get(self):
        """Return hue of color under cursor."""
        coords = self.coords('cursor')
        return round2(self.max_val * coords[0] / self.winfo_width())

    def set(self, value):
        """Set cursor position on the color corresponding to the hue value."""
        x = value / self.max_val * self.winfo_width()
        self.coords('cursor', x, 0, x, self.winfo_height())
        self.event_generate("<<ColorChange>>")
