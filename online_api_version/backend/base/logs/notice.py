from win10toast_click import ToastNotifier


def __logIt():
    print("click!")


def win_notice(title: str = 'NoTitle', content: str = 'NoMSG', icon: str = '', dura: int = 5, func=__logIt):
    notifiers = ToastNotifier()
    if icon:
        notifiers.show_toast(title=title, msg=content, duration=dura, callback_on_click=func)
    else:
        notifiers.show_toast(title=title, msg=content, duration=dura, callback_on_click=func, icon_path=icon)


win_notice()
