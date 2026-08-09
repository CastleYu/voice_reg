import logging
import os


# DEBUG 最详细的
# INFO 关键步骤，阶段性输出
# WARNING 可能会导致系统异常或数据超出预期的情况（如大规模删除或其他）
# ERROR 导致了系统异常或数据异常的情况，但是不中断运行
# CRITICAL 导致了系统异常或数据异常，中断了系统运行

class BaseLogs(object):
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)

    def debug(self, msg):
        self.logger.debug(msg)
        return self

    def info(self, msg):
        self.logger.info(msg)
        return self

    def warning(self, msg):
        self.logger.warning(msg)
        return self

    def error(self, msg):
        self.logger.error(msg)
        return self

    def critical(self, msg):
        self.logger.critical(msg)
        return self


class Logs(BaseLogs):
    def __init__(self, name=None):
        self.get_caller()
        if name is None:
            super(Logs, self).__init__(self.caller)
        else:
            super(Logs, self).__init__(name)

    def get_caller(self):
        import inspect
        frame = inspect.stack()[-1]
        module = inspect.getmodule(frame[0])
        self._caller_path = module.__file__
        self.caller = os.path.basename(self._caller_path.split('.')[0])
        return self.caller

    def set_log_file(self, file_name, level=logging.INFO):
        pass

    def enable_console_log(self, enable=True):
        pass
