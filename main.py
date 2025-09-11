import sys
import keyboard
from PyQt6.QtWidgets import QApplication
from gui import MacroConfigWindow
from executor import MacroExecutor
from config import config

def main():
    app = QApplication(sys.argv)

    executor = MacroExecutor()
    window = MacroConfigWindow(executor)
    window.show()

    # 全局热键绑定 - 从配置中获取快捷键
    start_key = config.get_key_by_title("启动/暂停")
    stop_key = config.get_key_by_title("停止")
    
    if start_key:
        keyboard.add_hotkey(start_key, lambda: window.start_macro())
    if stop_key:
        keyboard.add_hotkey(stop_key, lambda: window.stop_macro())

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
