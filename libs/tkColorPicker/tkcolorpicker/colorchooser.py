# -*- coding: utf-8 -*-
"""
Based on tkcolorpicker - Alternative to colorchooser for Tkinter.
See: https://github.com/j4321/tkColorPicker
"""

from locale import getdefaultlocale

from .functions import tk, ttk, hsv_to_rgb, rgb_to_hexa, rgb_to_hsv
from .gradientbar import GradientBar
from .limitvar import MaxValueVar
from .spinbox import Spinbox

# --- Translation
EN = {}
DE = {"Red": "Rot", "Green": "Grün", "Blue": "Blau",
      "Hue": "Farbton", "Saturation": "Sättigung", "Value": "Farbwert",
      "Cancel": "Abbrechen", "Color Chooser": "Farbwahl",
      "Alpha": "Alpha"}

try:
    if getdefaultlocale()[0][:2] == 'de':
        TR = DE
    else:
        TR = EN
except ValueError:
    TR = EN


def _(text):
    """Translate text."""
    return TR.get(text, text)


class ColorChooser(tk.Frame):
    """Color picker dialog."""

    def __init__(self, parent, color_components, **kwargs):
        """
        Create a ColorPicker dialog.

        Arguments:
            * parent: parent window
            * color: initially selected color in rgb or hexa format
            * alpha: alpha channel support (boolean)
            * title: dialog title
        """
        super().__init__(parent, **kwargs)

        # self.rowconfigure(1, weight=1)

        style = ttk.Style(self)
        style.map("palette.TFrame", relief=[('focus', 'sunken')],
                  bordercolor=[('focus', "#4D4D4D")])
        self.configure(background=style.lookup("TFrame", "background"))

        self.init_color(color_components)
        self._old_color = hsv_to_rgb(*self.get_current_color())

        col_frame = ttk.Frame(self)
        col_frame.grid(row=0, rowspan=3, column=1, padx=(4, 10), pady=(10, 4))

        self.create_hsv_chooser(col_frame)
        self.create_rgb_chooser(col_frame)

        self.create_gradient_views()

    def create_rgb_chooser(self, col_frame):
        rgb_frame = ttk.Frame(col_frame, relief="ridge", borderwidth=2)
        rgb_frame.pack(pady=4, fill="x")
        rgb_frame.columnconfigure(0, weight=1)
        s_red = Spinbox(rgb_frame, from_=0, to=255, width=4, name='spinbox',
                        textvariable=self.red, command=self._update_color_rgb)
        s_green = Spinbox(rgb_frame, from_=0, to=255, width=4, name='spinbox',
                          textvariable=self.green, command=self._update_color_rgb)
        s_blue = Spinbox(rgb_frame, from_=0, to=255, width=4, name='spinbox',
                         textvariable=self.blue, command=self._update_color_rgb)
        s_red.delete(0, 'end')
        s_red.insert(0, self._old_color[0])
        s_green.delete(0, 'end')
        s_green.insert(0, self._old_color[1])
        s_blue.delete(0, 'end')
        s_blue.insert(0, self._old_color[2])
        s_red.grid(row=0, column=1, sticky='e', padx=4, pady=4)
        s_green.grid(row=1, column=1, sticky='e', padx=4, pady=4)
        s_blue.grid(row=2, column=1, sticky='e', padx=4, pady=4)
        ttk.Label(rgb_frame, text=_('Red')).grid(row=0, column=0, sticky='e',
                                                 padx=4, pady=4)
        ttk.Label(rgb_frame, text=_('Green')).grid(row=1, column=0, sticky='e',
                                                   padx=4, pady=4)
        ttk.Label(rgb_frame, text=_('Blue')).grid(row=2, column=0, sticky='e',
                                                  padx=4, pady=4)
        s_red.bind('<FocusOut>', self._update_color_rgb)
        s_green.bind('<FocusOut>', self._update_color_rgb)
        s_blue.bind('<FocusOut>', self._update_color_rgb)
        s_red.bind('<Return>', self._update_color_rgb)
        s_green.bind('<Return>', self._update_color_rgb)
        s_blue.bind('<Return>', self._update_color_rgb)

    def create_hsv_chooser(self, col_frame):
        # --- hsv
        hsv_frame = ttk.Frame(col_frame, relief="ridge", borderwidth=2)
        hsv_frame.pack(pady=(0, 4), fill="x")
        hsv_frame.columnconfigure(0, weight=1)
        s_h = Spinbox(hsv_frame, from_=0, to=360, width=4, name='spinbox',
                      textvariable=self.hue, command=self._update_color_hsv)
        s_s = Spinbox(hsv_frame, from_=0, to=100, width=4,
                      textvariable=self.saturation, name='spinbox',
                      command=self._update_color_hsv)
        s_v = Spinbox(hsv_frame, from_=0, to=100, width=4, name='spinbox',
                      textvariable=self.value, command=self._update_color_hsv)
        h, s, v = rgb_to_hsv(*self._old_color)
        s_h.delete(0, 'end')
        s_h.insert(0, h)
        s_s.delete(0, 'end')
        s_s.insert(0, s)
        s_v.delete(0, 'end')
        s_v.insert(0, v)
        s_h.grid(row=0, column=1, sticky='w', padx=4, pady=4)
        s_s.grid(row=1, column=1, sticky='w', padx=4, pady=4)
        s_v.grid(row=2, column=1, sticky='w', padx=4, pady=4)
        ttk.Label(hsv_frame, text=_('Hue')).grid(row=0, column=0, sticky='e',
                                                 padx=4, pady=4)
        ttk.Label(hsv_frame, text=_('Saturation')).grid(row=1, column=0, sticky='e',
                                                        padx=4, pady=4)
        ttk.Label(hsv_frame, text=_('Value')).grid(row=2, column=0, sticky='e',
                                                   padx=4, pady=4)

        s_h.bind('<FocusOut>', self._update_color_hsv)
        s_s.bind('<FocusOut>', self._update_color_hsv)
        s_v.bind('<FocusOut>', self._update_color_hsv)
        s_h.bind('<Return>', self._update_color_hsv)
        s_s.bind('<Return>', self._update_color_hsv)
        s_v.bind('<Return>', self._update_color_hsv)

    def create_gradient_views(self):
        colors = ttk.Frame(self, borderwidth=0, relief='groove')
        colors.grid(row=0, column=0, rowspan=4, padx=10, pady=(10, 4), sticky='n')
        for i, key in enumerate(self.color_components.keys()):
            # --- GradientBar
            gradient_bar = GradientBar(colors, key, self.color_components, max_val=self.color_components[key].max_value,
                                       width=200, height=40, highlightthickness=0)
            gradient_bar.grid(row=i, column=0, pady=(0, 10), sticky='n')
            gradient_bar.bind("<B1-Motion>", self._change_color, True)
            gradient_bar.bind("<ButtonRelease-1>", self._change_color, True)
            gradient_bar.bind("<ButtonRelease-1>", lambda e: self.event_generate("<<Redraw>>"), True)

        preview_frame = ttk.Frame(colors, relief="groove", borderwidth=0, width=200, height=40)
        preview_frame.grid(row=len(self.color_components), column=0, pady=(0, 10), sticky='n')
        old_color_prev = tk.Label(preview_frame, background=rgb_to_hexa(*hsv_to_rgb(*self.get_current_color())),
                                  width=12, highlightthickness=0, height=2,
                                  padx=0, pady=0)
        old_color_prev.pack(expand=True, side=tk.LEFT)

        self.color_preview = tk.Label(preview_frame, width=12, height=2,
                                      pady=0, background=rgb_to_hexa(*hsv_to_rgb(*self.get_current_color())),
                                      padx=0, highlightthickness=0)
        old_color_prev.bind("<ButtonPress-1>", lambda x: self.set_color(*self._old_color), True)
        old_color_prev.bind("<ButtonRelease-1>", lambda e: self.event_generate("<<Redraw>>"), True)
        self.color_preview.pack(expand=True, side=tk.RIGHT)

    def init_color(self, color_components):
        self.color_components = color_components

        for name, component in color_components.items():
            setattr(self, name, component)

        r, g, b = hsv_to_rgb(*self.get_current_color())

        self.red = MaxValueVar(self, r, max_value=255, name="red")
        self.green = MaxValueVar(self, g, max_value=255, name="green")
        self.blue = MaxValueVar(self, b, max_value=255, name="blue")

    def get_current_color(self):
        return [color_component.get() for color_component in self.color_components.values()]

    def set_color(self, r, g, b):
        h, s, v = rgb_to_hsv(r, g, b)
        self.hue.set(h)
        self.saturation.set(s)
        self.value.set(v)
        self._change_color(None)

    def _update_preview(self, r, g, b):
        """Update color preview."""
        color = rgb_to_hexa(r, g, b)
        self.color_preview.configure(background=color)

    def _change_color(self, event):
        """Respond to motion of the hsv cursor."""
        h, s, v = self.get_current_color()
        r, g, b = hsv_to_rgb(h, s, v)
        self.red.set(r)
        self.green.set(g)
        self.blue.set(b)
        self.hue.set(h)
        self.saturation.set(s)
        self.value.set(v)
        self._update_preview(r, g, b)

    def _update_color_hsv(self, event=None):
        """Update display after a change in the HSV spinboxes."""
        if event is None or event.widget.old_value != event.widget.get():
            h = self.hue.get()
            s = self.saturation.get()
            v = self.value.get()
            r, g, b = hsv_to_rgb(h, s, v)
            self.red.set(r)
            self.green.set(g)
            self.blue.set(b)

            for color, component in zip([h, s, v], self.color_components.values()):
                component.set(color)

            self.event_generate("<<Redraw>>")
            self._update_preview(r, g, b)

    def _update_color_rgb(self, event=None):
        """Update display after a change in the RGB spinboxes."""
        if event is None or event.widget.old_value != event.widget.get():
            r = self.red.get()
            g = self.green.get()
            b = self.blue.get()
            h, s, v = rgb_to_hsv(r, g, b)
            self.hue.set(h)
            self.saturation.set(s)
            self.value.set(v)

            for color, component in zip([h, s, v], self.color_components.values()):
                component.set(color)

            self.event_generate("<<Redraw>>")
            self._update_preview(r, g, b)

    def ok(self):
        rgb, hsv, hexa = self.square.get()
        if self.alpha_channel:
            hexa = self.hexa.get()
            rgb += (self.alpha.get(),)
        self.color = rgb, hsv, hexa
        self.destroy()
