import numpy as np

import cv2

from pipeline.no_op_pipe import NoOpPipe
from pipeline.pipe import Pipe, PipeType
from utils.box_utils import Rect


class FindContoursPipe(Pipe):
    friendly_name = "FindContours"

    def remove_config(self):
        pass

    def show_config(self, frame):
        pass

    def flow(self, image):
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            best_contour = None
            return image, best_contour

        areas = [cv2.contourArea(contour) for contour in contours]
        largest_area_index = np.argmax(areas)
        best_contour = Rect(*cv2.boundingRect(contours[largest_area_index]))
        return image, best_contour

    def render_additional_info(self, image, info):
        if info is not None:
            cv2.rectangle(
                image,
                (info.x, info.y),
                (info.x + info.width, info.y + info.height),
                [0, 255, 0],
                5,
            )
        return image


class FindContoursPipeType(PipeType):

    priority = 60
    implementations = [NoOpPipe, FindContoursPipe]

    @staticmethod
    def create_config(config_frame, pipe):
        return None


if __name__ == "__main__":
    import argparse
    from PIL import Image

    parser = argparse.ArgumentParser(description="Test Blur Implementation")
    parser.add_argument("image", help="path to test image")
    args = parser.parse_args()

    image = Image.open(args.image).convert("RGB")
    image.thumbnail((500, 500), Image.LANCZOS)
    image.show()

    contour_pipe = FindContoursPipe()

    image_data = np.array(image).astype(np.uint8)
    image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2HSV)
    image_data = cv2.inRange(image_data, np.array([80, 50, 50]), np.array([220, 200, 200]))

    contour_image, best_contour = contour_pipe.flow(image_data)

    show_image = Image.fromarray(contour_image.astype(np.uint8))
    show_image.show()

    image_data = np.array(image).astype(np.uint8)
    cv2.rectangle(image_data, (best_contour.x, best_contour.y), (best_contour.x + best_contour.width, best_contour.y + best_contour.height), [0, 255, 0])
    show_image = Image.fromarray(image_data)
    show_image.show()
