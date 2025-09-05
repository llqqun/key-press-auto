import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QDoubleSpinBox, QLabel, QHBoxLayout, QLineEdit, QApplication,
    QHeaderView, QCheckBox, QFileDialog
)
from PyQt6.QtCore import Qt
from config import Step

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

        btn_start = QPushButton("启动")
        btn_start.clicked.connect(self.start_macro)
        btn_layout.addWidget(btn_start)

        btn_stop = QPushButton("停止")
        btn_stop.clicked.connect(self.stop_macro)
        btn_layout.addWidget(btn_stop)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

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
        self.table.setItem(row, 1, QTableWidgetItem("1.0"))
        self.table.setItem(row, 2, QTableWidgetItem("0.2"))
        
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

    def start_macro(self):
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

    def stop_macro(self):
        self.executor.stop()
