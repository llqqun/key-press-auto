import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QDoubleSpinBox, QLabel, QHBoxLayout, QLineEdit, QApplication,
    QHeaderView, QCheckBox, QFileDialog, QDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from module.Step import Step
from config import config

class ShortcutConfigDialog(QDialog):
    """快捷键配置对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("配置快捷键")
        self.resize(400, 200)
        
        # 获取当前配置
        self.shortcuts = config.keys.copy()
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 创建表格用于显示和编辑快捷键
        self.table = QTableWidget(len(self.shortcuts), 2)
        self.table.setHorizontalHeaderLabels(["功能", "快捷键"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # 填充表格
        for row, shortcut in enumerate(self.shortcuts):
            # 功能列不可编辑
            func_item = QTableWidgetItem(shortcut["title"])
            func_item.setFlags(func_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 0, func_item)
            
            # 快捷键列可编辑
            key_item = QTableWidgetItem(shortcut["key"])
            self.table.setItem(row, 1, key_item)
        
        layout.addWidget(self.table)
        
        # 按钮行
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("保存")
        btn_save.clicked.connect(self.save_shortcuts)
        btn_layout.addWidget(btn_save)
        
        btn_cancel = QPushButton("取消")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def save_shortcuts(self):
        """保存快捷键配置"""
        # 更新快捷键配置
        for row in range(self.table.rowCount()):
            title = self.table.item(row, 0).text()
            key = self.table.item(row, 1).text()
            # 检查是否已存在相同的快捷键
            if any(shortcut["key"] == key for shortcut in self.shortcuts if shortcut["title"] != title):
                QMessageBox.warning(self, "警告", "快捷键已存在，请重新输入！")
                return
            
            # 查找对应的配置项并更新
            for shortcut in self.shortcuts:
                if shortcut["title"] == title:
                    shortcut["key"] = key
                    break
        
        # 更新全局配置
        config.keys = self.shortcuts
        config.save_config()
        
        QMessageBox.information(self, "提示", "快捷键配置已保存！")
        self.accept()

class MacroConfigWindow(QWidget):
    def __init__(self, executor):
        super().__init__()
        self.executor = executor
        self.setWindowTitle("按键精灵")
        self.resize(600, 400)

        layout = QVBoxLayout()

        # 表格：配置步骤
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["按键", "延迟(s)", "随机波动(s)", "操作"])
        # 设置表格水平大小策略为Expanding，使其宽度能够达到100%父元素
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # 控制循环参数
        loop_layout = QHBoxLayout()
        loop_layout.addWidget(QLabel("循环次数(0无限):"))
        self.loop_count = QSpinBox()
        self.loop_count.setRange(0, 9999)
        loop_layout.addWidget(self.loop_count)

        loop_layout.addWidget(QLabel("循环时长(秒,0无限):"))
        self.loop_time = QSpinBox()
        self.loop_time.setRange(0, 999999)
        loop_layout.addWidget(self.loop_time)
        layout.addLayout(loop_layout)
        
        # 添加鼠标连点复选框
        mouse_layout = QHBoxLayout()
        self.mouse_click_checkbox = QCheckBox("启用鼠标连点")
        self.mouse_click_checkbox.setChecked(self.executor.mouse_click_double)
        self.mouse_click_checkbox.stateChanged.connect(self.toggle_mouse_click)
        mouse_layout.addWidget(self.mouse_click_checkbox)
        
        # 添加pydirectinput游戏模式复选框
        self.game_mode_directinput_checkbox = QCheckBox("使用pydirectinput游戏模式")
        self.game_mode_directinput_checkbox.setChecked(False)  # 默认不启用
        self.game_mode_directinput_checkbox.stateChanged.connect(self.toggle_game_mode_directinput)
        mouse_layout.addWidget(self.game_mode_directinput_checkbox)
        
        # 添加到主布局
        layout.addLayout(mouse_layout)

        # 按钮行
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("添加步骤")
        btn_add.clicked.connect(self.add_step)
        btn_layout.addWidget(btn_add)

        btn_save = QPushButton("保存配置")
        btn_save.clicked.connect(self.save_config)
        btn_layout.addWidget(btn_save)
        
        btn_load = QPushButton("加载配置")
        btn_load.clicked.connect(self.load_config)
        btn_layout.addWidget(btn_load)

        self.start_btn = QPushButton("启动")
        self.start_btn.clicked.connect(self.start_macro)
        btn_layout.addWidget(self.start_btn)

        btn_stop = QPushButton("停止")
        btn_stop.clicked.connect(self.stop_macro)
        btn_layout.addWidget(btn_stop)
        
        # 添加快捷键配置按钮
        btn_shortcut = QPushButton("配置快捷键")
        btn_shortcut.clicked.connect(self.show_shortcut_config)
        btn_layout.addWidget(btn_shortcut)
        
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        
        # 初始化按钮文本，显示当前快捷键
        self.update_button_texts()

    def save_config(self):
        steps = []
        for row in range(self.table.rowCount()):
            key = self.table.item(row, 0).text()
            delay = float(self.table.item(row, 1).text())
            rand = float(self.table.item(row, 2).text())
            steps.append(Step(key, delay, rand))
        
        # 创建配置字典，包含步骤和循环参数
        config = {
            'steps': [step.to_dict() for step in steps],
            'loop_count': self.loop_count.value(),
            'loop_time': self.loop_time.value(),
            'mouse_click_double': self.executor.mouse_click_double
        }
        
        # 显示文件对话框让用户选择保存位置
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存配置", "", "JSON Files (*.json);;All Files (*)")
        
        if file_path:
            # 保存为JSON文件
            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            print(f"配置已保存到: {file_path}")

    def add_step(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem("a"))
        self.table.setItem(row, 1, QTableWidgetItem("0.1"))
        self.table.setItem(row, 2, QTableWidgetItem("0.1"))
        
        delete_btn = QPushButton("删除")
        delete_btn.clicked.connect(self.create_delete_handler())
        self.table.setCellWidget(row, 3, delete_btn)
        
    def create_delete_handler(self):
        # 创建删除处理函数，获取按钮的当前行索引
        return lambda: self.delete_step(self.get_button_row())
        
    def get_button_row(self):
        # 获取触发事件的按钮所在的行
        button = self.sender()
        if button:
            # 遍历表格查找按钮所在行
            for row in range(self.table.rowCount()):
                if self.table.cellWidget(row, 3) == button:
                    return row
        return -1
        
    def delete_step(self, row):
        if row >= 0:
            self.table.removeRow(row)
            
    def toggle_mouse_click(self, state):
        self.executor.mouse_click_double = (state == Qt.CheckState.Checked.value)
        
    def toggle_game_mode_directinput(self, state):
        """切换pydirectinput游戏模式"""
        self.executor.set_game_mode_directinput(state == Qt.CheckState.Checked.value)

    def start_macro(self):
        start_key = config.get_key_by_title("启动/暂停")
        print(self.executor.running, self.executor.paused)
        if self.executor.running and self.executor.paused:
            print('继续执行')
            # 继续执行同时修改按钮文案
            if start_key:
                self.start_btn.setText(f"暂停 {start_key}")
            else:
                self.start_btn.setText("暂停")
            self.executor.resume()
            return
        elif self.executor.running and not self.executor.paused:
            print('暂停执行')
            if start_key:
                self.start_btn.setText(f"继续 {start_key}")
            else:
                self.start_btn.setText("继续")
            self.executor.pause()
            return
        elif not self.executor.running:
            print('启动执行')
            if start_key:
                self.start_btn.setText(f"暂停 {start_key}")
            else:
                self.start_btn.setText("暂停")

        steps = []
        for row in range(self.table.rowCount()):
            key = self.table.item(row, 0).text()
            delay = float(self.table.item(row, 1).text())
            rand = float(self.table.item(row, 2).text())
            steps.append(Step(key, delay, rand))
        self.executor.load_steps(steps,
                                 loop_count=self.loop_count.value(),
                                 loop_time=self.loop_time.value())
        self.executor.start()

    def load_config(self):
        # 显示文件对话框让用户选择要加载的文件
        file_path, _ = QFileDialog.getOpenFileName(
            self, "加载配置", "", "JSON Files (*.json);;All Files (*)")
        
        if file_path:
            try:
                # 从JSON文件加载配置
                with open(file_path, "r", encoding='utf-8') as f:
                    config = json.load(f)
                
                # 清空现有表格内容
                self.table.setRowCount(0)
                
                # 加载步骤
                if 'steps' in config:
                    for step_data in config['steps']:
                        row = self.table.rowCount()
                        self.table.insertRow(row)
                        self.table.setItem(row, 0, QTableWidgetItem(step_data['key']))
                        self.table.setItem(row, 1, QTableWidgetItem(str(step_data['delay'])))
                        self.table.setItem(row, 2, QTableWidgetItem(str(step_data.get('random_offset', 0.1))))
                        
                        delete_btn = QPushButton("删除")
                        delete_btn.clicked.connect(self.create_delete_handler())
                        self.table.setCellWidget(row, 3, delete_btn)
                
                # 加载循环参数
                if 'loop_count' in config:
                    self.loop_count.setValue(config['loop_count'])
                if 'loop_time' in config:
                    self.loop_time.setValue(config['loop_time'])
                
                # 加载鼠标连点设置
                if 'mouse_click_double' in config:
                    self.mouse_click_checkbox.setChecked(config['mouse_click_double'])
                    self.executor.mouse_click_double = config['mouse_click_double']
                
                print(f"配置已从: {file_path} 加载")
            except Exception as e:
                print(f"加载配置失败: {str(e)}")

    def update_button_texts(self):
        """更新按钮文本，显示当前配置的快捷键"""
        start_key = config.get_key_by_title("启动/暂停")
        stop_key = config.get_key_by_title("停止")
        
        if start_key:
            self.start_btn.setText(f"启动 {start_key}")
        if stop_key:
            stop_btn = self.findChild(QPushButton, "")
            # 查找停止按钮
            for child in self.findChildren(QPushButton):
                if child.text().startswith("停止"):
                    child.setText(f"停止 {stop_key}")
                    break
    
    def show_shortcut_config(self):
        """显示快捷键配置对话框"""
        dialog = ShortcutConfigDialog(self)
        if dialog.exec():
            # 如果用户保存了配置，更新按钮文本
            self.update_button_texts()
    
    def stop_macro(self):
        start_key = config.get_key_by_title("启动/暂停")
        if start_key:
            self.start_btn.setText(f"启动 {start_key}")
        else:
            self.start_btn.setText("启动")
        self.executor.stop()
