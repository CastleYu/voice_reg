import time
import requests
from win10toast import ToastNotifier


def check_endpoint():
    url = "http://127.0.0.1:5000/get_all_user"
    toaster = ToastNotifier()
    try:
        response = requests.get(url, timeout=5)  # 超时时间可自行调整
        if response.status_code != 200:
            # 不是 200，发送通知
            toaster.show_toast(
                "接口状态异常",
                f"返回状态码：{response.status_code}",
                duration=10,  # 通知在桌面停留 10 秒，可自行修改
                threaded=True
            )
        else:
            import time
            print(f"{time.time()}")
    except Exception as e:
        # 接口无法正常访问，发送通知
        toaster.show_toast(
            "接口访问失败",
            str(e),
            duration=10,
            threaded=True
        )


if __name__ == "__main__":
    while True:
        check_endpoint()
        # 等待 30 分钟（1800 秒）后再次检查
        time.sleep(1800)
