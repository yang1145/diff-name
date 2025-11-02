#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
温馨提示框工具脚本
提供各种类型的提示框功能
"""

import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QDesktopWidget
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QPoint, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPainter, QPolygonF, QPen, QBrush, QPainterPath


# 温馨提示列表
warm_tips = [
    "想你了，记得照顾好自己哦~",
    "你的笑容是我最大的动力！",
    "愿你今天拥有美好的一天！",
    "无论多忙，记得喝水休息~",
    "想你了，今天也要元气满满哦~",
    "今天的你，比昨天更棒！",
    "每一个不曾起舞的日子，都是对生命的辜负。",
    "愿你被世界温柔以待。",
    "你的努力，终将成就更好的你！",
    "累了就休息一下，别太拼啦~",
    "想你了，记得按时吃饭~",
    "纵然黑夜漫长，黎明总会到来。",
    "你是最棒的，相信自己！",
    "生活很苦，但你很甜~",
    "想你了，愿你每天都有好心情~",
    "你的存在，让这个世界更加美好。",
    "愿你的每一天都充满阳光和欢笑。",
    "即使生活偶尔会下雨，但彩虹总会出现。",
    "你比你想象的更勇敢，比你看起来更坚强。",
    "每一次的努力都不会白费，每一份坚持都值得被尊重。",
    "愿你眼中有光，心中有爱，手中有温暖的咖啡。",
    "你的善良，是这世界最珍贵的宝藏。",
    "愿你在每一个平凡的日子里，都能发现不平凡的美好。",
    "你的微笑，是治愈一切的良药。",
    "无论走到哪里，都别忘了带上自己的阳光。",
    "愿你的生活如诗如画，每一天都是新的开始。",
    "你的每一个小进步，都值得被庆祝。",
    "愿你被温柔以待，也愿你温柔待人。",
    "在这个快节奏的世界里，别忘了偶尔停下来看看风景。",
    "你的独特，是这个世界独一无二的礼物。",
    "愿你的梦想都能照进现实，愿你的努力都有回报。",
    "即使是最小的星星，也能照亮一片夜空。",
    "愿你永远保持初心，永远热爱生活。",
    "你的坚强，是面对困难时最美的姿态。",
    "愿你拥有诗意的人生，和自由的灵魂。",
    "每一天都是一个新的机会，去成为更好的自己。",
    "你的温暖，可以融化最冰冷的心。",
    "愿你所到之处，都有鲜花为你盛开。",
    "你是独一无二的，你的价值无可替代。",
    "愿你的生活充满小确幸，每一个瞬间都值得珍藏。",
    "你的善良和真诚，是这个世界上最美的风景。",
    "愿你永远年轻，永远热泪盈眶。",
    "你的笑容，是这个世界最亮的那束光。",
    "愿你心中有梦，眼里有光，脚下有路。",
    "你的每一次尝试，都是向成功迈进的一步。",
    "愿你被这个世界深深爱着，也深深爱着这个世界。",
    "你的存在，本身就是一种奇迹。",
    "愿你的每一天都充满惊喜和感动。",
    "你的温柔，是这个世界上最强大的力量。",
    "愿你永远相信美好的事情即将发生。"
]


class HeartShapedTipWindow(QWidget):
    """
    心形排列的提示窗口（使用自定义QWidget而不是QMessageBox）
    """
    def __init__(self, message, x, y, color=None):
        super().__init__()
        self.color = color or QColor(255, 182, 193, 200)  # 默认浅粉色
        self.message = message
        self.init_ui(message)
        self.move(x, y)
        
    def init_ui(self, message):
        """
        初始化用户界面
        """
        # 设置窗口属性
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置窗口大小（增大窗口尺寸）
        self.setFixedSize(300, 150)
        
    def paintEvent(self, event):
        """
        绘制事件，用于绘制窗口背景和带发光效果的文字
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制圆角矩形背景
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 15, 15)
        painter.setClipPath(path)
        
        # 绘制半透明背景
        painter.setBrush(QBrush(self.color))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)
        
        # 绘制发光文字
        self.draw_glowing_text(painter)
        
    def draw_glowing_text(self, painter):
        """
        绘制带发光效果的文字
        """
        # 设置字体
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        
        # 文字发光效果 - 绘制多层渐变的阴影
        text_rect = self.rect().adjusted(10, 10, -10, -10)
        
        # 绘制发光层（多层不同透明度的相同文字形成发光效果）
        for i in range(10, 0, -1):
            # 计算透明度，越往外层透明度越低
            alpha = 50 - i * 4
            if alpha < 0:
                alpha = 0
                
            # 设置发光颜色
            glow_color = QColor(255, 255, 255, alpha)
            painter.setPen(QPen(glow_color, i, Qt.SolidLine))
            painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, self.message)
        
        # 绘制文字主体
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, self.message)
        
    def start_fade_out_animation(self, duration=1000):
        """
        开始淡出动画
        """
        # 创建位置动画（向右下角移动并逐渐透明）
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(duration)
        
        # 设置起始和结束位置
        start_pos = self.pos()
        end_pos = QPoint(start_pos.x() + 100, start_pos.y() + 100)
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        
        # 连接动画完成信号到关闭窗口
        self.animation.finished.connect(self.close)
        self.animation.start()
        
        # 同时改变透明度
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(duration)
        self.opacity_animation.setStartValue(1.0)
        self.opacity_animation.setEndValue(0.0)
        self.opacity_animation.start()
        
    def start_firework_animation(self, duration=1000):
        """
        开始烟花爆炸动画
        """
        # 随机生成爆炸方向
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(100, 300)
        
        # 计算终点位置
        start_pos = self.pos()
        end_pos = QPoint(
            start_pos.x() + int(distance * math.cos(angle)),
            start_pos.y() + int(distance * math.sin(angle))
        )
        
        # 创建位置动画
        self.position_animation = QPropertyAnimation(self, b"pos")
        self.position_animation.setDuration(duration)
        self.position_animation.setStartValue(start_pos)
        self.position_animation.setEndValue(end_pos)
        self.position_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # 创建透明度动画
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(duration)
        self.opacity_animation.setStartValue(1.0)
        self.opacity_animation.setEndValue(0.0)
        self.opacity_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # 并行动画
        self.position_animation.start()
        self.opacity_animation.start()
        
        # 动画结束后关闭窗口
        self.position_animation.finished.connect(self.close)


