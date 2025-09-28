import pyautogui
import time
import threading
from game_input_pydirectinput import GameDirectInput  # 导入使用pydirectinput的游戏输入模块
from game_input_win32 import GameWin32Input  # 导入使用pywin32的游戏输入模块

class MacroExecutor:
    def __init__(self):
        self.steps = [] # 执行步骤
        self.running = False # 是否运行
        self.paused = False # 是否暂停
        self.mouse_click_double = False # 鼠标连点
        self.loop_count = 0 # 循环次数
        self.loop_time = 0 # 循环时间
        self.thread = None  # 键盘线程
        self.thread_mouse = None  # 鼠标线程
        self.game_mode_directinput = False  # pydirectinput游戏模式标志
        self.game_mode_win32 = False  # pywin32游戏模式标志
        self.game_direct_input = GameDirectInput()  # 创建pydirectinput实例
        self.game_win32_input = GameWin32Input()  # 创建pywin32实例


    def load_steps(self, steps, loop_count=0, loop_time=0):
        """设置流程与循环参数"""
        self.steps = steps
        self.loop_count = loop_count
        self.loop_time = loop_time

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        print("启动")
        self.running = True
        self.paused = False
        self.thread = threading.Thread(target=self.run_loop, daemon=True)
        self.thread.start()

        if self.mouse_click_double:
            self.thread_mouse = threading.Thread(target=self.run_mouse, daemon=True)
            self.thread_mouse.start()

    def stop(self):
        print("停止")
        self.running = False
        self.paused = False

    def pause(self):
        print("暂停")
        self.paused = True

    def resume(self):
        print("继续")
        self.paused = False
        
    def set_game_mode_directinput(self, enabled):
        """设置是否使用SendInput游戏模式"""
        self.game_mode_directinput = enabled
        # 如果启用了pydirectinput模式，自动禁用win32模式
        if enabled:
            self.game_mode_win32 = False
            
    def set_game_mode_win32(self, enabled):
        """设置是否使用pywin32游戏模式"""
        self.game_mode_win32 = enabled
        # 如果启用了win32模式，自动禁用pydirectinput模式
        if enabled:
            self.game_mode_directinput = False

    def run_loop(self):
        start_time = time.time()
        count = 0
        while self.running:
            if self.loop_count and count >= self.loop_count:
                break
            if self.loop_time and (time.time() - start_time >= self.loop_time):
                break

            for step in self.steps:
                if not self.running:
                    break
                while self.paused:
                    time.sleep(1)

                # 根据模式选择不同的按键模拟方法
                if self.game_mode_win32:
                    self.game_win32_input.press_key(step.key)
                elif self.game_mode_directinput:
                    self.game_direct_input.press_key(step.key)
                else:
                    pyautogui.press(step.key)
                    
                wait_time = step.get_wait_time()
                time.sleep(max(0, wait_time))
            count += 1

    def run_mouse(self):
        while self.running:
            if self.paused:
                time.sleep(1)
                continue
            if self.mouse_click_double:
                # 根据模式选择不同的鼠标点击方法
                    if self.game_mode_win32:
                        self.game_win32_input.click()
                    elif self.game_mode_directinput:
                        self.game_direct_input.click()
                    else:
                        pyautogui.click()
            time.sleep(0.05)
