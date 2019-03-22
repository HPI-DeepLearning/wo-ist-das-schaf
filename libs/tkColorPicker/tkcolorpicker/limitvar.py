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

Limited StringVar
"""
from .functions import tk


class MaxValueVar(tk.IntVar):

    def __init__(self, *args, **kwargs):
        self.max_value = kwargs.pop('max_value')
        super().__init__(*args, **kwargs)

    def set(self, value):
        value = int(value)
        if value > self.max_value:
            value = self.max_value
        super().set(value)

    def get(self):
        """Return the value of the variable as an integer."""
        value = self._tk.globalgetvar(self._name)
        try:
            return self._tk.getint(value)
        except (TypeError, tk.TclError):
            return 0
