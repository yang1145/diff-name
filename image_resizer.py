#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图片批量调整工具
支持批量设置图片为固定大小、压缩率、格式转换和强制拉伸
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QFileDialog,
    QSpinBox, QComboBox, QCheckBox, QTextEdit, QVBoxLayout, QHBoxLayout,
    QGroupBox, QProgressBar, QMessageBox, QLineEdit, QGridLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PIL import Image


class ImageProcessor(QThread):
    """图片处理线程类"""
    progress_updated = pyqtSignal(int)  # 进度更新信号
    log_message = pyqtSignal(str)       # 日志消息信号
    processing_finished = pyqtSignal()  # 处理完成信号

    def __init__(self, image_files, output_dir, width, height, quality, format_ext, force_stretch):
        super().__init__()
        self.image_files = image_files
        self.output_dir = output_dir
        self.width = width
        self.height = height
        self.quality = quality
        self.format_ext = format_ext
        self.force_stretch = force_stretch

    def run(self):
        """执行图片处理任务"""
        total_files = len(self.image_files)
        for i, image_path in enumerate(self.image_files):
            try:
                # 更新进度
                progress = int((i / total_files) * 100)
                self.progress_updated.emit(progress)
                
                # 打开图片
                with Image.open(image_path) as img:
                    # 转换为RGB模式（某些格式如PNG有透明通道）
                    if self.format_ext.lower() in ['jpg', 'jpeg']:
                        img = img.convert('RGB')
                    
                    # 调整图片大小
                    if self.force_stretch:
                        # 强制拉伸到指定尺寸
                        resized_img = img.resize((self.width, self.height), Image.LANCZOS)
                    else:
                        # 保持纵横比并填充到指定尺寸
                        img.thumbnail((self.width, self.height), Image.LANCZOS)
                        resized_img = Image.new('RGB', (self.width, self.height), (255, 255, 255))
                        x = (self.width - img.width) // 2
                        y = (self.height - img.height) // 2
                        resized_img.paste(img, (x, y))
                    
                    # 构造输出文件路径
                    output_filename = f"{Path(image_path).stem}.{self.format_ext}"
                    output_path = Path(self.output_dir) / output_filename
                    
                    # 保存图片
                    if self.format_ext.lower() in ['jpg', 'jpeg']:
                        resized_img.save(str(output_path), 'JPEG', quality=self.quality)
                    elif self.format_ext.lower() == 'png':
                        resized_img.save(str(output_path), 'PNG', compress_level=int((100-self.quality)/10))
                    else:
                        resized_img.save(str(output_path))
                    
                    self.log_message.emit(f"已处理: {image_path}")
            
            except Exception as e:
                self.log_message.emit(f"处理 {image_path} 时出错: {str(e)}")
        
        # 完成处理
        self.progress_updated.emit(100)
        self.log_message.emit(f"处理完成！共处理 {total_files} 个文件")
        self.processing_finished.emit()


