from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QDoubleSpinBox, QLabel, QHBoxLayout, QLineEdit, QApplication,
    QHeaderView, QCheckBox
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

    def stop_macro(self):
        self.executor.stop()
