import tkinter as tk
import tkinter.font as tk_font
from tkinter.filedialog import askopenfilename

import cv2

from gui.config_frame import ConfigFrame
from utils.gui_utils import DebouncedEntry


class FileConfig(ConfigFrame):

    def __init__(self, parent, file_types, max_side_length=500, resample_filter=cv2.INTER_AREA, default_file_path=''):
        super().__init__(master=parent)
        self.file_types = file_types

        self.default_max_side_length = max_side_length
        self.max_side_length = tk.StringVar(master=self)
        self.max_side_length.set(max_side_length)
        size_frame = self.build_size_entry()

        self.file_path = tk.StringVar(master=self)
        self.file_path.set(default_file_path)
        path_frame = self.build_path_selection()

        self.selected_filter = tk.IntVar(master=self)
        filter_frame = self.build_filter_selection(self.selected_filter)
        self.selected_filter.set(resample_filter)

        size_frame.pack(fill=tk.X)
        path_frame.pack(fill=tk.X, pady=20)
        filter_frame.pack(fill=tk.X)

    def build_size_entry(self):
        frame = tk.LabelFrame(master=self, text="Max. Bildgröße")
        entry = DebouncedEntry(
            master=frame,
            textvariable=self.max_side_length,
            min_val=1,
            conversion_func=int
        )
        entry.pack(side=tk.TOP)
        return frame

    def build_path_selection(self):
        frame = tk.LabelFrame(master=self, text="Dateiauswahl")

        self.file_label = tk.Label(master=frame)
        self.file_label.pack(side=tk.LEFT)

        button = tk.Button(master=frame, text="Datei")
        button['command'] = self.set_path(frame, button)
        button.pack(side=tk.RIGHT)

        return frame

    def fit_text(self, text, max_width):
        label = self.file_label

        font = tk_font.nametofont(label.cget("font"))
        actual_width = font.measure(text)
        if actual_width <= max_width:
            # the original text fits; no need to add ellipsis
            label.configure(text=text)
        else:
            # the original text won't fit. Keep shrinking
            # until it does
            while actual_width > max_width and len(text) > 1:
                text = text[1:]
                actual_width = font.measure("..." + text)
            self.file_label['text'] = "..." + text

    def set_path(self, frame, button):
        def inner():
            file_path = askopenfilename(filetypes=self.file_types)
            self.file_path.set(file_path)
            file_label_width = frame.winfo_width() - button.winfo_width()
            self.fit_text(file_path, file_label_width)
        return inner

    def build_filter_selection(self, var):
        filter_selection_frame = tk.LabelFrame(master=self, text="InterpolationsMethode")
        for flag in ["NEAREST", "LINEAR", "CUBIC", "AREA", "LANCZOS4"]:
            tk.Radiobutton(
                master=filter_selection_frame,
                text=flag,
                variable=var,
                value=getattr(cv2, "INTER_{}".format(flag))
            ).pack(side=tk.BOTTOM)
        return filter_selection_frame

    def get_config(self):
        try:
            max_side_length = int(self.max_side_length.get())
        except ValueError:
            max_side_length = self.default_max_side_length

        return self.file_path.get(), max_side_length, self.selected_filter.get()


class CameraConfig(FileConfig):

    def __init__(self, *args, **kwargs):
        kwargs['default_file_path'] = '0'
        super().__init__(*args, **kwargs)

    def build_path_selection(self):
        frame = tk.LabelFrame(master=self, text="Auswahl der Kamera")

        entry = DebouncedEntry(
            master=frame,
            textvariable=self.file_path,
            min_val=0,
            conversion_func=int
        )
        entry.pack(side=tk.TOP)
        return frame