class ImageResizerApp(QMainWindow):
    """主应用程序窗口"""
    
    def __init__(self):
        super().__init__()
        self.image_files = []  # 待处理的图片文件列表
        self.output_dir = ""   # 输出目录
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('图片批量调整工具')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 输入区域
        input_group = QGroupBox("输入设置")
        input_layout = QVBoxLayout()
        
        # 图片选择按钮和显示
        file_select_layout = QHBoxLayout()
        self.select_files_btn = QPushButton("选择图片文件")
        self.select_files_btn.clicked.connect(self.select_images)
        self.files_count_label = QLabel("未选择文件")
        file_select_layout.addWidget(self.select_files_btn)
        file_select_layout.addWidget(self.files_count_label)
        file_select_layout.addStretch()
        
        input_layout.addLayout(file_select_layout)
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # 输出设置区域
        output_group = QGroupBox("输出设置")
        output_layout = QGridLayout()
        
        # 输出目录设置
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setPlaceholderText("请选择输出目录")
        self.select_output_dir_btn = QPushButton("选择输出目录")
        self.select_output_dir_btn.clicked.connect(self.select_output_directory)
        output_layout.addWidget(QLabel("输出目录:"), 0, 0)
        output_layout.addWidget(self.output_dir_edit, 0, 1)
        output_layout.addWidget(self.select_output_dir_btn, 0, 2)
        
        # 图片尺寸设置
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 10000)
        self.width_spinbox.setValue(800)
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(1, 10000)
        self.height_spinbox.setValue(600)
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("宽度:"))
        size_layout.addWidget(self.width_spinbox)
        size_layout.addWidget(QLabel("高度:"))
        size_layout.addWidget(self.height_spinbox)
        output_layout.addLayout(size_layout, 1, 0, 1, 3)
        
        # 格式设置
        self.format_combo = QComboBox()
        self.format_combo.addItems(['jpg', 'png'])
        output_layout.addWidget(QLabel("输出格式:"), 2, 0)
        output_layout.addWidget(self.format_combo, 2, 1, 1, 2)
        
        # 压缩质量设置
        self.quality_spinbox = QSpinBox()
        self.quality_spinbox.setRange(1, 100)
        self.quality_spinbox.setValue(85)
        output_layout.addWidget(QLabel("压缩质量:"), 3, 0)
        output_layout.addWidget(self.quality_spinbox, 3, 1, 1, 2)
        
        # 强制拉伸选项
        self.stretch_checkbox = QCheckBox("强制拉伸到指定尺寸（否则保持比例并居中）")
        self.stretch_checkbox.setChecked(True)
        output_layout.addWidget(self.stretch_checkbox, 4, 0, 1, 3)
        
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)
        
        # 控制按钮区域
        control_layout = QHBoxLayout()
        self.start_process_btn = QPushButton("开始处理")
        self.start_process_btn.clicked.connect(self.start_processing)
        self.start_process_btn.setEnabled(False)
        control_layout.addWidget(self.start_process_btn)
        control_layout.addStretch()
        main_layout.addLayout(control_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        # 日志显示区域
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(self.log_text)
        
        # 状态栏
        self.statusBar().showMessage("就绪")
    
    def select_images(self):
        """选择图片文件"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, 
            "选择图片文件", 
            "", 
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"
        )
        
        if file_paths:
            self.image_files = file_paths
            self.files_count_label.setText(f"已选择 {len(file_paths)} 个文件")
            self.log_text.append(f"选择了 {len(file_paths)} 个图片文件")
            self.check_start_enable()
    
    def select_output_directory(self):
        """选择输出目录"""
        directory = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if directory:
            self.output_dir = directory
            self.output_dir_edit.setText(directory)
            self.check_start_enable()
    
    def check_start_enable(self):
        """检查是否可以开始处理"""
        can_start = len(self.image_files) > 0 and bool(self.output_dir)
        self.start_process_btn.setEnabled(can_start)
    
    def start_processing(self):
        """开始处理图片"""
        if not self.image_files:
            QMessageBox.warning(self, "警告", "请先选择图片文件")
            return
        
        if not self.output_dir:
            QMessageBox.warning(self, "警告", "请先选择输出目录")
            return
        
        # 禁用相关控件
        self.select_files_btn.setEnabled(False)
        self.select_output_dir_btn.setEnabled(False)
        self.start_process_btn.setEnabled(False)
        self.width_spinbox.setEnabled(False)
        self.height_spinbox.setEnabled(False)
        self.format_combo.setEnabled(False)
        self.quality_spinbox.setEnabled(False)
        self.stretch_checkbox.setEnabled(False)
        
        # 创建并启动处理线程
        self.processor = ImageProcessor(
            self.image_files,
            self.output_dir,
            self.width_spinbox.value(),
            self.height_spinbox.value(),
            self.quality_spinbox.value(),
            self.format_combo.currentText(),
            self.stretch_checkbox.isChecked()
        )
        
        # 连接信号
        self.processor.progress_updated.connect(self.update_progress)
        self.processor.log_message.connect(self.add_log)
        self.processor.processing_finished.connect(self.processing_finished)
        
        # 开始处理
        self.statusBar().showMessage("正在处理图片...")
        self.processor.start()
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def add_log(self, message):
        """添加日志消息"""
        self.log_text.append(message)
    
    def processing_finished(self):
        """处理完成回调"""
        # 启用相关控件
        self.select_files_btn.setEnabled(True)
        self.select_output_dir_btn.setEnabled(True)
        self.start_process_btn.setEnabled(True)
        self.width_spinbox.setEnabled(True)
        self.height_spinbox.setEnabled(True)
        self.format_combo.setEnabled(True)
        self.quality_spinbox.setEnabled(True)
        self.stretch_checkbox.setEnabled(True)
        
        # 更新状态
        self.statusBar().showMessage("处理完成")
        QMessageBox.information(self, "完成", "图片处理已完成！")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = ImageResizerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()