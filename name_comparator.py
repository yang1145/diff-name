import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QSplitter, QGroupBox, QMessageBox)
from PyQt5.QtCore import Qt


class NameComparatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('姓名比较工具')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建分隔器用于左右布局
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧输入区域
        input_group = QGroupBox("输入姓名列表")
        input_layout = QHBoxLayout(input_group)
        
        # 第一列输入
        col1_layout = QVBoxLayout()
        col1_layout.addWidget(QLabel("第一列姓名:"))
        self.col1_text = QTextEdit()
        self.col1_text.setPlaceholderText("每行输入一个姓名...")
        col1_layout.addWidget(self.col1_text)
        input_layout.addLayout(col1_layout)
        
        # 第二列输入
        col2_layout = QVBoxLayout()
        col2_layout.addWidget(QLabel("第二列姓名:"))
        self.col2_text = QTextEdit()
        self.col2_text.setPlaceholderText("每行输入一个姓名...")
        col2_layout.addWidget(self.col2_text)
        input_layout.addLayout(col2_layout)
        
        # 右侧结果区域
        result_group = QGroupBox("比较结果")
        result_layout = QVBoxLayout(result_group)
        
        # 结果表格
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["唯一姓名", "来源列", "状态"])
        result_layout.addWidget(self.result_table)
        
        # 添加到分隔器
        splitter.addWidget(input_group)
        splitter.addWidget(result_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        self.compare_btn = QPushButton("比较姓名")
        self.compare_btn.clicked.connect(self.compare_names)
        self.clear_btn = QPushButton("清空")
        self.clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(self.compare_btn)
        button_layout.addWidget(self.clear_btn)
        main_layout.addLayout(button_layout)
        
        # 状态栏
        self.statusBar().showMessage('就绪')
    
    def compare_names(self):
        # 获取两个文本框的内容并分割成列表
        col1_text = self.col1_text.toPlainText().strip()
        col2_text = self.col2_text.toPlainText().strip()
        
        # 处理空输入情况
        if not col1_text and not col2_text:
            QMessageBox.warning(self, "警告", "请至少在一列中输入姓名！")
            return
        
        # 将文本分割为姓名列表
        names1 = set(filter(None, [name.strip() for name in col1_text.split('\n')])) if col1_text else set()
        names2 = set(filter(None, [name.strip() for name in col2_text.split('\n')])) if col2_text else set()
        
        # 找出不重复的姓名（只在其中一个列表中出现）
        unique_names1 = names1 - names2  # 只在第一列出现
        unique_names2 = names2 - names1  # 只在第二列出现
        
        # 显示结果
        self.display_results(unique_names1, unique_names2)
        
        # 更新状态栏
        total_unique = len(unique_names1) + len(unique_names2)
        self.statusBar().showMessage(f'找到 {total_unique} 个不重复的姓名')
    
    def display_results(self, unique_names1, unique_names2):
        # 清空表格
        self.result_table.setRowCount(0)
        
        # 添加结果到表格
        row = 0
        # 添加只在第一列出现的姓名
        for name in sorted(unique_names1):
            self.result_table.insertRow(row)
            self.result_table.setItem(row, 0, QTableWidgetItem(name))
            self.result_table.setItem(row, 1, QTableWidgetItem("第一列"))
            self.result_table.setItem(row, 2, QTableWidgetItem("唯一"))
            row += 1
        
        # 添加只在第二列出现的姓名
        for name in sorted(unique_names2):
            self.result_table.insertRow(row)
            self.result_table.setItem(row, 0, QTableWidgetItem(name))
            self.result_table.setItem(row, 1, QTableWidgetItem("第二列"))
            self.result_table.setItem(row, 2, QTableWidgetItem("唯一"))
            row += 1
        
        # 调整列宽
        self.result_table.resizeColumnsToContents()
    
    def clear_all(self):
        self.col1_text.clear()
        self.col2_text.clear()
        self.result_table.setRowCount(0)
        self.statusBar().showMessage('已清空')


def main():
    app = QApplication(sys.argv)
    window = NameComparatorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()