class Rotating3DHeart(QWidget):
    """
    3D旋转心形窗口
    """
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.init_ui()
        self.start_animation()
        
    def init_ui(self):
        """
        初始化用户界面
        """
        # 设置窗口属性
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置窗口大小（增大窗口尺寸）
        self.setFixedSize(500, 500)
        
        # 屏幕居中
        screen_geometry = QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
    def start_animation(self):
        """
        开始旋转动画
        """
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_heart)
        self.timer.start(30)  # 30毫秒更新一次，提高帧率
        
    def rotate_heart(self):
        """
        旋转心形
        """
        self.angle = (self.angle + 3) % 360
        self.update()
        
    def paintEvent(self, event):
        """
        绘制事件，绘制3D心形
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 移动坐标系到窗口中心
        painter.translate(self.width() / 2, self.height() / 2)
        
        # 应用旋转
        painter.rotate(self.angle)
        
        # 绘制3D效果的心形
        self.draw_3d_heart(painter)
        
    def draw_3d_heart(self, painter):
        """
        绘制3D心形
        """
        # 增大心形尺寸
        scale = 150
        
        # 绘制多层心形创建立体效果
        for i in range(10):
            # 每一层心形稍微偏移，创建深度感
            depth = 10 - i
            alpha = 255 - i * 20  # 逐渐变透明
            
            # 定义心形的点
            points = []
            
            # 生成心形点
            for j in range(100):
                t = j * 2 * math.pi / 100
                # 心形方程
                x = 16 * math.pow(math.sin(t), 3)
                y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
                
                # 缩放并添加到点列表
                points.append(QPoint(
                    int(x * scale / 16) + depth,
                    -int(y * scale / 13) + depth
                ))
            
            # 创建心形多边形
            heart_polygon = QPolygonF(points)
            
            # 绘制心形
            if i == 0:  # 最顶层的心形
                painter.setPen(QPen(QColor(255, 20, 147, alpha), 2))
                painter.setBrush(QBrush(QColor(255, 182, 193, alpha)))
            else:  # 其他层作为阴影
                painter.setPen(QPen(QColor(200 - i*10, 0, 50 + i*5, alpha), 1))
                painter.setBrush(QBrush(QColor(200 - i*10, 0, 50 + i*5, alpha//2)))
            
            painter.drawPolygon(heart_polygon)
        
        # 绘制高光效果
        highlight_points = []
        for i in range(50):
            t = i * math.pi / 50
            x = 16 * math.pow(math.sin(t), 3)
            y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
            highlight_points.append(QPoint(int(x * scale / 16), -int(y * scale / 13)))
        
        if highlight_points:
            highlight_polygon = QPolygonF(highlight_points)
            painter.setPen(QPen(QColor(255, 255, 255, 150), 1))
            painter.setBrush(QBrush(QColor(255, 255, 255, 100)))
            painter.drawPolygon(highlight_polygon)


def heart_shape_points(num_points, scale=100, x_offset=400, y_offset=300):
    """
    生成心形曲线上的点坐标
    
    Args:
        num_points (int): 点的数量
        scale (int): 缩放因子
        x_offset (int): x轴偏移量
        y_offset (int): y轴偏移量
    
    Returns:
        list: 包含(x, y)坐标的列表
    """
    points = []
    for i in range(num_points):
        # 心形方程参数
        t = i * 2 * math.pi / num_points
        
        # 心形方程: 
        # x = 16sin³(t)
        # y = 13cos(t) - 5cos(2t) - 2cos(3t) - cos(4t)
        x = 16 * math.pow(math.sin(t), 3)
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        
        # 缩放并调整坐标
        x = x * scale + x_offset
        y = -y * scale + y_offset  # y轴翻转，因为屏幕坐标系y轴向下
        
        points.append((int(x), int(y)))
    
    return points


def calculate_heart_scale_for_screen(screen_width, screen_height):
    """
    根据屏幕尺寸计算心形大小
    
    Args:
        screen_width (int): 屏幕宽度
        screen_height (int): 屏幕高度
    
    Returns:
        tuple: (scale, x_offset, y_offset) 心形缩放因子和偏移量
    """
    # 计算可用空间（考虑边距）
    margin_x = screen_width * 0.1  # 10% 边距
    margin_y = screen_height * 0.1  # 10% 边距
    
    available_width = screen_width - 2 * margin_x
    available_height = screen_height - 2 * margin_y
    
    # 心形方程的最大范围大约是 x: [-16, 16], y: [-15, 13]
    # 所以宽度大约是32个单位，高度大约是28个单位
    max_heart_width = 32
    max_heart_height = 28
    
    # 计算缩放因子，取宽高中的较小值以确保心形完整显示
    scale_x = available_width / max_heart_width
    scale_y = available_height / max_heart_height
    scale = min(scale_x, scale_y) * 0.8  # 再缩小一点以确保边距
    
    # 计算偏移量使心形居中
    x_offset = screen_width / 2
    y_offset = screen_height / 2
    
    return scale, x_offset, y_offset


def generate_random_color():
    """
    生成随机颜色
    """
    # 生成鲜艳的颜色，alpha值保持半透明
    red = random.randint(100, 255)
    green = random.randint(100, 255)
    blue = random.randint(100, 255)
    return QColor(red, green, blue, 200)


class HeartShapedTipsApp:
    """
    心形提示框应用类
    """
    def __init__(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        
        # 获取屏幕尺寸
        screen_geometry = QDesktopWidget().screenGeometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()
        
        # 根据屏幕尺寸计算心形参数
        scale, x_offset, y_offset = calculate_heart_scale_for_screen(self.screen_width, self.screen_height)
        
        # 生成心形坐标点
        self.points = heart_shape_points(50, scale=scale, x_offset=x_offset, y_offset=y_offset)
        self.tip_windows = []
        self.current_index = 0
        self.is_dispersion_phase = False  # 是否处于消散阶段
        self.heart_3d_window = None  # 3D心形窗口
        
    def show_next_tip(self):
        """
        显示下一个提示框
        """
        if not self.is_dispersion_phase and self.current_index < len(self.points):
            x, y = self.points[self.current_index]
            tip = random.choice(warm_tips)
            # 心形阶段使用粉色
            color = QColor(255, 182, 193, 200)
            tip_window = HeartShapedTipWindow(tip, x, y, color)
            self.tip_windows.append(tip_window)
            tip_window.show()
            
            self.current_index += 1
            
            # 如果还有更多提示框需要显示，安排下一次显示
            if self.current_index < len(self.points):
                QTimer.singleShot(500, self.show_next_tip)  # 0.5秒后显示下一个
            else:
                # 所有心形窗口都已显示，1秒后开始消散动画
                QTimer.singleShot(1000, self.start_dispersion)
    
    def start_dispersion(self):
        """
        开始消散动画
        """
        self.is_dispersion_phase = True
        
        # 对所有窗口执行消散动画
        for i, window in enumerate(self.tip_windows):
            # 延迟执行每个窗口的消散动画
            QTimer.singleShot(i * 20, lambda w=window: w.start_fade_out_animation(800))
        
        # 所有窗口消散后，开始随机显示新窗口
        QTimer.singleShot(len(self.tip_windows) * 20 + 1000, self.show_random_tips)
    
    def show_random_tips(self):
        """
        随机显示新窗口
        """
        self.tip_windows = []  # 清空旧窗口列表
        self.current_index = 0
        
        # 显示150个随机位置的窗口
        self.show_next_random_tip()
        
        # 确保应用不会退出
        self.app.setQuitOnLastWindowClosed(False)
    
    def show_next_random_tip(self):
        """
        显示下一个随机位置的提示框
        """
        if self.current_index < 150:
            # 生成随机位置（避免超出屏幕边界）
            x = random.randint(50, self.screen_width - 250)
            y = random.randint(50, self.screen_height - 150)
            
            tip = random.choice(warm_tips)
            # 随机颜色
            color = generate_random_color()
            tip_window = HeartShapedTipWindow(tip, x, y, color)
            self.tip_windows.append(tip_window)
            tip_window.show()
            
            self.current_index += 1
            
            # 如果还有更多提示框需要显示，安排下一次显示
            if self.current_index < 150:
                QTimer.singleShot(200, self.show_next_random_tip)  # 0.2秒后显示下一个
            else:
                # 所有窗口都已显示，2秒后开始烟花消散
                QTimer.singleShot(2000, self.firework_dispersion)
    
    def firework_dispersion(self):
        """
        烟花爆炸形式的消散动画
        """
        # 对所有窗口执行烟花动画
        for i, window in enumerate(self.tip_windows):
            # 延迟执行每个窗口的烟花动画
            QTimer.singleShot(i * 10, lambda w=window: w.start_firework_animation(1000))
        
        # 所有窗口消散后显示3D心形
        QTimer.singleShot(len(self.tip_windows) * 10 + 2000, self.show_3d_heart)
    
    def show_3d_heart(self):
        """
        显示3D旋转心形
        """
        self.heart_3d_window = Rotating3DHeart()
        self.heart_3d_window.show()
        
        # 5秒后退出程序
        QTimer.singleShot(5000, self.app.quit)
    
    def run(self):
        """
        运行应用
        """
        # 设置应用不因最后一个窗口关闭而退出
        self.app.setQuitOnLastWindowClosed(False)
        
        # 显示第一个提示框
        self.show_next_tip()
        # 运行事件循环
        return self.app.exec_()


def show_heart_shaped_tips():
    """
    显示心形排列的提示框，每个窗口间隔0.5秒显示
    """
    app = HeartShapedTipsApp()
    return app.run()


def show_random_tip():
    """
    随机显示一条温馨提示
    """
    qapp = QApplication.instance()
    if qapp is None:
        qapp = QApplication(sys.argv)
    
    # 设置应用不因最后一个窗口关闭而退出
    qapp.setQuitOnLastWindowClosed(False)
    
    # 随机选择一个提示
    tip = random.choice(warm_tips)
    
    # 创建自定义窗口
    tip_window = HeartShapedTipWindow(tip, 100, 100)
    
    # 显示窗口
    tip_window.show()
    
    # 运行事件循环
    return qapp.exec_()


def main():
    """主函数"""
    show_heart_shaped_tips()


if __name__ == '__main__':
    main()