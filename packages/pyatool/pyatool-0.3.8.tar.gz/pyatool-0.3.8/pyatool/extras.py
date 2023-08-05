import requests
import tempfile
import os
import re
import platform

SYSTEM_TYPE = platform.system()


def hello_world(toolkit=None):
    """
    test only

    :param toolkit:
    :return:
    """
    # toolkit contains some tools for development
    # get device id
    device_id = toolkit.device_id
    print(device_id)
    # use adb
    toolkit.adb.run(['shell', 'ps'])


def install_from(url: str = None, path: str = None, toolkit=None):
    """
    根据url或path安装指定apk

    :param url: apk对应的下载url
    :param path: apk的本地路径
    :param toolkit:
    :return:
    """
    if (not (url or path)) or (url and path):
        raise TypeError('need url or path for installation, not both or none')
    if url and not path:
        return _install_from_url(url, toolkit)
    else:
        return _install_from_path(path, toolkit)


def _install_from_url(url, toolkit=None):
    resp = requests.get(url)
    if not resp.ok:
        return False
    with tempfile.NamedTemporaryFile('wb+', suffix='.apk', delete=False) as temp:
        temp.write(resp.content)
        temp.close()
        toolkit.adb.run(['install', '-r', '-d', '-t', temp.name])
        os.remove(temp.name)
    return True


def _install_from_path(path, toolkit=None):
    return toolkit.adb.run(['install', '-r', '-d', '-t', path])


def get_current_activity(toolkit=None):
    """
    获取设备的当前栈顶activity名称

    :param toolkit:
    :return:
    """

    # TODO if sh has installed in windows, command is same as linux ..
    # filter_name = 'findstr' if SYSTEM_TYPE == 'Windows' else 'grep'
    return toolkit.adb.run(['shell', 'dumpsys', 'activity', 'top', '|', 'grep', 'ACTIVITY'])


def is_installed(package_name: str, toolkit=None):
    """
    检测包是否已被安装到设备上

    :param package_name: 待检测的包名
    :param toolkit:
    :return:
    """
    return package_name in show_package(toolkit)


def show_package(toolkit=None):
    """
    展示设备上所有已安装的包

    :param toolkit:
    :return:
    """
    return toolkit.adb.run(['shell', 'pm', 'list', 'package'])


def clean_cache(package_name: str, toolkit=None):
    """
    清理对应包的缓存

    :param package_name: 对应包名
    :param toolkit:
    :return:
    """
    return toolkit.adb.run(['shell', 'pm', 'clear', package_name])


def uninstall(package_name: str, toolkit=None, save_data: bool = None):
    """
    卸载指定包

    :param package_name: 对应包名
    :param toolkit:
    :param save_data: 是否保留data
    :return:
    """
    if save_data:
        cmd_list = ['uninstall', '-k', package_name]
    else:
        cmd_list = ['uninstall', package_name]
    return toolkit.adb.run(cmd_list)


def switch_airplane(status: bool, toolkit=None):
    """
    切换飞行模式的开关

    :param status: true or false
    :param toolkit:
    :return:
    """
    base_setting_cmd = ["shell", "settings", "put", "global", "airplane_mode_on"]
    base_am_cmd = ["shell", "am", "broadcast", "-a", "android.intent.action.AIRPLANE_MODE", "--ez", "state"]
    if status:
        base_setting_cmd += ['1']
        base_am_cmd += ['true']
    else:
        base_setting_cmd += ['0']
        base_am_cmd += ['false']
    toolkit.adb.run(base_setting_cmd)
    toolkit.adb.run(base_am_cmd)


def switch_wifi(status: bool, toolkit=None):
    """
    切换wifi开关

    :param status: true or false
    :param toolkit:
    :return:
    """
    base_cmd = ['shell', 'svc', 'wifi']
    cmd_dict = {
        True: base_cmd + ['enable'],
        False: base_cmd + ['disable'],
    }
    toolkit.adb.run(cmd_dict[status])


def switch_screen(status: bool, toolkit=None):
    """
    点亮/熄灭 屏幕

    :param status: true or false
    :param toolkit:
    :return:
    """
    base_cmd = ['shell', 'input', 'keyevent']
    cmd_dict = {
        True: base_cmd + ['224'],
        False: base_cmd + ['223'],
    }
    toolkit.adb.run(cmd_dict[status])


def input_text(content: str, toolkit=None):
    """
    输入文字（不支持中文）。中文输入可以利用ADBKeyBoard (https://github.com/senzhk/ADBKeyBoard)

    :param content: 期望的输入内容
    :param toolkit:
    :return:
    """
    toolkit.adb.run(['shell', 'input', 'text', content])


