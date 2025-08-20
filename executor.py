import pyautogui
import time
import threading
import keyboard

class MacroExecutor:
    def __init__(self):
        self.steps = []
        self.running = False
        self.paused = False
        self.mouse_click_double = False # 鼠标连点
        self.loop_count = 0 # 循环次数
        self.loop_time = 0 # 循环时间
        self.thread = None

    def load_steps(self, steps, loop_count=0, loop_time=0):
        """设置流程与循环参数"""
        self.steps = steps
        self.loop_count = loop_count
        self.loop_time = loop_time

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.running = True
        self.paused = False
        self.thread = threading.Thread(target=self.run_loop, daemon=True)
        self.thread.start()

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

            for step in self.steps:
                if not self.running:
                    break
                while self.paused:
                    time.sleep(0.1)

                pyautogui.press(step.key)
                wait_time = step.get_wait_time()
                time.sleep(max(0, wait_time))
            count += 1

        self.running = False
