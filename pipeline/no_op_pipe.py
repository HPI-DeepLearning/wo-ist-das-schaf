from pipeline.pipe import Pipe


class NoOpPipe(Pipe):
    friendly_name = "keine Operation"

    def show_config(self, frame):
        pass

    def remove_config(self):
        pass

    def flow(self, image):
        return image
