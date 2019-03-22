import tkinter as tk


class DebouncedEntry(tk.Entry):

    def __init__(self, *args, **kwargs):
        self.conversion_func = kwargs.pop('conversion_func', int)
        self.min_value = kwargs.pop('min_val', None)
        self.bound_var = kwargs.pop('textvariable')

        master = kwargs.get('master')
        debounce_func = master.register(self.debounce)
        self.debounce_var = tk.StringVar(master=master)
        self.debounce_var.set(self.bound_var.get())

        kwargs.update({
            "textvariable": self.debounce_var,
            "validate": "focusout",
            "validatecommand": (debounce_func, '%P')
        })

        super().__init__(*args, **kwargs)

    def debounce(self, new_value):
        try:
            val = self.conversion_func(new_value)
        except ValueError:
            return False

        if self.min_value is not None and val < self.min_value:
            return False

        self.bound_var.set(val)
        return True
