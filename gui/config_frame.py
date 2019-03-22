import abc
import tkinter as tk


class ConfigFrame(tk.Frame):

    @abc.abstractmethod
    def get_config(self):
        raise NotImplementedError
