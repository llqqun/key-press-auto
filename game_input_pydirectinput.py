"""
游戏兼容的输入模拟模块
使用pydirectinput库提供底层的键盘和鼠标控制
专为游戏环境设计，解决PyAutoGUI在游戏中不工作的问题
"""
import pydirectinput
import time

class GameDirectInput:
    def __init__(self):
        # 初始化pydirectinput
        # 可以根据需要设置一些配置选项
        pydirectinput.PAUSE = 0.01  # 设置默认延迟，可根据需要调整
        
    def press_key(self, key):
        """按下并释放指定的按键
        使用pydirectinput提供的底层按键模拟，提高与游戏的兼容性
        """
        try:
            # 对于单字符键，直接使用字符
            if len(key) == 1 and key.isalnum():
                pydirectinput.press(key)
            # 对于特殊键，需要处理
            else:
                # 常见特殊键的映射
                special_keys = {
                    'space': 'space',
                    'enter': 'enter',
                    'esc': 'esc',
                    'tab': 'tab',
                    'up': 'up',
                    'down': 'down',
                    'right': 'right',
                    'left': 'left',
                    'backspace': 'backspace',
                    'delete': 'delete',
                    'shift': 'shift',
                    'ctrl': 'ctrl',
                    'alt': 'alt',
                    'f1': 'f1',
                    'f2': 'f2',
                    'f3': 'f3',
                    'f4': 'f4',
                    'f5': 'f5',
                    'f6': 'f6',
                    'f7': 'f7',
                    'f8': 'f8',
                    'f9': 'f9',
                    'f10': 'f10',
                    'f11': 'f11',
                    'f12': 'f12'
                }
                
                # 检查是否是特殊键
                key_lower = key.lower()
                if key_lower in special_keys:
                    pydirectinput.press(special_keys[key_lower])
                else:
                    # 默认情况下尝试使用原始键
                    print(f"尝试使用未映射的键: {key}")
                    pydirectinput.press(key)
                     
                # 短暂延迟确保按键被正确处理
                time.sleep(0.01)
        except Exception as e:
            print(f"按键模拟错误: {e}")
    
    def click(self, x=None, y=None, button='left'):
        """执行鼠标点击操作
        使用pydirectinput提供的底层鼠标模拟
        """
        try:
            # 如果指定了坐标，先移动鼠标
            if x is not None and y is not None:
                pydirectinput.moveTo(x, y)
                time.sleep(0.01)  # 短暂延迟以确保鼠标移动到位
            
            # 执行点击
            if button == 'left':
                pydirectinput.click(button='left')
            elif button == 'right':
                pydirectinput.click(button='right')
            elif button == 'middle':
                pydirectinput.click(button='middle')
            
            # 短暂延迟确保点击被正确处理
            time.sleep(0.01)
        except Exception as e:
            print(f"鼠标点击错误: {e}")
            
    def hold_key(self, key):
        """按住指定的按键不释放
        适用于需要长按的操作
        """
        try:
            # 对于单字符键，直接使用字符
            if len(key) == 1 and key.isalnum():
                pydirectinput.keyDown(key)
            # 对于特殊键，需要处理
            else:
                special_keys = {
                    'space': 'space',
                    'enter': 'enter',
                    'esc': 'esc',
                    'tab': 'tab',
                    'up': 'up',
                    'down': 'down',
                    'right': 'right',
                    'left': 'left',
                    'shift': 'shift',
                    'ctrl': 'ctrl',
                    'alt': 'alt'
                }
                
                key_lower = key.lower()
                if key_lower in special_keys:
                    pydirectinput.keyDown(special_keys[key_lower])
                else:
                    pydirectinput.keyDown(key)
        except Exception as e:
            print(f"按键按下错误: {e}")
            
    def release_key(self, key):
        """释放之前按住的按键
        配合hold_key使用
        """
        try:
            # 对于单字符键，直接使用字符
            if len(key) == 1 and key.isalnum():
                pydirectinput.keyUp(key)
            # 对于特殊键，需要处理
            else:
                special_keys = {
                    'space': 'space',
                    'enter': 'enter',
                    'esc': 'esc',
                    'tab': 'tab',
                    'up': 'up',
                    'down': 'down',
                    'right': 'right',
                    'left': 'left',
                    'shift': 'shift',
                    'ctrl': 'ctrl',
                    'alt': 'alt'
                }
                
                key_lower = key.lower()
                if key_lower in special_keys:
                    pydirectinput.keyUp(special_keys[key_lower])
                else:
                    pydirectinput.keyUp(key)
        except Exception as e:
            print(f"按键释放错误: {e}")