import pyautogui
import time
import threading
import keyboard

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
        self.thread_mouse = threading.Thread(target=self.run_mouse, daemon=True)
        self.thread.start()
        self.thread_mouse.start()

    def stop(self):
        print("停止")
        self.running = False

    def pause(self):
        print("暂停")
        self.paused = True

    def resume(self):
        print("继续")
        self.start()

    def run_loop(self):
        start_time = time.time()
        count = 0
        while self.running:
            if self.loop_count and count >= self.loop_count:
                break
            if self.loop_time and (time.time() - start_time >= self.loop_time):
                break
            print('任务运行中...')
            for step in self.steps:
                if not self.running:
                    break
                while self.paused:
                    time.sleep(0.1)

                pyautogui.press(step.key)
                
                # 如果启用了鼠标连点功能，执行鼠标点击
                # if self.mouse_click_double:
                #     pyautogui.click()
                    
                wait_time = step.get_wait_time()
                time.sleep(max(0, wait_time))
            count += 1

        print('任务暂停...')
        self.running = False

    def run_mouse(self):
        while self.running:
            if self.paused:
                time.sleep(0.1)
                continue
            if self.mouse_click_double:
                pyautogui.click()
            time.sleep(0.05)
