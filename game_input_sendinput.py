"""
游戏兼容的输入模拟模块
使用Windows SendInput API提供底层的键盘和鼠标控制
专为游戏环境设计，解决PyAutoGUI和pydirectinput在游戏中不工作的问题
"""
import ctypes
import time
import win32con
import win32api
from ctypes import wintypes

# Windows API常量
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

# 鼠标事件常量
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_ABSOLUTE = 0x8000

# 键盘事件常量
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

# 定义结构体
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD)
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT)
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", INPUT_UNION)
    ]

# 虚拟键码映射
VK_CODE = {
    'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45, 'f': 0x46, 'g': 0x47, 'h': 0x48,
    'i': 0x49, 'j': 0x4A, 'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F, 'p': 0x50,
    'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54, 'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58,
    'y': 0x59, 'z': 0x5A,
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35, '6': 0x36, '7': 0x37,
    '8': 0x38, '9': 0x39,
    'space': 0x20, 'enter': 0x0D, 'esc': 0x1B, 'tab': 0x09,
    'up': 0x26, 'down': 0x28, 'right': 0x27, 'left': 0x25,
    'backspace': 0x08, 'delete': 0x2E,
    'shift': 0x10, 'ctrl': 0x11, 'alt': 0x12,
    'f1': 0x70, 'f2': 0x71, 'f3': 0x72, 'f4': 0x73, 'f5': 0x74, 'f6': 0x75,
    'f7': 0x76, 'f8': 0x77, 'f9': 0x78, 'f10': 0x79, 'f11': 0x7A, 'f12': 0x7B
}

class GameSendInput:
    def __init__(self):
        # 初始化SendInput API
        self.user32 = ctypes.windll.user32
        self.user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
        self.user32.SendInput.restype = wintypes.UINT
        
        # 获取屏幕尺寸
        self.screen_width = win32api.GetSystemMetrics(0)
        self.screen_height = win32api.GetSystemMetrics(1)
        
    def _send_input(self, inputs):
        """发送输入事件"""
        n_inputs = len(inputs)
        arr = INPUT * n_inputs
        input_arr = arr(*inputs)
        
        result = self.user32.SendInput(n_inputs, input_arr, ctypes.sizeof(INPUT))
        if result != n_inputs:
            print(f"SendInput失败，发送了{result}/{n_inputs}个事件")
            
        # 短暂延迟确保事件被处理
        time.sleep(0.01)
        
    def _create_mouse_input(self, dx, dy, flags, mouse_data=0):
        """创建鼠标输入事件"""
        mi = MOUSEINPUT()
        mi.dx = dx
        mi.dy = dy
        mi.mouseData = mouse_data
        mi.dwFlags = flags
        mi.time = 0
        mi.dwExtraInfo = None
        
        inp = INPUT()
        inp.type = INPUT_MOUSE
        inp.union.mi = mi
        
        return inp
        
    def _create_keyboard_input(self, vk, scan, flags):
        """创建键盘输入事件"""
        ki = KEYBDINPUT()
        ki.wVk = vk
        ki.wScan = scan
        ki.dwFlags = flags
        ki.time = 0
        ki.dwExtraInfo = None
        
        inp = INPUT()
        inp.type = INPUT_KEYBOARD
        inp.union.ki = ki
        
        return inp
        
    def press_key(self, key):
        """按下并释放指定的按键"""
        try:
            # 获取虚拟键码
            key_lower = key.lower()
            if key_lower in VK_CODE:
                vk = VK_CODE[key_lower]
            elif len(key) == 1 and key.isalnum():
                # 对于未映射的单字符，尝试转换为大写获取虚拟键码
                vk = ord(key.upper())
            else:
                print(f"未映射的键: {key}")
                return
                
            # 发送按键按下和释放事件
            inputs = [
                self._create_keyboard_input(vk, 0, 0),  # 按键按下
                self._create_keyboard_input(vk, 0, KEYEVENTF_KEYUP)  # 按键释放
            ]
            
            self._send_input(inputs)
            
        except Exception as e:
            print(f"按键模拟错误: {e}")
    
    def click(self, x=None, y=None, button='left'):
        """执行鼠标点击操作"""
        try:
            # 如果指定了坐标，先移动鼠标
            if x is not None and y is not None:
                # 转换为绝对坐标
                abs_x = int(x * 65535 / self.screen_width)
                abs_y = int(y * 65535 / self.screen_height)
                
                # 发送鼠标移动事件
                move_input = self._create_mouse_input(abs_x, abs_y, MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE)
                self._send_input([move_input])
            
            # 根据按钮类型发送点击事件
            if button == 'left':
                down_flag = MOUSEEVENTF_LEFTDOWN
                up_flag = MOUSEEVENTF_LEFTUP
            elif button == 'right':
                down_flag = MOUSEEVENTF_RIGHTDOWN
                up_flag = MOUSEEVENTF_RIGHTUP
            elif button == 'middle':
                down_flag = MOUSEEVENTF_MIDDLEDOWN
                up_flag = MOUSEEVENTF_MIDDLEUP
            else:
                print(f"不支持的鼠标按钮: {button}")
                return
            
            # 发送鼠标按下和释放事件
            inputs = [
                self._create_mouse_input(0, 0, down_flag),  # 鼠标按下
                self._create_mouse_input(0, 0, up_flag)    # 鼠标释放
            ]
            
            self._send_input(inputs)
            
        except Exception as e:
            print(f"鼠标点击错误: {e}")
            
    def hold_key(self, key):
        """按住指定的按键不释放"""
        try:
            # 获取虚拟键码
            key_lower = key.lower()
            if key_lower in VK_CODE:
                vk = VK_CODE[key_lower]
            elif len(key) == 1 and key.isalnum():
                vk = ord(key.upper())
            else:
                print(f"未映射的键: {key}")
                return
                
            # 发送按键按下事件
            input_event = self._create_keyboard_input(vk, 0, 0)
            self._send_input([input_event])
            
        except Exception as e:
            print(f"按键按下错误: {e}")
            
    def release_key(self, key):
        """释放之前按住的按键"""
        try:
            # 获取虚拟键码
            key_lower = key.lower()
            if key_lower in VK_CODE:
                vk = VK_CODE[key_lower]
            elif len(key) == 1 and key.isalnum():
                vk = ord(key.upper())
            else:
                print(f"未映射的键: {key}")
                return
                
            # 发送按键释放事件
            input_event = self._create_keyboard_input(vk, 0, KEYEVENTF_KEYUP)
            self._send_input([input_event])
            
        except Exception as e:
            print(f"按键释放错误: {e}")