import tkinter as tk
import argparse

from pipeline.pipe import PipeType
# noinspection PyUnresolvedReferences
from pipeline import *


def get_pipe_types(return_sorted=True):
    pipe_types = PipeType.__subclasses__()
    if not return_sorted:
        return pipe_types
    return sorted(pipe_types, key=lambda x: x.priority)


class PipeTypeFrame(tk.Frame):
    def __init__(self, master, config_frame, pipe_type):
        super().__init__(master=master, relief=tk.RIDGE, borderwidth=3)
        self.config_frame = config_frame

        self.pipes = [x() for x in pipe_type.implementations]
        pipe_type.create_and_unify_configs(self.pipes, self.config_frame)

        self.selected_pipe = tk.IntVar()
        self.selected_pipe.set(0)

        button_args = {"variable": self.selected_pipe}

        self.choices = []
        self.config_buttons = []
        for i, pipe in enumerate(self.pipes):
            implementation_button = tk.Radiobutton(master=self, text=pipe.friendly_name, value=i, **button_args)
            implementation_button.grid(row=i, column=0)
            self.choices.append(implementation_button)

            config_button = tk.Button(master=self, text="Konfiguriere", command=self.get_command(pipe))
            config_button.grid(row=i, column=1)
            self.config_buttons.append(config_button)

    def get_command(self, pipe):
        return lambda: self.config_frame.set(pipe)

    def get_selected(self):
        return self.pipes[self.selected_pipe.get()]

    def get_all(self):
        return self.pipes


class PipeViewer(tk.Frame):
    def __init__(self, master=None, config_frame=None):
        super().__init__(master=master, relief=tk.RIDGE, borderwidth=3)
        self.config_frame = config_frame
        if self.config_frame is None:
            self.config_frame = tk.Toplevel(self)

        self.pipe_viewers = []

        pipe_types = get_pipe_types()
        self.pipe_viewers = [PipeTypeFrame(self, self.config_frame, pt) for pt in pipe_types]
        self.stage_buttons = []
        self.config_buttons = []

        self.show_stage = tk.IntVar()

        stage_button_args = {"master": self, "indicatoron": 0, "var": self.show_stage, "text": "Anzeige"}
        button_grid_args = {"sticky": tk.W+tk.E+tk.N+tk.S, "padx": 2, "pady": 2}

        for i, pipe_viewer in enumerate(self.pipe_viewers):
            pipe_viewer.grid(row=0, column=i, padx=2, pady=2)
            stage_button = tk.Radiobutton(value=i, **stage_button_args)
            stage_button.grid(row=1, column=i, **button_grid_args)
            self.stage_buttons.append(stage_button)

        self.show_stage.set(len(self.pipe_viewers) - 1)

        if master is None:
            self.pack()
            self.master.title("Verarbeitung")

    def get_active_pipes(self):
        return [pipe_viewer.get_selected() for pipe_viewer in self.pipe_viewers]


def main(args):
    viewer = PipeViewer()
    viewer.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zeige die Schritte zur Verarbeitung an.")
    main(parser.parse_args())
