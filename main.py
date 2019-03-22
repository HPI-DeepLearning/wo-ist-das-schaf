import argparse
import queue
import threading
import tkinter as tk

from gui.configurator import ConfiguratorFrame
from gui.media_display import MediaDisplay
from gui.pipe_viewer import PipeViewer
from pipeline.input_pipe import InputPipe
from pipeline.thresholding import ThresholdingPipe


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)

        grid_options = {
            "padx": 2,
            "pady": 2,
            "sticky": tk.E + tk.W + tk.S + tk.N,
        }

        self.processing_thread = None
        self.stop = threading.Event()
        self.stop_gui_update = threading.Event()

        self.synchronization_queue = queue.Queue()

        self.display = MediaDisplay(self.synchronization_queue, master=self)
        self.display.grid(**grid_options)

        self.config_frame = ConfiguratorFrame(master=self)
        self.config_frame.grid(column=1, row=0)

        self.pipe_viewer = PipeViewer(master=self, config_frame=self.config_frame)
        self.pipe_viewer.grid(column=0, row=1, columnspan=1, **grid_options)

        self.process_button = tk.Button(master=self, text="Starte Pipeline!", command=self.toggle_processing)
        self.process_button.grid(column=1, row=1)

        if master is None:
            self.grid()
            self.master.title("Finde das Schaf")

            self.wait_visibility()
            # bad windows hack
            for pipe_viewer in self.pipe_viewer.pipe_viewers:
                for pipe in pipe_viewer.pipes:
                    if isinstance(pipe, ThresholdingPipe):
                        pipe.remove_config()

    def process(self):
        while True:
            if self.stop.is_set():
                self.stop.clear()
                break
            try:
                self.process_step()
            except Exception as e:
                print(e)
                self.stop.set()
                self.stop_gui_update.set()

    def periodic_image_display_update(self):
        self.display.maybe_change_image()
        if self.stop_gui_update.is_set():
            self.stop_gui_update.clear()
            return
        self.master.after(1000 // 30, self.periodic_image_display_update)

    def process_step(self):
        selected_pipes = self.pipe_viewer.get_active_pipes()
        show_pipe = self.pipe_viewer.show_stage.get()

        image = None
        auxilliary_data = []
        current_input_image = None
        for i, pipe in enumerate(selected_pipes):
            image = pipe.flow(*([image] + auxilliary_data))
            if image is None:
                return

            if isinstance(pipe, InputPipe):
                current_input_image = pipe.get_image_data()

            if isinstance(image, tuple):
                auxilliary_data = image[1:]
                image = image[0]
            else:
                auxilliary_data = []

            if i == show_pipe:
                if len(auxilliary_data) > 0:
                    render_image = pipe.render_additional_info(current_input_image, *auxilliary_data)
                    self.synchronization_queue.put(render_image)
                else:
                    self.synchronization_queue.put(image)

    def toggle_processing(self):
        print("toggle processing")
        if self.processing_thread is None:
            self.processing_thread = threading.Thread(target=self.process, daemon=True)
            self.processing_thread.start()
            self.process_button.configure(text="Stoppe Pipeline!")
            self.periodic_image_display_update()
        else:
            self.stop.set()
            self.stop_gui_update.set()
            self.processing_thread = None
            self.process_button.configure(text="Starte Pipeline!")


def main(args):
    viewer = MainWindow()
    viewer.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Programm zum Finden des HPI-Schafs")
    main(parser.parse_args())
