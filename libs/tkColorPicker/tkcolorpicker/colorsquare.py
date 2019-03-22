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

Color square gradient with selection cross
"""

from .functions import tk, rgb_to_hexa, hsv_to_rgb


class ColorSquare(tk.Canvas):
    """Square color gradient with selection cross."""

    def __init__(self, parent, color_components, tolerance_components, height=256, width=256, include_saturation=None, **kwargs):
        """
        Create a ColorSquare.

        Keyword arguments:
            * parent: parent window
            * hue: color square gradient for given hue (color in top right corner
                   is (hue, 100, 100) in HSV
            * color: initially selected color given in HSV
            * width, height and any keyword option accepted by a tkinter Canvas
        """
        tk.Canvas.__init__(self, parent, height=height, width=width, **kwargs)
        self.bg = tk.PhotoImage(width=width, height=height, master=self)

        self.color_components = color_components
        self.tolerance_components = tolerance_components
        self.include_saturation = include_saturation

        self.bind('<Configure>', lambda e: self.draw())

    def fill_square(self):
        """Create the gradient."""

        def get_min_max_value(v, tolerance):
            max_value = v.max_value
            v = v.get()
            min_value = max(v - max_value * tolerance / 100, 0)
            max_value = min(v + max_value * tolerance / 100, max_value)
            return min_value, max_value

        h, s, v = self.color_components.values()
        h_tolerance, s_tolerance, v_tolerance = self.extract_values(self.tolerance_components)

        h_min, h_max = get_min_max_value(h, h_tolerance)

        variable_min, variable_max = get_min_max_value(s, s_tolerance) if self.include_saturation.get() else get_min_max_value(v, v_tolerance)
        fixed = 100

        width = self.winfo_width()
        height = self.winfo_height()
        height_interpolation = lambda i: (1 - i / height) * max(variable_min, 0) + i / height * min(variable_max, 100)

        if height > 1 and width > 1:
            data = []
            for i in range(height):
                line = []
                for j in range(width):
                    hij = ((1 - j / width) * h_min + j / width * h_max) % h.max_value
                    if self.include_saturation.get():
                        sij = height_interpolation(i)
                        vij = fixed
                    else:
                        sij = fixed
                        vij = height_interpolation(i)
                    color = rgb_to_hexa(*hsv_to_rgb(hij, sij, vij))
                    line.append(color)
                data.append("{" + " ".join(line) + "}")
            self.bg.put(" ".join(data))

    def draw(self, *args):
        """Draw the gradient and the selection cross on the canvas."""
        width = self.winfo_width()
        height = self.winfo_height()
        self.delete("bg")
        self.delete("cross_h")
        self.delete("cross_v")
        del self.bg
        self.bg = tk.PhotoImage(width=width, height=height, master=self)
        self.fill_square()
        self.create_image(0, 0, image=self.bg, anchor="nw", tags="bg")
        self.tag_lower("bg")

    def extract_values(self, components):
        return [component.get() for component in components.values()]