def start_activity(package_name: str, activity_name: str = None, toolkit=None):
    """
    根据包名/活动名 启动应用/活动 （更复杂场景请使用 start_activity_with_command）

    :param package_name: 包名
    :param activity_name: 活动名
    :param toolkit:
    :return:
    """
    base_cmd = ['shell', 'am', 'start']
    if not activity_name:
        return toolkit.adb.run(base_cmd + [package_name])
    return toolkit.adb.run(base_cmd + ['{}/.{}'.format(package_name, activity_name)])


def start_activity_with_command(command: str, toolkit=None):
    """
    更灵活的 start_activity，实际上是运行 adb shell am start <command>

    :param command: adb shell am start <command>
    :param toolkit:
    :return:
    """
    return toolkit.adb.run(['shell', 'am', 'start', command.split(' ')])


def force_stop(package_name: str, toolkit=None):
    """
    根据包名/活动名 停止应用

    :param package_name: 包名
    :param toolkit:
    :return:
    """
    return toolkit.adb.run(['shell', 'am', 'force-stop', package_name])


def _clean_backstage(toolkit=None):
    """
    （无效）清理后台应用/进程

    :param toolkit:
    :return:
    """
    return toolkit.adb.run(['shell', 'am', 'kill-all'])


def send_broadcast(command: str, toolkit=None):
    """
    发送广播，实际上是 adb shell am broadcast <command>

    :param command: 在 am broadcast 后的命令
    :param toolkit:
    :return:
    """
    return toolkit.adb.run(['shell', 'am', 'start', command.split(' ')])


def input_key_event(key_code, toolkit=None):
    """
    send key event

    :param key_code: 按钮对应的 keycode， 例如home键是3。参考https://developer.android.com/reference/kotlin/android/view/KeyEvent
    :param toolkit:
    :return:
    """
    return toolkit.adb.run(['shell', 'input', 'keyevent', str(key_code)])


def swipe(x1, y1, x2, y2, toolkit=None):
    """
    swipe from (x1, y1) to (x2, y2)

    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :param toolkit:
    :return:
    """
    x1, y1, x2, y2 = map(str, (x1, y1, x2, y2))
    return toolkit.adb.run(['shell', 'input', 'swipe', x1, y1, x2, y2])


def click(x, y, toolkit=None):
    """
    click (x, y)

    :param x:
    :param y:
    :param toolkit:
    :return:
    """
    return toolkit.adb.run(['shell', 'input', 'tap', str(x), str(y)])


def get_ip_address(toolkit=None):
    """
    获取android设备ip地址

    :param toolkit:
    :return:
    """
    # TODO better design?
    result = toolkit.adb.run(['shell', 'ifconfig', 'wlan0'])
    return re.findall(r'inet\s*addr:(.*?)\s', result, re.DOTALL)[0]


def set_ime(ime_name, toolkit=None):
    """
    设置输入法（需要使用adb shell ime list -a 获取输入法包名）

    :param ime_name: 输入法包名 eg：com.android.inputmethod.pinyin/.PinyinIME
    :param toolkit:
    :return:
    """
    return toolkit.adb.run(['shell', 'ime', 'set', ime_name])


def pull(src, target, toolkit=None):
    """
    adb pull <src> <target>

    :param src:
    :param target:
    :param toolkit:
    :return:
    """
    return toolkit.adb.run(['pull', src, target])


def push(src, target, toolkit=None):
    """
    adb push <src> <target>

    :param src:
    :param target:
    :param toolkit:
    :return:
    """
    return toolkit.adb.run(['push', src, target])


def is_connected(toolkit=None):
    """
    check if device is connected

    :param toolkit:
    :return:
    """
    try:
        toolkit.adb.run(['shell', 'echo', '"hello"'])
    except RuntimeError:
        return False
    return True


def make_dir(target, toolkit=None):
    """
    make empty dir: adb shell mkdir <target_dir>

    :param target: 目标路径
    :param toolkit:
    :return:
    """
    return toolkit.adb.run(['shell', 'mkdir', target])


def remove_dir(target, toolkit=None):
    """
    clean dir: adb shell rm -rf <target>

    :param target: 目标路径
    :param toolkit:
    :return:
    """
    return toolkit.adb.run(['shell', 'rm', '-rf', target])


__all__ = [
    'hello_world',

    'install_from',
    'show_package',
    'get_current_activity',
    'is_installed',
    'clean_cache',
    'uninstall',
    'switch_airplane',
    'switch_wifi',
    'input_text',
    'start_activity',
    'start_activity_with_command',
    'get_ip_address',
    'set_ime',
    'push',
    'pull',
    'send_broadcast',
    'force_stop',
    'input_key_event',
    'swipe',
    'click',
    'is_connected',
    'make_dir',
    'remove_dir',
]
