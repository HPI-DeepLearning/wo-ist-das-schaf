import argparse
import queue
import tkinter as tk

import numpy as np
from PIL import Image, ImageTk


class MediaDisplay(tk.Frame):
    def __init__(self, queue, master=None, width=1000, height=500):
        super().__init__(master=master, relief=tk.RIDGE, borderwidth=3)

        self.image_display = tk.Canvas(self, width=width, height=height)
        self.image_display.pack(fill=tk.BOTH, expand=tk.YES)

        self.current_image = None

        self._img = None
        self._tk_img = None

        self.queue = queue

        if master is None:
            self.pack(fill=tk.BOTH)
            self.master.title("Anzeige")

    def resize_image(self, image, max_width, max_height, resample):
        aspect_ratio = image.height / image.width
        new_width = max_width
        new_height = max_width * aspect_ratio
        if max_width * aspect_ratio > max_height:
            new_height = max_height
            new_width = max_height * (1 / aspect_ratio)
        return image.resize((int(new_width), int(new_height)), resample)

    def show_image(self, image):
        self._img = Image.fromarray(image.copy())
        self._img = self.resize_image(self._img, self.winfo_width(), self.winfo_height(), Image.LANCZOS)
        self._tk_img = ImageTk.PhotoImage(self._img)

        if self.current_image is not None:
            self.image_display.delete(self.current_image)
            self.current_image = None
        self.current_image = self.image_display.create_image(
            self.winfo_width() // 2 - self._img.width // 2,
            self.winfo_height() // 2 - self._img.height // 2,
            image=self._tk_img,
            anchor=tk.NW
        )

    def maybe_change_image(self):
        while self.queue.qsize():
            try:
                new_image = self.queue.get(0)
                self.show_image(new_image)
            except queue.Empty:
                pass


def main(args):
    viewer = MediaDisplay()
    i = Image.open("testbild.png")
    viewer.show_image(np.array(i))
    viewer.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zeige ein Bild/Video/Stream an.")
    main(parser.parse_args())
