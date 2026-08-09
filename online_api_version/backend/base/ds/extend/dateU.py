from datetime import datetime, timezone, timedelta


class DateParserCore:
    def __init__(self):
        self.parser: DateParser = None
        self.error_tuple: tuple = None

    def parse(self, date_str):
        if not self.parser:
            raise ValueError("Parser is not set.")
        return self.parser.parse(date_str)

    def _set_parser(self, parser_cls, *args):
        # 将解析器类的实例化对象赋值给 self.parser
        instance = parser_cls()
        self.parser = instance
        self.error_tuple = instance.error_tuple
        return self

    def __call__(self, parser_cls):
        cls_func_map = {
            DateParser: self._set_parser,  # 定义类型到方法的映射
        }

        # 遍历 map，找到合适的处理函数
        for base_cls, handler in cls_func_map.items():
            if issubclass(parser_cls, base_cls):
                return handler(parser_cls)

        raise ValueError(f"Unsupported parser type: {parser_cls.__name__}")


class DateParser:
    def parse(self, time_string):
        raise NotImplementedError("Subclasses should implement this method.")


class MomentDateParser(DateParser):
    def parse(self, time_string):
        import moment
        return moment.date(time_string).datetime


class DateutilDateParser(DateParser):
    def __init__(self):
        from dateutil.parser import ParserError
        self.error_tuple = (ParserError,)

    def parse(self, time_string):
        from dateutil.parser import parser
        return parser().parse(timestr=time_string)


date_core = DateParserCore()
date_core(DateutilDateParser)


def parse_date(date, date_parser_core: DateParserCore = date_core):
    try:
        if isinstance(date, str):
            parsed_date = date_parser_core.parse(date)
        elif isinstance(date, datetime):
            parsed_date = date
        else:
            raise TypeError(f'date:\n-> Expected: str | datetime\n-> Got Item: {type(date)}\n-> DataValue: {date}')
        if parsed_date.tzinfo:
            parsed_date = parsed_date.astimezone(timezone(timedelta(hours=8)))
        return parsed_date.replace(tzinfo=None)
    except date_parser_core.error_tuple:
        return None


def parse_date_to_string(date, date_parser_core: DateParserCore = date_core):
    parsed_date = parse_date(date, date_parser_core)
    return parsed_date.strftime('%Y-%m-%d %H:%M:%S')


def compare_dates(date1, date2, date_parser_core: DateParserCore = date_core):
    parsed_date1 = parse_date(date1, date_parser_core)
    parsed_date2 = parse_date(date2, date_parser_core)

    if parsed_date1 < parsed_date2:
        return "<"
    elif parsed_date1 > parsed_date2:
        return ">"
    else:
        return "="
