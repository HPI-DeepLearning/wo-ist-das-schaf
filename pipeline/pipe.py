import abc
from abc import ABC


class Pipe(ABC):
    can_unify_config = False

    @property
    @abc.abstractmethod
    def friendly_name(self):
        raise NotImplementedError

    @abc.abstractmethod
    def show_config(self, frame):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_config(self):
        raise NotImplementedError

    @abc.abstractmethod
    def flow(self, image):
        raise NotImplementedError

    def render_additional_info(self, image, info):
        pass


class PipeType:
    priority = -1
    implementations = []

    @staticmethod
    def get_implementations_by_super_class(super_class, recursive=True):
        return super_class.__subclasses__()

    @staticmethod
    @abc.abstractmethod
    def create_config(config_frame, pipe):
        raise NotImplementedError

    @classmethod
    def create_and_unify_configs(cls, pipes, config_frame):
        unifiable_pipes = [pipe for pipe in pipes if pipe.can_unify_config]
        if len(unifiable_pipes) > 0:
            config = cls.create_config(config_frame, unifiable_pipes[0])
            for pipe in unifiable_pipes:
                pipe.config_window = config
