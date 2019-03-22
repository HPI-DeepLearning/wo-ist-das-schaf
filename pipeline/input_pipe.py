import abc
from tkinter.filedialog import askopenfilename

import cv2
import numpy as np
from PIL import Image

from gui.input_file_config import FileConfig, CameraConfig
from pipeline.pipe import Pipe, PipeType


class InputPipe(Pipe):
    _FILE_TYPES = (("all files", "*.*"),)

    def __init__(self, input_trigger=None):
        self.input_trigger = input_trigger
        self.max_side_length = 500
        self.resample_filter = cv2.INTER_AREA
        self.path = ''
        self.config_window = None

    def show_config(self, frame):
        if self.config_window is None:
            self.config_window = FileConfig(
                frame,
                self._FILE_TYPES,
                max_side_length=self.max_side_length,
                resample_filter=self.resample_filter
            )
        self.config_window.pack()

    def remove_config(self):
        if self.config_window is not None:
            self.config_window.pack_forget()

    def resize(self, image):
        if self.max_side_length is None:
            return image

        height, width, _ = image.shape
        aspect_ratio = height / width
        new_width = self.max_side_length if width > height else self.max_side_length * 1 / aspect_ratio
        new_height = self.max_side_length if height > width else self.max_side_length * aspect_ratio
        image = cv2.resize(image, (int(new_width), int(new_height)), interpolation=self.resample_filter)
        return image

    @abc.abstractmethod
    def flow(self, image):
        if self.config_window is not None:
            self.path, self.max_side_length, self.resample_filter = self.config_window.get_config()

    @abc.abstractmethod
    def input_remaining(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_image_data(self):
        raise NotImplementedError


class ImagePipe(InputPipe):
    friendly_name = "Bild"
    _FILE_TYPES = (("Bilder", "*.jpg *.jpeg *.png"), ("all files", "*.*"))

    def __init__(self, path=None):
        super().__init__()
        self._img = None
        self.processed = True

    def flow(self, image):
        super().flow(image)

        if self.path is None or len(self.path) == 0:
            return None

        with Image.open(self.path) as the_image:
            self._img = the_image.convert('RGB')
            self._img = self.resize(np.array(self._img))
        self.processed = True
        return self._img.copy()

    def input_remaining(self):
        return not self.processed

    def get_image_data(self):
        return self._img.copy()


class VideoPipe(InputPipe):
    friendly_name = "Video"
    _FILE_TYPES = (("Videos", "*.mp4 *.mpeg *.avi"), ("all files", "*.*"))

    def __init__(self, path=None):
        super().__init__()
        self.path = path
        self.old_path = self.path
        self.current_frame = None
        self.video = None
        self.frame_counter = 0

    def open_video(self):
        self.video = cv2.VideoCapture(self.path)
        if not self.video.isOpened():
            print("Could not open Video: {}".format(self.path))
            return False
        self.old_path = self.path
        self.frame_counter = 0
        return True

    def flow(self, image):
        super().flow(image)

        if self.path is None or len(self.path) == 0:
            return None

        if self.path != self.old_path:
            if not self.open_video():
                return None

        ret, frame = self.video.read()
        if ret is False or self.frame_counter >= self.video.get(cv2.CAP_PROP_FRAME_COUNT):
            self.video.release()
            self.open_video()
            return None
        else:
            self.frame_counter += 1
        frame = self.resize(frame)

        # convert from BGR to RGB
        frame = frame[:, :, ::-1]

        self.current_frame = frame.copy()
        return frame

    def input_remaining(self):
        return False

    def get_image_data(self):
        return self.current_frame


class CameraPipe(InputPipe):
    friendly_name = "Kamera"

    def __init__(self):
        super().__init__()
        self.camera = None
        self.can_not_open_current_id = False
        self.camera_id = 0
        self.current_frame = None

    def open_camera(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None

        self.camera = cv2.VideoCapture(self.camera_id)
        if not self.camera.isOpened():
            print("Could not open Camera with id {}".format(self.camera_id))
            self.camera = None
            self.can_not_open_current_id = True
            return False
        self.can_not_open_current_id = False
        return True

    def flow(self, image):
        super().flow(image)

        if self.path is None or len(self.path) == 0:
            return None

        try:
            camera_id = int(self.path)
        except ValueError:
            return None

        if (self.camera is None and not self.can_not_open_current_id) or camera_id != self.camera_id:
            self.camera_id = camera_id
            if not self.open_camera():
                return None
        elif self.camera is None and self.can_not_open_current_id:
            return None

        ret, frame = self.camera.read()
        if ret is False:
            print("Could not read from camera")
            return None
        frame = self.resize(frame)

        # convert from BGR to RGB
        frame = frame[:, :, ::-1]

        self.current_frame = frame.copy()
        return frame

    def show_config(self, frame):
        if self.config_window is None:
            self.config_window = CameraConfig(
                frame,
                self._FILE_TYPES,
                max_side_length=self.max_side_length,
                resample_filter=self.resample_filter
            )
        self.config_window.pack()

    def input_remaining(self):
        return False

    def get_image_data(self):
        return self.current_frame


class InputPipeType(PipeType):
    priority = 0
    implementations = PipeType.get_implementations_by_super_class(InputPipe)

    @staticmethod
    def create_config(config_frame, pipe):
        return None
