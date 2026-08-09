# logs

import logging


# DEBUG 最详细的
# INFO 关键步骤，阶段性输出
# WARNING 可能会导致系统异常或数据超出预期的情况（如大规模删除或其他）
# ERROR 导致了系统异常或数据异常的情况，但是不中断运行
# CRITICAL 导致了系统异常或数据异常，中断了系统运行


class ConsoleLog:
    def __init__(self, *args, **kwargs):
        self.debug = True

    def _suc_log(self, *args, **kwargs):
        if self.debug:
            text = '\033[92m[Class:{}] '.format(self.__class__.__name__)
            text = self.__log(text, *args, **kwargs)
            return text

    def _warn_log(self, *args, **kwargs):
        text = '\033[93m[Class:{}] '.format(self.__class__.__name__)
        text = self.__log(text, *args, **kwargs)
        return text

    def _err_log(self, *args, **kwargs):
        text = '\033[91m[Class:{}] '.format(self.__class__.__name__)
        text = self.__log(text, *args, **kwargs)
        return text

    def __log(self, text, *args, **kwargs):
        for i in args:
            text += f'{i} '
        for key, value in kwargs.items():
            text += f'{key}={value} '
        text += '\033[0m'
        print(text)
        return text


class Log:
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    ALL = -1

    def __init__(self, theme: str):
        self.theme = theme
        self.logger = logging.getLogger(f'日志:{theme}')
        self.logger.setLevel(logging.DEBUG)
        self.formatter = {
            'standard': '[%(asctime)s] [%(name)s] |%(levelname)-8s| ',
            'message': '%(message)s ',
            'breakpoint': '[%(pathname)s:%(lineno)d] '
        }

    def add_logger(self, level: int, file_name: str = '', class_name: str = ''):
        # 根据日志级别构建不同的formatter
        if class_name == '':
            self.formatter['class_name'] = f"[{class_name}] "
        format_str = '%(message)s'
        if level == self.ALL:
            (self.add_logger(self.DEBUG, f'日志:{self.theme}_debug.log')
             .add_logger(self.INFO, f'日志:{self.theme}_info.log')
             .add_logger(self.WARNING, f'日志:{self.theme}_warning.log')
             .add_logger(self.ERROR, f'日志:{self.theme}_error.log')
             .add_logger(self.CRITICAL, f'日志:{self.theme}_critical.log')
             )
            return self
        elif level == logging.DEBUG or level == logging.INFO:
            format_str = self.formatter['standard'] + self.formatter['message']
        elif level == logging.WARNING or level == logging.ERROR:
            format_str = self.formatter['standard'] + self.formatter.get('class_name', '') + self.formatter['message']
        elif level == logging.CRITICAL:
            format_str = '\n' + self.formatter['standard'] + self.formatter.get('class_name', '') + self.formatter[
                'message'] + '\n' + self.formatter['breakpoint'] + '\n'
        if not file_name:
            file_name = f'{self.theme}_{level}.log'
        # 创建文件处理器
        handler = logging.FileHandler(file_name, encoding='utf-8')
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(format_str))
        self.logger.addHandler(handler)
        return self

    def __getattr__(self, item):
        return getattr(self.logger, item)

    def debug(self, message: str):
        self.logger.debug(message)
        return message

    def info(self, message: str):
        self.logger.info(message)
        return message

    def warning(self, message: str):
        self.logger.warning(message)
        return message

    def error(self, message: str):
        self.logger.error(message)
        return message

    def critical(self, message: str):
        self.logger.critical(message)
        return message
