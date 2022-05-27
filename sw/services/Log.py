
import logging


class Log:
    __logger = None

    @classmethod
    def _logger(cls):
        if not cls.__logger:
            cls.__logger = logging.getLogger('project')
        return cls.__logger

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        cls._logger().warning(msg, *args, **kwargs)

    @classmethod
    def warn(cls, msg, *args, **kwargs):
        cls._logger().warn(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        cls._logger().error(msg, *args, **kwargs)

    @classmethod
    def critical(cls, msg, *args, **kwargs):
        cls._logger().critical(msg, *args, **kwargs)

    @classmethod
    def info(cls, msg, *args, **kwargs):
        cls._logger().info(msg, *args, **kwargs)
