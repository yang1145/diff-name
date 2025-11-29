import os
import sys
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
    QHBoxLayout, QLineEdit, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
import pandas as pd


class IDCardGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.background_image_path = "id_card.png"
        self.output_path = "generated_id_card.png"
        self.excel_data = None  # 存储从Excel导入的数据
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('工作证生成器')
        self.setGeometry(100, 100, 800, 500)

        # 创建主布局（水平布局）
        main_layout = QHBoxLayout()
        
        # 左侧控制面板
        control_panel = QVBoxLayout()
        
        # 背景图片选择
        bg_layout = QHBoxLayout()
        bg_label = QLabel('背景图片:')
        self.bg_path_edit = QLineEdit()
        self.bg_path_edit.setText("使用固定文件: id_card.png")
        self.bg_path_edit.setReadOnly(True)
        bg_layout.addWidget(bg_label)
        bg_layout.addWidget(self.bg_path_edit)
        
        # 照片选择
        photo_layout = QHBoxLayout()
        photo_label = QLabel('证件照片:')
        self.photo_path_edit = QLineEdit()
        self.photo_path_edit.setReadOnly(True)
        photo_button = QPushButton('选择照片')
        photo_button.clicked.connect(self.select_photo)
        photo_layout.addWidget(photo_label)
        photo_layout.addWidget(self.photo_path_edit)
        photo_layout.addWidget(photo_button)
        
        # 姓名输入
        name_layout = QHBoxLayout()
        name_label = QLabel('姓名:')
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        
        # 职位输入
        position_layout = QHBoxLayout()
        position_label = QLabel('职位:')
        self.position_edit = QLineEdit()
        position_layout.addWidget(position_label)
        position_layout.addWidget(self.position_edit)
        
        # 编号输入
        id_layout = QHBoxLayout()
        id_label = QLabel('编号:')
        self.id_edit = QLineEdit()
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.id_edit)
        
        # 输出文件名
        output_layout = QHBoxLayout()
        output_label = QLabel('输出文件:')
        self.output_edit = QLineEdit()
        self.output_edit.setText(self.output_path)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_edit)
        
        # Excel导入按钮
        excel_layout = QHBoxLayout()
        excel_label = QLabel('批量导入:')
        self.excel_path_edit = QLineEdit()
        self.excel_path_edit.setReadOnly(True)
        excel_button = QPushButton('选择Excel文件')
        excel_button.clicked.connect(self.select_excel)
        excel_layout.addWidget(excel_label)
        excel_layout.addWidget(self.excel_path_edit)
        excel_layout.addWidget(excel_button)
        
        # 批量生成按钮
        batch_generate_button = QPushButton('批量生成工作证')
        batch_generate_button.clicked.connect(self.batch_generate_id_cards)
        
        # 生成按钮
        generate_button = QPushButton('生成工作证')
        generate_button.clicked.connect(self.generate_id_card)
        
        # 添加控件到左侧控制面板
        control_panel.addLayout(bg_layout)
        control_panel.addLayout(photo_layout)
        control_panel.addLayout(name_layout)
        control_panel.addLayout(position_layout)
        control_panel.addLayout(id_layout)
        control_panel.addLayout(output_layout)
        control_panel.addLayout(excel_layout)
        control_panel.addWidget(batch_generate_button)
        control_panel.addWidget(generate_button)
        
        # 右侧预览区域
        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(4)
        self.preview_table.setHorizontalHeaderLabels(['姓名', '职位', '编号', '照片路径'])
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 将控制面板和预览区域添加到主布局
        main_layout.addLayout(control_panel, 1)
        main_layout.addWidget(self.preview_table, 1)
        
        self.setLayout(main_layout)

    def select_photo(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, '选择证件照片', '', 'Images (*.png *.jpg *.jpeg)')
        if file_name:
            self.photo_path = file_name
            self.photo_path_edit.setText(file_name)

    def select_excel(self):
        """选择Excel文件并加载数据"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, '选择Excel文件', '', 'Excel Files (*.xlsx *.xls)')
        if file_name:
            self.excel_path = file_name
            self.excel_path_edit.setText(file_name)
            self.load_excel_data(file_name)

    def load_excel_data(self, file_path):
        """加载Excel数据并在预览表中显示"""
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)
            
            # 检查必要的列是否存在
            required_columns = ['姓名', '职位', '编号']
            if not all(col in df.columns for col in required_columns):
                QMessageBox.warning(self, '错误', f'Excel文件必须包含列: {", ".join(required_columns)}')
                return
            
            # 保存数据
            self.excel_data = df
            
            # 更新预览表格
            self.update_preview_table(df)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'读取Excel文件时出错: {str(e)}')

    def update_preview_table(self, df):
        """更新预览表格"""
        self.preview_table.setRowCount(len(df))
        
        for row, (_, row_data) in enumerate(df.iterrows()):
            # 姓名
            name_item = QTableWidgetItem(str(row_data.get('姓名', '')))
            self.preview_table.setItem(row, 0, name_item)
            
            # 职位
            position_item = QTableWidgetItem(str(row_data.get('职位', '')))
            self.preview_table.setItem(row, 1, position_item)
            
            # 编号
            id_item = QTableWidgetItem(str(row_data.get('编号', '')))
            self.preview_table.setItem(row, 2, id_item)
            
            # 照片路径（如果有）
            photo_item = QTableWidgetItem(str(row_data.get('照片路径', '')))
            self.preview_table.setItem(row, 3, photo_item)

    def batch_generate_id_cards(self):
        """批量生成工作证"""
        if self.excel_data is None or len(self.excel_data) == 0:
            QMessageBox.warning(self, '错误', '请先导入Excel文件')
            return
            
        # 询问用户输出目录
        output_dir = QFileDialog.getExistingDirectory(self, '选择输出目录')
        if not output_dir:
            return
            
        success_count = 0
        failed_items = []
        
        try:
            for _, row_data in self.excel_data.iterrows():
                name = str(row_data.get('姓名', ''))
                position = str(row_data.get('职位', ''))
                employee_id = str(row_data.get('编号', ''))
                photo_path = str(row_data.get('照片路径', ''))
                
                # 如果没有照片路径，则使用默认空字符串
                if not photo_path or photo_path == 'nan':
                    photo_path = ''
                
                # 生成输出文件名
                output_file = os.path.join(output_dir, f"{name}_工作证.png")
                
                try:
                    self._generate_id_card_impl(
                        background_image_path=self.background_image_path,
                        photo_path=photo_path,
                        name=name,
                        position=position,
                        employee_id=employee_id,
                        output_path=output_file
                    )
                    success_count += 1
                except Exception as e:
                    failed_items.append(f"{name}: {str(e)}")
            
            # 显示结果
            message = f"批量生成完成!\n成功: {success_count} 个"
            if failed_items:
                message += f"\n失败: {len(failed_items)} 个"
                for item in failed_items[:5]:  # 只显示前5个错误
                    message += f"\n- {item}"
                if len(failed_items) > 5:
                    message += f"\n... 还有 {len(failed_items) - 5} 个错误"
                    
            QMessageBox.information(self, '批量生成结果', message)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'批量生成过程中出现错误: {str(e)}')

    def generate_id_card(self):
        # 获取输入值
        background_image = self.background_image_path
        photo_image = getattr(self, 'photo_path', '')
        name = self.name_edit.text()
        position = self.position_edit.text()
        employee_id = self.id_edit.text()
        output_file = self.output_edit.text()

        # 检查必要字段
        if not name:
            QMessageBox.warning(self, '错误', '请输入姓名')
            return

        try:
            self._generate_id_card_impl(
                background_image_path=background_image,
                photo_path=photo_image,
                name=name,
                position=position,
                employee_id=employee_id,
                output_path=output_file
            )
            QMessageBox.information(self, '成功', f'工作证已生成: {output_file}')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成工作证时出错: {str(e)}')

    def _generate_id_card_impl(
            self,
            background_image_path,
            photo_path,
            name,
            position,
            employee_id,
            output_path="generated_id_card.png"
    ):
        """
        生成工作证的核心实现
        
        :param background_image_path: 背景图片路径 (id_card.png)
        :param photo_path: 证件照路径
        :param name: 姓名
        :param position: 职位
        :param employee_id: 编号
        :param output_path: 输出文件路径
        """

        # 检查背景图片是否存在
        if not os.path.exists(background_image_path):
            raise FileNotFoundError(f"背景图片 {background_image_path} 不存在")

        # 打开背景图片
        background = Image.open(background_image_path)

        # 打开证件照
        if photo_path and os.path.exists(photo_path):
            photo = Image.open(photo_path)
            # 调整证件照大小为固定区域: 从(1750, 470)到(2050, 850)
            # 区域大小为 300x380
            photo = photo.resize((300, 380))

            # 将证件照粘贴到背景上指定位置 (1750, 470)
            background.paste(photo, (1750, 470))
        elif photo_path:
            print(f"警告: 照片 {photo_path} 未找到")

        # 创建绘图对象
        draw = ImageDraw.Draw(background)

        # 尝试加载阿里巴巴普惠体字体，如果失败则使用默认字体
        font_path = "AlibabaPuHuiTi.ttf"
        try:
            # 使用阿里巴巴普惠体字体，增大字体大小
            font_large = ImageFont.truetype(font_path, 60)
            font_medium = ImageFont.truetype(font_path, 40)
            font_small = ImageFont.truetype(font_path, 30)
        except IOError:
            # 尝试加载系统中文字体
            try:
                # Windows系统常用字体
                font_large = ImageFont.truetype("simhei.ttf", 60)
                font_medium = ImageFont.truetype("simhei.ttf", 40)
                font_small = ImageFont.truetype("simhei.ttf", 30)
            except IOError:
                try:
                    # 尝试其他常见中文字体
                    font_large = ImageFont.truetype("msyh.ttc", 60)
                    font_medium = ImageFont.truetype("msyh.ttc", 40)
                    font_small = ImageFont.truetype("msyh.ttc", 30)
                except IOError:
                    # 使用默认字体
                    font_large = ImageFont.load_default()
                    font_medium = ImageFont.load_default()
                    font_small = ImageFont.load_default()
                    print("警告: 无法加载中文字体，使用默认字体")

        # 添加文本信息到指定区域
        name_bbox = (1850, 1380, 2200, 1430)
        position_bbox = (1900, 1513, 2200, 1583)
        id_bbox = (1830, 1667, 2150, 1727)

        draw.text((name_bbox[0], name_bbox[1]), f"{name}", fill=(255, 255, 255), font=font_large)
        # 职位字体现在和姓名一样大
        draw.text((position_bbox[0], position_bbox[1]), f"{position}", fill=(255, 255, 255), font=font_large)
        draw.text((id_bbox[0], id_bbox[1]), f"{employee_id}", fill=(255, 255, 255), font=font_medium)

        # 保存结果
        background.save(output_path)
        print(f"工作证已生成: {output_path}")


def main():
    """
    主函数 - 启动GUI应用程序
    """
    app = QApplication(sys.argv)
    window = IDCardGeneratorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()