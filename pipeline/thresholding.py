import numpy as np

import cv2

import libs.tkColorPicker.tkcolorpicker.colorpicker_window as tkcolorpicker
import libs.tkColorPicker.tkcolorpicker.colorchooser as colorchooser
import libs.tkColorPicker.tkcolorpicker.colorsquare as colorsquare
import libs.tkColorPicker.tkcolorpicker.gradientbar as gradientbar

# um die eigene Implementierung zu verwenden, einfach die nächste Zeile aus- und die übernachste Zeile einkommentieren!
# import tasks.farbkonvertierung as farbkonvertierung
import tasks.farbkonvertierung_selbst_implementiert as farbkonvertierung

from pipeline.no_op_pipe import NoOpPipe
from pipeline.pipe import Pipe, PipeType

# monkey patch tcolorpicker lib
from tasks.thresholding import threshold

for function in dir(farbkonvertierung):
    for module in [tkcolorpicker, colorchooser, colorsquare, gradientbar]:
        if hasattr(module, function):
            setattr(module, function, getattr(farbkonvertierung, function))


class ThresholdingPipe(Pipe):
    friendly_name = "OpenCV Threshold"
    can_unify_config = True

    def __init__(self):
        self.base_color = [0, 100, 100]
        self.tolerances = [50, 50, 50]
        self.max_values = [360, 100, 100]
        self.config_window = None

    def scale_color(self, colors):
        hue_scale = [colors[0] / self.max_values[0] * 180]
        colors = [color / max_value * 255 for color, max_value in zip(colors[1:], self.max_values[1:])]
        return hue_scale + colors

    def get_color_range(self):
        min_v_and_s = [
            max(component - max_value * (tolerance / 100), 0) for component, max_value, tolerance in
            zip(self.base_color, self.max_values, self.tolerances)
        ]

        max_v_and_s = [
            min(component + max_value * (tolerance / 100), max_value) for component, max_value, tolerance in
            zip(self.base_color, self.max_values, self.tolerances)
        ]

        min_color = self.scale_color(min_v_and_s)
        max_color = self.scale_color(max_v_and_s)

        return np.array(min_color, dtype=np.int32), np.array(max_color, dtype=np.int32)

    def threshold(self, image, min_color, max_color):
        return cv2.inRange(image, min_color, max_color)

    def flow(self, image):
        color_info = self.config_window.get_config()
        self.base_color = color_info['color']
        self.tolerances = color_info['tolerances']

        image = image.astype(np.uint8)
        hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        min_color, max_color = self.get_color_range()
        return self.threshold(hsv_image, min_color, max_color)

    def show_config(self, frame):
        if self.config_window is not None:
            self.config_window.show()

    def remove_config(self):
        if self.config_window is not None:
            self.config_window.hide()


class NaiveThresholdingPipe(ThresholdingPipe):
    friendly_name = "Eigenes Threshold"

    def threshold(self, image, min_color, max_color):
        return threshold(image, min_color, max_color) * 255


class ThresholdPipeType(PipeType):
    priority = 30
    implementations = [NoOpPipe, ThresholdingPipe, NaiveThresholdingPipe]

    @staticmethod
    def create_config(config_frame, pipe):
        return tkcolorpicker.ColorPicker(config_frame, farbkonvertierung.hsv_to_rgb(*pipe.base_color), pipe.tolerances)


if __name__ == "__main__":
    import argparse
    import tkinter as tk

    from PIL import Image

    parser = argparse.ArgumentParser(description="Test Blur Implementation")
    parser.add_argument("image", help="path to test image")
    args = parser.parse_args()

    image = Image.open(args.image).convert("RGB")
    image.thumbnail((500, 500), Image.LANCZOS)

    thresholding = ThresholdingPipe()
    # thresholding.config(tk.Tk())
    thresholding.base_color = [150, 75, 75]
    thresholding.tolerances = [20, 25, 15]

    naive_thresholding = NaiveThresholdingPipe()
    naive_thresholding.base_color = thresholding.base_color
    naive_thresholding.tolerances = thresholding.tolerances

    image_data = np.array(image).astype(np.float32)
    thresholded_image = thresholding.flow(image_data)

    image = Image.fromarray(thresholded_image.astype(np.uint8))
    image.show()

    thresholded_image = naive_thresholding.flow(image_data)

    image = Image.fromarray(thresholded_image.astype(np.uint8))
    image.show()

    # Speed Check
    # import timeit
    # print(f"cv threshold: {timeit.timeit('thresholding.flow(image_data)', globals=globals(), number=10)}")
    # print(f"naive threshold: {timeit.timeit('naive_thresholding.flow(image_data)', globals=globals(), number=10)}")
