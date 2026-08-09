import time
from datetime import datetime


def get_today_timestamps():
    today = datetime.now().date()
    start_of_today = datetime.combine(today, datetime.min.time())
    end_of_today = datetime.combine(today, datetime.max.time())
    start_timestamp = int(start_of_today.timestamp())
    end_timestamp = int(end_of_today.timestamp())
    return start_timestamp, end_timestamp


def is_in_today(timestamp):
    start_timestamp, end_timestamp = get_today_timestamps()
    return start_timestamp <= timestamp <= end_timestamp


def time_to_str(timestamp):
    # 使用 fromtimestamp 方法将时间戳转换为 datetime 对象
    dt_object = datetime.fromtimestamp(timestamp)
    # 格式化日期时间为可读字符串，例如：2024-09-15 10:23:45
    readable_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return readable_string


last_time = time.perf_counter()


def print_time(index):
    global last_time
    now_time = time.perf_counter()
    print(f'{index}:{now_time - last_time:.4f}')
    last_time = now_time
