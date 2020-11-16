import abc
import math
from abc import ABC

import numpy as np

from PIL import Image, ImageFilter

import tasks.blur as tasks
from gui.conv_kernel_config import ConvolutionKernelConfig
from pipeline.no_op_pipe import NoOpPipe

from pipeline.pipe import Pipe, PipeType
from utils.convolution_utils import build_default_kernel


class ConvolutionPipe(Pipe, ABC):

    config_type = ConvolutionKernelConfig

    def __init__(self, *args, **kwargs):
        self.kernel = build_default_kernel(3, normalize=True)
        super().__init__(*args, **kwargs)
        self.config_window = None

    def show_config(self, frame):
        if self.config_window is None:
            self.config_window = ConvolutionKernelConfig(frame, kernel_size=len(self.kernel))
        self.config_window.pack()

    def remove_config(self):
        if self.config_window is not None:
            self.config_window.pack_forget()

    def update_kernel(self):
        if self.config_window is not None:
            self.kernel = self.config_window.get_config()
            self.kernel = self.kernel.squeeze()

    def normalize_image(self, buffer_image):
        buffer_image /= max(self.kernel.sum(), 1)
        buffer_image = np.clip(buffer_image, 0, 255)
        return buffer_image


class ConvPipe(ConvolutionPipe):
    friendly_name = "Langsame eigene Convolution"
    can_unify_config = True

    def flow(self, image):
        self.update_kernel()
        height, width, num_channels = image.shape

        image = image.astype(np.float32)
        buffer_image = np.zeros_like(image)

        kernel_radius = len(self.kernel) // 2
        image = np.pad(image, [(kernel_radius, kernel_radius), (kernel_radius, kernel_radius), (0, 0)], mode='constant')
        for y in range(height):
            for x in range(width):
                for c in range(num_channels):
                    tasks.apply_convolution_2d_kernel(image, buffer_image, y, x, c, width, height, self.kernel)

        buffer_image = self.normalize_image(buffer_image)
        return buffer_image.astype(np.uint8)


class SeparableConvPipe(ConvolutionPipe):
    friendly_name = "Eigene Convolution"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kernel = build_default_kernel(3, separable=True, normalize=True)

    def show_config(self, frame):
        if self.config_window is None:
            self.config_window = ConvolutionKernelConfig(frame, separable=True)
        self.config_window.pack()

    def flow(self, image):
        self.update_kernel()
        height, width, num_channels = image.shape

        image = image.astype(np.float32)
        buffer_image = np.zeros_like(image)

        kernel_radius = len(self.kernel) // 2
        image = np.pad(image, [(kernel_radius, kernel_radius), (kernel_radius, kernel_radius), (0, 0)], mode='constant')
        tmp_buffer = np.zeros_like(image)

        for y in range(height - 1):
            for x in range(width - 1):
                    tasks.apply_convolution_1d_kernel(image, tmp_buffer, (y + kernel_radius, x + kernel_radius), 0, height, self.kernel)

        for y in range(height - 1):
            for x in range(width - 1):
                    tasks.apply_convolution_1d_kernel(tmp_buffer, buffer_image, (y + kernel_radius, x + kernel_radius), 1, width, self.kernel)

        buffer_image = self.normalize_image(buffer_image)
        return buffer_image.astype(np.uint8)


class FastConvPipe(ConvolutionPipe):
    friendly_name = "Schnelle Convolution"
    can_unify_config = True

    def flow(self, image):
        self.update_kernel()

        in_type = image.dtype
        image = Image.fromarray(image.astype(np.uint8))
        filtered_image = image.filter(
            ImageFilter.Kernel(self.kernel.shape, self.kernel.ravel(), scale=max(self.kernel.sum(), 1))
        )

        return np.array(filtered_image, dtype=in_type)


class BlurPipeType(PipeType):
    priority = 20
    implementations = [NoOpPipe, FastConvPipe, SeparableConvPipe, ConvPipe]
    # implementations = PipeType.get_implementations_by_super_class(ConvolutionPipe)

    @staticmethod
    def create_config(config_frame, pipe):
        return ConvolutionKernelConfig(config_frame, kernel_size=len(pipe.kernel))


if __name__ == "__main__":
    import argparse
    import inspect

    parser = argparse.ArgumentParser(description="Test Blur Implementation")
    parser.add_argument("image", help="path to test image")
    args = parser.parse_args()

    image = Image.open(args.image).convert("RGB")
    image.thumbnail((500, 500), Image.LANCZOS)

    blur = ConvPipe()
    separable_blur = SeparableConvPipe()
    fast_blur = FastConvPipe()

    print(inspect.isabstract(ConvolutionPipe))
    print(inspect.isabstract(ConvPipe))
    print(inspect.isabstract(SeparableConvPipe))
    print(inspect.isabstract(FastConvPipe))

    image_data = np.array(image).astype(np.float32)
    # blur_image_data = blur.flow(image_data)
    # blur2_image_data = separable_blur.flow(image_data)
    # blur3_image_data = fast_blur.flow(image_data)
    # image.show()
    #
    # image = Image.fromarray(blur_image_data.astype(np.uint8))
    # image.show()
    #
    # image = Image.fromarray(blur2_image_data.astype(np.uint8))
    # image.show()
    #
    # image = Image.fromarray(blur3_image_data.astype(np.uint8))
    # image.show()

    # Speed Check
    import timeit
    print(f"naive blur: {timeit.timeit('blur.flow(image_data)', globals=globals(), number=5)}")
    print(f"separable blur: {timeit.timeit('separable_blur.flow(image_data)', globals=globals(), number=5)}")
    print(f"fast blur: {timeit.timeit('fast_blur.flow(image_data)', globals=globals(), number=5)}")
