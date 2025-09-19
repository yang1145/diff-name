import sys
import os
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QSplitter, QGroupBox, QFileDialog, QMessageBox, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard


class FileNameNameExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('文件名姓名提取工具')
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
        input_group = QGroupBox("选择文件夹")
        input_layout = QVBoxLayout(input_group)

        # 文件夹选择按钮
        folder_layout = QHBoxLayout()
        self.folder_path_label = QLabel("未选择文件夹")
        self.select_folder_btn = QPushButton("选择文件夹")
        self.select_folder_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.folder_path_label)
        folder_layout.addWidget(self.select_folder_btn)
        input_layout.addLayout(folder_layout)

        # 过滤词输入
        filter_layout = QVBoxLayout()
        filter_layout.addWidget(QLabel("过滤词 (用逗号分隔):"))
        self.filter_words_input = QLineEdit()
        self.filter_words_input.setPlaceholderText("例如: report,data,info")
        filter_layout.addWidget(self.filter_words_input)
        input_layout.addLayout(filter_layout)

        # 文件列表显示
        file_list_layout = QVBoxLayout()
        file_list_layout.addWidget(QLabel("文件列表:"))
        self.file_list_text = QTextEdit()
        self.file_list_text.setReadOnly(True)
        file_list_layout.addWidget(self.file_list_text)
        input_layout.addLayout(file_list_layout)

        # 右侧结果区域
        result_group = QGroupBox("提取结果")
        result_layout = QVBoxLayout(result_group)

        # 结果表格
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["文件名", "提取的姓名", "状态"])
        result_layout.addWidget(self.result_table)

        # 添加到分隔器
        splitter.addWidget(input_group)
        splitter.addWidget(result_group)

        # 按钮区域
        button_layout = QHBoxLayout()
        self.extract_btn = QPushButton("提取姓名")
        self.extract_btn.clicked.connect(self.extract_names)
        self.extract_btn.setEnabled(False)
        self.copy_btn = QPushButton("复制所有姓名")
        self.copy_btn.clicked.connect(self.copy_all_names)
        self.copy_btn.setEnabled(False)
        self.clear_btn = QPushButton("清空")
        self.clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(self.extract_btn)
        button_layout.addWidget(self.copy_btn)
        button_layout.addWidget(self.clear_btn)
        main_layout.addLayout(button_layout)

        # 状态栏
        self.statusBar().showMessage('请选择文件夹')

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.folder_path_label.setText(folder_path)
            self.load_file_list(folder_path)
            self.extract_btn.setEnabled(True)
            self.statusBar().showMessage(f'已选择文件夹: {folder_path}')

    def load_file_list(self, folder_path):
        try:
            # 获取文件夹中的所有文件（不包括子文件夹中的文件和其他脚本）
            files = []
            for f in os.listdir(folder_path):
                file_path = os.path.join(folder_path, f)
                # 只添加文件，不添加目录和其他Python脚本
                if os.path.isfile(file_path) and not f.endswith('.py'):
                    files.append(f)

            # 显示文件列表
            self.file_list_text.setPlainText('\n'.join(files))
            self.statusBar().showMessage(f'找到 {len(files)} 个文件')
        except Exception as e:
            QMessageBox.critical(self, "错误", f"读取文件夹时出错: {str(e)}")

    def extract_names(self):
        folder_path = self.folder_path_label.text()
        if not os.path.exists(folder_path) or folder_path == "未选择文件夹":
            QMessageBox.warning(self, "警告", "请选择有效的文件夹！")
            return

        try:
            # 获取文件列表
            file_names = self.file_list_text.toPlainText().strip().split('\n')
            if not file_names or file_names == ['']:
                QMessageBox.warning(self, "警告", "文件夹中没有文件！")
                return

            # 提取姓名并显示结果
            self.extract_and_display_names(file_names)
            
            self.statusBar().showMessage(f'已完成从 {len(file_names)} 个文件名中提取姓名')
        except Exception as e:
            QMessageBox.critical(self, "错误", f"提取姓名时出错: {str(e)}")

    def get_filter_words(self):
        """
        获取过滤词列表
        """
        filter_text = self.filter_words_input.text().strip()
        if not filter_text:
            return []
        
        # 用逗号分隔过滤词，并清理空白字符
        filter_words = [word.strip() for word in filter_text.split(',') if word.strip()]
        return filter_words

    def extract_name_from_filename(self, filename):
        """
        从文件名中提取姓名
        支持多种格式，例如:
        - Zhang_San_Report.docx -> Zhang San
        - li_si_data.xlsx -> Li Si
        - wangwu.txt -> Wang Wu
        - Report_Zhao_Liu.pdf -> Zhao Liu
        """
        # 获取过滤词
        filter_words = self.get_filter_words()
        
        # 移除文件扩展名
        name_part = os.path.splitext(filename)[0]
        
        # 移除过滤词
        for filter_word in filter_words:
            # 不区分大小写的过滤词移除
            pattern = re.compile(re.escape(filter_word), re.IGNORECASE)
            name_part = pattern.sub('', name_part)
        
        # 清理多余的下划线和连字符
        name_part = re.sub(r'[_\-]+', '_', name_part)
        name_part = re.sub(r'^_+|_+$', '', name_part)  # 移除开头和结尾的下划线
        
        # 如果过滤后没有内容，返回空
        if not name_part:
            return ""
        
        # 尝试多种分割方式提取姓名
        # 1. 下划线分割
        if '_' in name_part:
            parts = name_part.split('_')
            # 尝试找到可能是姓名的部分
            for i, part in enumerate(parts):
                # 如果部分包含中文字符，可能是中文姓名
                if re.search(r'[\u4e00-\u9fff]+', part):
                    return part
                # 如果是英文，检查是否可能是英文姓名
                elif re.match(r'^[A-Za-z]+$', part):
                    # 如果下一个部分也是英文，可能是名和姓
                    if i + 1 < len(parts) and re.match(r'^[A-Za-z]+$', parts[i+1]):
                        return f"{part} {parts[i+1]}"
                    # 单个英文部分
                    return part.capitalize()
        
        # 2. 驼峰命名法 (如: zhangSanReport -> Zhang San)
        camel_parts = re.findall(r'[A-Z][a-z]*|[a-z]+', name_part)
        if len(camel_parts) >= 2:
            # 如果是英文姓名，格式化为标准形式
            name = ' '.join(camel_parts)
            return name.title()
        
        # 3. 全中文或全英文文件名
        # 中文姓名 (2-4个汉字)
        chinese_name = re.search(r'[\u4e00-\u9fff]{2,4}', name_part)
        if chinese_name:
            return chinese_name.group()
        
        # 英文姓名 (尝试识别常见的英文名格式)
        english_parts = re.findall(r'[A-Za-z]+', name_part)
        if english_parts:
            # 如果有2个或更多部分，可能是名和姓
            if len(english_parts) >= 2:
                return f"{english_parts[0].capitalize()} {english_parts[1].capitalize()}"
            else:
                return english_parts[0].capitalize()
        
        # 如果无法提取姓名，返回空字符串
        return ""

    def extract_and_display_names(self, file_names):
        # 清空表格
        self.result_table.setRowCount(0)

        # 添加结果到表格
        row = 0
        for filename in file_names:
            extracted_name = self.extract_name_from_filename(filename)
            
            self.result_table.insertRow(row)
            self.result_table.setItem(row, 0, QTableWidgetItem(filename))
            
            if extracted_name:
                self.result_table.setItem(row, 1, QTableWidgetItem(extracted_name))
                self.result_table.setItem(row, 2, QTableWidgetItem("成功"))
            else:
                self.result_table.setItem(row, 1, QTableWidgetItem("未找到姓名"))
                self.result_table.setItem(row, 2, QTableWidgetItem("失败"))
            row += 1

        # 调整列宽
        self.result_table.resizeColumnsToContents()
        
        # 启用复制按钮
        self.copy_btn.setEnabled(True)

    def copy_all_names(self):
        """
        一键复制所有提取出的姓名
        """
        names = []
        for row in range(self.result_table.rowCount()):
            name_item = self.result_table.item(row, 1)
            status_item = self.result_table.item(row, 2)
            
            # 只复制成功提取的姓名
            if name_item and status_item and status_item.text() == "成功":
                names.append(name_item.text())
        
        if names:
            # 将姓名列表合并为一列（每行一个姓名）
            names_text = '\n'.join(names)
            
            # 复制到剪贴板
            clipboard = QApplication.clipboard()
            clipboard.setText(names_text)
            
            self.statusBar().showMessage(f'已复制 {len(names)} 个姓名到剪贴板')
        else:
            self.statusBar().showMessage('没有可复制的姓名')

    def clear_all(self):
        self.folder_path_label.setText("未选择文件夹")
        self.filter_words_input.clear()
        self.file_list_text.clear()
        self.result_table.setRowCount(0)
        self.extract_btn.setEnabled(False)
        self.statusBar().showMessage('已清空')


def main():
    app = QApplication(sys.argv)
    window = FileNameNameExtractorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()