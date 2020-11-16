import tkinter as tk
import tkinter.ttk as ttk
import libs.tkColorPicker.tkcolorpicker.colorpicker_window as tkcolorpicker
import libs.tkColorPicker.tkcolorpicker.colorchooser as colorchooser
import libs.tkColorPicker.tkcolorpicker.colorsquare as colorsquare
import libs.tkColorPicker.tkcolorpicker.gradientbar as gradientbar
import tasks.farbkonvertierung as farbkonvertierung


# monkey patch tcolorpicker lib
for function in dir(farbkonvertierung):
    for module in [tkcolorpicker, colorchooser, colorsquare, gradientbar]:
        if hasattr(module, function):
            setattr(module, function, getattr(farbkonvertierung, function))


root = tk.Tk()
style = ttk.Style(root)
style.theme_use('clam')

print(tkcolorpicker.askcolor((255, 255, 0), root))
