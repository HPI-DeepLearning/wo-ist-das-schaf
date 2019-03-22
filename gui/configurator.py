import tkinter as tk
import argparse


class ConfiguratorFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, relief=tk.RIDGE, borderwidth=3)

        self.current_pipe = None

        if master is None:
            self.pack()
            self.master.title("Anzeige")

    def set(self, pipe):
        if self.current_pipe is not None:
            self.current_pipe.remove_config()
        pipe.show_config(self)
        self.current_pipe = pipe


def main(args):
    viewer = ConfiguratorFrame()
    viewer.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zeige ein Bild/Video/Stream an.")
    main(parser.parse_args())
