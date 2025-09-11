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
    keyboard.add_hotkey("f10", lambda: window.start_macro())
    keyboard.add_hotkey("f11", lambda: window.stop_macro())

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
