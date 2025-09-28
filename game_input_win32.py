"""
基于pywin32的游戏输入模拟模块
通过Windows API直接模拟键盘和鼠标事件
提供最高级别的游戏兼容性
"""
import win32api
import win32con
import time

class GameWin32Input:
    def __init__(self):
        # 初始化Windows API相关常量
        self.VK_CODE = {
            'backspace': 0x08,
            'tab': 0x09,
            'clear': 0x0C,
            'enter': 0x0D,
            'shift': 0x10,
            'ctrl': 0x11,
            'alt': 0x12,
            'pause': 0x13,
            'caps_lock': 0x14,
            'esc': 0x1B,
            'space': 0x20,
            'page_up': 0x21,
            'page_down': 0x22,
            'end': 0x23,
            'home': 0x24,
            'left': 0x25,
            'up': 0x26,
            'right': 0x27,
            'down': 0x28,
            'select': 0x29,
            'print': 0x2A,
            'execute': 0x2B,
            'print_screen': 0x2C,
            'insert': 0x2D,
            'delete': 0x2E,
            'help': 0x2F,
            '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
            '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
            'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45,
            'f': 0x46, 'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A,
            'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F,
            'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54,
            'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59,
            'z': 0x5A,
            'numpad0': 0x60, 'numpad1': 0x61, 'numpad2': 0x62, 'numpad3': 0x63,
            'numpad4': 0x64, 'numpad5': 0x65, 'numpad6': 0x66, 'numpad7': 0x67,
            'numpad8': 0x68, 'numpad9': 0x69, 'multiply': 0x6A, 'add': 0x6B,
            'separator': 0x6C, 'subtract': 0x6D, 'decimal': 0x6E, 'divide': 0x6F,
            'f1': 0x70, 'f2': 0x71, 'f3': 0x72, 'f4': 0x73, 'f5': 0x74,
            'f6': 0x75, 'f7': 0x76, 'f8': 0x77, 'f9': 0x78, 'f10': 0x79,
            'f11': 0x7A, 'f12': 0x7B,
            'num_lock': 0x90, 'scroll_lock': 0x91,
            'lshift': 0xA0, 'rshift': 0xA1,
            'lcontrol': 0xA2, 'rcontrol': 0xA3,
            'lmenu': 0xA4, 'rmenu': 0xA5,
            'browser_back': 0xA6, 'browser_forward': 0xA7,
            'browser_refresh': 0xA8, 'browser_stop': 0xA9,
            'browser_search': 0xAA, 'browser_favorites': 0xAB,
            'browser_home': 0xAC,
            'volume_mute': 0xAD, 'volume_down': 0xAE, 'volume_up': 0xAF,
            'media_next_track': 0xB0, 'media_prev_track': 0xB1,
            'media_stop': 0xB2, 'media_play_pause': 0xB3,
            'launch_mail': 0xB4, 'launch_media_select': 0xB5,
            'launch_app1': 0xB6, 'launch_app2': 0xB7,
        }
        
    def _get_vk_code(self, key):
        """获取按键对应的虚拟键码"""
        # 转换为小写以保持一致性
        key_lower = key.lower()
        
        # 如果是单个字符，尝试直接映射
        if len(key) == 1 and key.isalnum():
            return self.VK_CODE.get(key_lower)
        
        # 否则查找特殊键映射
        return self.VK_CODE.get(key_lower)
        
    def _send_key_event(self, vk_code, is_down=True):
        """发送键盘事件到Windows系统"""
        # 0表示按键按下，win32con.KEYEVENTF_KEYUP表示按键释放
        flags = 0 if is_down else win32con.KEYEVENTF_KEYUP
        win32api.keybd_event(vk_code, 0, flags, 0)
        
    def press_key(self, key):
        """按下并释放指定的按键
        使用Windows API直接模拟键盘事件，提供最高级别的游戏兼容性
        """
        try:
            # 获取虚拟键码
            vk_code = self._get_vk_code(key)
            
            if vk_code is None:
                print(f"未找到键 {key} 对应的虚拟键码")
                return
            
            # 按下按键
            self._send_key_event(vk_code, is_down=True)
            
            # 短暂延迟确保按键被正确处理
            time.sleep(0.01)
            
            # 释放按键
            self._send_key_event(vk_code, is_down=False)
            
            # 按键之间的短暂延迟
            time.sleep(0.01)
            
        except Exception as e:
            print(f"按键模拟错误: {e}")
            
    def click(self, x=None, y=None, button='left'):
        """执行鼠标点击操作
        使用Windows API直接模拟鼠标事件
        """
        try:
            # 如果指定了坐标，先移动鼠标
            if x is not None and y is not None:
                win32api.SetCursorPos((x, y))
                time.sleep(0.01)  # 短暂延迟以确保鼠标移动到位
            
            # 确定鼠标按键
            if button == 'left':
                down_flag = win32con.MOUSEEVENTF_LEFTDOWN
                up_flag = win32con.MOUSEEVENTF_LEFTUP
            elif button == 'right':
                down_flag = win32con.MOUSEEVENTF_RIGHTDOWN
                up_flag = win32con.MOUSEEVENTF_RIGHTUP
            elif button == 'middle':
                down_flag = win32con.MOUSEEVENTF_MIDDLEDOWN
                up_flag = win32con.MOUSEEVENTF_MIDDLEUP
            else:
                print(f"不支持的鼠标按键: {button}")
                return
            
            # 获取当前鼠标位置
            current_x, current_y = win32api.GetCursorPos()
            
            # 执行鼠标点击
            win32api.mouse_event(down_flag, current_x, current_y, 0, 0)
            time.sleep(0.01)  # 短暂延迟
            win32api.mouse_event(up_flag, current_x, current_y, 0, 0)
            
            # 点击之间的短暂延迟
            time.sleep(0.01)
            
        except Exception as e:
            print(f"鼠标点击错误: {e}")
            
    def hold_key(self, key):
        """按住指定的按键不释放
        适用于需要长按的操作
        """
        try:
            # 获取虚拟键码
            vk_code = self._get_vk_code(key)
            
            if vk_code is None:
                print(f"未找到键 {key} 对应的虚拟键码")
                return
            
            # 按下按键
            self._send_key_event(vk_code, is_down=True)
            
        except Exception as e:
            print(f"按键按下错误: {e}")
            
    def release_key(self, key):
        """释放之前按住的按键
        配合hold_key使用
        """
        try:
            # 获取虚拟键码
            vk_code = self._get_vk_code(key)
            
            if vk_code is None:
                print(f"未找到键 {key} 对应的虚拟键码")
                return
            
            # 释放按键
            self._send_key_event(vk_code, is_down=False)
            
        except Exception as e:
            print(f"按键释放错误: {e}")