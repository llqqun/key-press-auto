import sys
import keyboard
from PyQt6.QtWidgets import QApplication
from gui import MacroConfigWindow
from executor import MacroExecutor

def main():
    app = QApplication(sys.argv)

    executor = MacroExecutor()
    window = MacroConfigWindow(executor)
    window.show()

    # 全局热键绑定
    keyboard.add_hotkey("f12", lambda: executor.pause())
    keyboard.add_hotkey("f11", lambda: executor.resume())

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
