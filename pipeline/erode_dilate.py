from abc import ABC

import cv2
import numpy as np

import tasks.erode_dilate as tasks
from gui.erode_dilate_config import ErodeDilateConfig
from pipeline.no_op_pipe import NoOpPipe
from pipeline.pipe import Pipe, PipeType


class ErodeDilatePipe(Pipe, ABC):
    can_unify_config = True

    def __init__(self):
        super().__init__()
        self.kernel_width = 3
        self.kernel_height = 3
        self.config_window = None

    def show_config(self, frame):
        if self.config_window is None:
            self.config_window = ErodeDilateConfig(frame, self.kernel_width, self.kernel_height)
        self.config_window.pack()

    def remove_config(self):
        if self.config_window is not None:
            self.config_window.pack_forget()

    def build_kernel(self):
        return np.ones((self.kernel_height, self.kernel_width))

    def flow(self, image):
        if self.config_window is not None:
            self.kernel_width, self.kernel_height = self.config_window.get_config()


class CVErodePipe(ErodeDilatePipe):
    friendly_name = "Opencv Erode"

    def flow(self, image):
        super().flow(image)
        return cv2.erode(image, self.build_kernel())


class CVDilatePipe(ErodeDilatePipe):
    friendly_name = "Opencv Dilate"

    def flow(self, image):
        super().flow(image)
        return cv2.dilate(image, self.build_kernel())


class NaiveErodePipe(ErodeDilatePipe):
    friendly_name = "Eigenes Erode"

    def flow(self, image):
        super().flow(image)
        height, width = image.shape

        eroded = np.zeros_like(image)
        kernel = self.build_kernel().shape
        for y in range(height):
            for x in range(width):
                tasks.apply_erode_kernel(image, eroded, x, y, kernel)
        return eroded


class NaiveDilatePipe(ErodeDilatePipe):
    friendly_name = "Eigenes Dilate"

    def flow(self, image):
        super().flow(image)
        height, width = image.shape

        dilated = np.zeros_like(image)
        kernel = self.build_kernel().shape
        for y in range(height):
            for x in range(width):
                tasks.apply_dilate_kernel(image, dilated, x, y, kernel)

        return dilated


class ErodePipeType(PipeType):
    priority = 40
    implementations = [NoOpPipe, CVErodePipe, NaiveErodePipe]

    @staticmethod
    def create_config(config_frame, pipe):
        return ErodeDilateConfig(config_frame, pipe.kernel_width, pipe.kernel_height)


class DilatePipeType(PipeType):
    priority = 50
    implementations = [NoOpPipe, CVDilatePipe, NaiveDilatePipe]

    @staticmethod
    def create_config(config_frame, pipe):
        return ErodeDilateConfig(config_frame, pipe.kernel_width, pipe.kernel_height)


if __name__ == "__main__":
    import argparse
    from PIL import Image

    parser = argparse.ArgumentParser(description="Test Erode Dilate Implementation")
    parser.add_argument("image", help="path to test image")
    args = parser.parse_args()

    image = Image.open(args.image).convert("L")
    image.thumbnail((500, 500), Image.LANCZOS)
    image_data = np.array(image).astype(np.uint8)

    naive_erode_pipe = NaiveErodePipe()
    naive_dilate_pipe = NaiveDilatePipe()
    naive_erode_dilate = lambda image: naive_dilate_pipe.flow(naive_erode_pipe.flow(image))

    cv_erode_pipe = CVErodePipe()
    cv_dilate_pipe = CVDilatePipe()
    cv_erode_dilate = lambda image: cv_dilate_pipe.flow(cv_erode_pipe.flow(image))

    naive_processed_image = naive_erode_dilate(image_data)
    image = Image.fromarray(naive_processed_image)
    image.show()

    cv_processed_image = cv_erode_dilate(image_data)
    image = Image.fromarray(cv_processed_image.astype(np.uint8))
    image.show()

    # Speed Check
    # import statistics
    # import timeit
    # print(f"cv erode-dilate: {statistics.mean(timeit.repeat('cv_erode_dilate(image_data)', globals=globals(), number=2, repeat=5))}")
    # print(f"naive erode-dilate: {statistics.mean(timeit.repeat('naive_erode_dilate(image_data)', globals=globals(), number=2, repeat=5))}")

