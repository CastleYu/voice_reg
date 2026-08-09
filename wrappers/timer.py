import time


def timerC(func):
    def wrapper(*args, **kwargs):
        # 记录开始时间
        start_time = time.time()
        # 执行原始函数
        result = func(*args, **kwargs)
        # 记录结束时间
        end_time = time.time()
        # 计算并输出运行时间
        run_time = end_time - start_time
        print(f"函数 '{func.__name__}' 运行时间 {run_time:.4f} 秒")
        return result

    return wrapper
