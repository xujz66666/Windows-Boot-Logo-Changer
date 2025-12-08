#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI模块 - 分离界面和逻辑
"""

import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pathlib import Path

from config import *
from utils import *
from icon_processor import *
from system_ops import *


class SystemIconReplacer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.source_image_path = None
        self.temp_dir = create_temp_dir(TEMP_DIR_PREFIX)
        self.processed_ico_path = None
        self.processed_png_path = None
        
    def initUI(self):
        """初始化界面"""
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(300, 300, *WINDOW_SIZE)
        self.setMinimumSize(600, 500)
        
        # 设置应用图标
        if Path('icon.ico').exists():
            self.setWindowIcon(QIcon('icon.ico'))
        else:
            # 创建一个临时图标
            pixmap = QPixmap(100, 100)
            pixmap.fill(Qt.blue)
            painter = QPainter(pixmap)
            painter.setPen(Qt.white)
            painter.setFont(QFont("Arial", 50, QFont.Bold))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, "I")
            painter.end()
            self.setWindowIcon(QIcon(pixmap))
            
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel('Windows开机图标替换工具')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(STYLES['title'])
        layout.addWidget(title_label)
        
        # 警告框
        self.create_warning_box(layout)
        
        # 图片处理区域
        self.create_image_processing_area(layout)
        
        # 控制按钮
        self.create_control_buttons(layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(STYLES['progress_bar'])
        layout.addWidget(self.progress_bar)
        
        # 状态信息
        self.status_label = QLabel('就绪 - 请以管理员身份运行此程序')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(STYLES['status_bar'])
        layout.addWidget(self.status_label)
        
        # 加载默认图标预览
        self.load_default_icon()
        
        # 检查管理员权限
        if not is_admin():
            self.show_admin_warning()
            
    def create_warning_box(self, layout):
        """创建警告框"""
        warning_box = QGroupBox('⚠️ 重要警告')
        warning_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        warning_layout = QVBoxLayout()
        warning_layout.setSpacing(8)
        warning_layout.setContentsMargins(15, 10, 15, 10)
        
        warning_text = "\n".join([
            WARNING_MESSAGES['admin_required'],
            WARNING_MESSAGES['backup_required'],
            "操作前关闭所有重要程序",
            "可能需要重启电脑生效",
            "",
            WARNING_MESSAGES['system_file'],
            WARNING_MESSAGES['icon_info']
        ])
        
        warning_label = QLabel(warning_text)
        warning_label.setWordWrap(True)
        warning_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        warning_label.setStyleSheet(STYLES['warning_text'])
        warning_layout.addWidget(warning_label)
        
        warning_box.setLayout(warning_layout)
        warning_box.setStyleSheet(STYLES['warning_box'])
        layout.addWidget(warning_box, 0, Qt.AlignTop)
        
    def create_image_processing_area(self, layout):
        """创建图片处理区域"""
        image_group = QGroupBox('图标处理')
        image_group.setStyleSheet(STYLES['group_box'])
        image_layout = QHBoxLayout()
        image_layout.setSpacing(30)
        image_layout.setContentsMargins(20, 10, 20, 10)
        image_layout.setAlignment(Qt.AlignCenter)
        
        # 原始图标
        original_box = QGroupBox('原始Windows图标')
        original_box.setStyleSheet(STYLES['group_box'])
        original_layout = QVBoxLayout()
        original_layout.setAlignment(Qt.AlignCenter)
        original_layout.setSpacing(15)
        original_layout.setContentsMargins(15, 15, 15, 15)
        
        self.original_preview = QLabel()
        self.original_preview.setAlignment(Qt.AlignCenter)
        self.original_preview.setMinimumSize(*PREVIEW_SIZE)
        self.original_preview.setMaximumSize(*PREVIEW_SIZE)
        self.original_preview.setStyleSheet(STYLES['preview_label'])
        original_layout.addWidget(self.original_preview)
        
        # 显示图标信息
        self.original_info = QLabel(f"资源ID: {ICON_RESOURCE_ID}\n尺寸: {DEFAULT_ICON_SIZE[0]}x{DEFAULT_ICON_SIZE[1]}\n格式: ICO")
        self.original_info.setAlignment(Qt.AlignCenter)
        self.original_info.setStyleSheet('font-size: 12px; color: #666; font-weight: bold;')
        original_layout.addWidget(self.original_info)
        
        original_box.setLayout(original_layout)
        image_layout.addWidget(original_box)
        
        # 箭头
        arrow_label = QLabel('➔')
        arrow_label.setAlignment(Qt.AlignCenter)
        arrow_label.setStyleSheet('font-size: 36px; font-weight: bold; color: #3498db;')
        arrow_label.setMinimumWidth(60)
        arrow_label.setFixedHeight(PREVIEW_SIZE[1])  # 与预览图高度一致
        image_layout.addWidget(arrow_label)
        
        # 新图标
        new_box = QGroupBox('新图标')
        new_box.setStyleSheet(STYLES['group_box'])
        new_layout = QVBoxLayout()
        new_layout.setAlignment(Qt.AlignCenter)
        new_layout.setSpacing(15)
        new_layout.setContentsMargins(15, 15, 15, 15)
        
        self.new_preview = QLabel('点击下方按钮选择图片')
        self.new_preview.setAlignment(Qt.AlignCenter)
        self.new_preview.setMinimumSize(*PREVIEW_SIZE)
        self.new_preview.setMaximumSize(*PREVIEW_SIZE)
        self.new_preview.setStyleSheet(STYLES['preview_label'])
        self.new_preview.setWordWrap(True)
        new_layout.addWidget(self.new_preview)
        
        # 图标要求
        self.requirements = QLabel('要求: PNG格式\n尺寸: 建议256x256\n背景: 透明')
        self.requirements.setAlignment(Qt.AlignCenter)
        self.requirements.setStyleSheet('font-size: 12px; color: #666; font-weight: bold;')
        new_layout.addWidget(self.requirements)
        
        new_box.setLayout(new_layout)
        image_layout.addWidget(new_box)
        
        image_group.setLayout(image_layout)
        layout.addWidget(image_group)
        
    def create_control_buttons(self, layout):
        """创建控制按钮"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(20, 10, 20, 10)
        
        self.select_btn = QPushButton('选择图片')
        self.select_btn.setIcon(QIcon.fromTheme('document-open'))
        self.select_btn.clicked.connect(self.select_image)
        self.select_btn.setMinimumHeight(50)
        self.select_btn.setToolTip('选择要替换的图标图片')
        self.select_btn.setStyleSheet(STYLES['button'])
        
        self.preview_btn = QPushButton('预览效果')
        self.preview_btn.setIcon(QIcon.fromTheme('view-refresh'))
        self.preview_btn.clicked.connect(self.preview_effect)
        self.preview_btn.setMinimumHeight(50)
        self.preview_btn.setEnabled(False)
        self.preview_btn.setToolTip('预览替换后的效果')
        self.preview_btn.setStyleSheet(STYLES['button'])
        
        self.replace_btn = QPushButton('🔧 替换系统图标')
        self.replace_btn.setIcon(QIcon.fromTheme('system-run'))
        self.replace_btn.clicked.connect(self.replace_system_icon)
        self.replace_btn.setMinimumHeight(50)
        self.replace_btn.setEnabled(False)
        self.replace_btn.setToolTip('开始替换系统图标')
        self.replace_btn.setStyleSheet(STYLES['replace_button'])
        
        # 分配按钮宽度
        button_layout.addWidget(self.select_btn)
        button_layout.addWidget(self.preview_btn)
        button_layout.addWidget(self.replace_btn)
        button_layout.setStretch(0, 1)
        button_layout.setStretch(1, 1)
        button_layout.setStretch(2, 2)
        
        layout.addLayout(button_layout)
        
    def load_default_icon(self):
        """加载默认Windows图标预览（使用image文件夹中的图片）"""
        # 尝试从image文件夹加载图片
        image_path = os.path.join(os.path.dirname(__file__), '../image/OIP-C.jpg')
        
        if os.path.exists(image_path):
            # 加载图片并调整大小
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(*PREVIEW_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # 创建黑色背景
            final_pixmap = QPixmap(*PREVIEW_SIZE)
            final_pixmap.fill(Qt.black)
            
            # 在黑色背景上绘制缩放后的图片
            painter = QPainter(final_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            x = (PREVIEW_SIZE[0] - scaled_pixmap.width()) // 2
            y = (PREVIEW_SIZE[1] - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)
            painter.end()
            
            self.original_preview.setPixmap(final_pixmap)
        else:
            # 如果图片不存在，使用默认绘制
            pixmap = QPixmap(*PREVIEW_SIZE)
            pixmap.fill(Qt.black)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # 绘制Windows图标（四个蓝色方块）
            painter.setBrush(QColor(0, 120, 215))  # Windows蓝色
            painter.setPen(Qt.NoPen)
            
            # 四个方格
            square_size = 40
            padding = 20
            spacing = 8
            
            squares = [
                QRect(padding, padding, square_size, square_size),
                QRect(padding + square_size + spacing, padding, square_size, square_size),
                QRect(padding, padding + square_size + spacing, square_size, square_size),
                QRect(padding + square_size + spacing, padding + square_size + spacing, square_size, square_size)
            ]
            
            for square in squares:
                painter.drawRect(square)
            
            painter.end()
            self.original_preview.setPixmap(pixmap)
        
    def select_image(self):
        """选择图片文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择图标图片',
            DEFAULT_IMAGE_DIR,
            FILE_FILTERS
        )
        
        if file_path:
            if not check_image_validity(file_path):
                show_message(self, '图片无效', '选择的图片文件无效或损坏，请重新选择。', 'warning')
                return
                
            self.source_image_path = file_path
            
            # 显示预览
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(*PREVIEW_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.new_preview.setPixmap(scaled)
                self.preview_btn.setEnabled(True)
                self.replace_btn.setEnabled(True)
                
                # 显示图片信息
                try:
                    info = get_file_info(file_path)
                    info_text = f"尺寸: {info['size'][0]}x{info['size'][1]}\n格式: {info['format']}\n模式: {info['mode']}"
                    self.requirements.setText(info_text)
                    self.status_label.setText(f'已选择: {Path(file_path).name}')
                except Exception as e:
                    show_message(self, '信息获取失败', f'获取图片信息失败: {str(e)}', 'warning')
                    
    def preview_effect(self):
        """预览效果"""
        if not self.source_image_path:
            return
            
        # 创建预览对话框
        preview_dialog = QDialog(self)
        preview_dialog.setWindowTitle('预览启动效果')
        preview_dialog.setModal(True)
        preview_dialog.resize(450, 350)
        preview_dialog.setStyleSheet('background-color: #f8f9fa; border-radius: 10px;')
        
        layout = QVBoxLayout(preview_dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 模拟Windows启动界面
        preview_label = QLabel('Windows启动画面预览')
        preview_label.setAlignment(Qt.AlignCenter)
        preview_label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px; color: #2c3e50;')
        layout.addWidget(preview_label)
        
        # 创建黑色背景的预览
        preview_area = QLabel()
        preview_area.setAlignment(Qt.AlignCenter)
        preview_area.setMinimumSize(380, 220)
        preview_area.setStyleSheet('background-color: black; border: 3px solid #ddd; border-radius: 8px;')
        
        # 加载并处理图片
        source_pixmap = QPixmap(self.source_image_path)
        if not source_pixmap.isNull():
            # 创建圆形图标
            pixmap = QPixmap(120, 120)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # 设置圆形裁剪
            path = QPainterPath()
            path.addEllipse(0, 0, 120, 120)
            painter.setClipPath(path)
            
            # 绘制图片
            painter.drawPixmap(0, 0, 120, 120, source_pixmap.scaled(
                120, 120, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
            
            # 绘制圆圈
            painter.setClipping(False)
            painter.setPen(QPen(QColor(0, 120, 215), 4))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(1, 1, 118, 118)
            
            painter.end()
            
            preview_area.setPixmap(pixmap)
            
        layout.addWidget(preview_area)
        
        # 加载动画
        loading_label = QLabel('●')
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setStyleSheet('color: white; font-size: 24px;')
        layout.addWidget(loading_label)
        
        # 创建加载动画
        self.animation = QPropertyAnimation(loading_label, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.3)
        self.animation.setLoopCount(-1)
        self.animation.start()
        
        close_btn = QPushButton('关闭预览')
        close_btn.clicked.connect(preview_dialog.accept)
        close_btn.setMinimumHeight(35)
        close_btn.setStyleSheet(STYLES['button'])
        layout.addWidget(close_btn)
        
        preview_dialog.exec_()
        
    def replace_system_icon(self):
        """实际替换系统图标"""
        if not self.source_image_path:
            show_message(self, '错误', '请先选择图片', 'warning')
            return
            
        # 确认对话框
        if not show_confirmation(
            self, '⚠️ 最终确认',
            '您确定要替换系统图标吗？\n\n' +
            '此操作将修改系统文件，可能导致：\n\n' +
            '• 系统不稳定\n' +
            '• 某些功能异常\n' +
            '• 需要系统还原\n\n' +
            '强烈建议先创建系统还原点！'
        ):
            return
            
        try:
            self.progress_bar.setVisible(True)
            self.status_label.setText('正在处理图标...')
            QApplication.processEvents()
            
            # 处理图标
            self.progress_bar.setValue(20)
            self.processed_ico_path, self.processed_png_path = process_icon(self.source_image_path, self.temp_dir)
            
            self.progress_bar.setValue(40)
            self.status_label.setText('正在备份系统文件...')
            QApplication.processEvents()
            
            # 系统文件路径
            backup_file = os.path.join(self.temp_dir, 'imageres.dll.backup')
            backup_path = backup_system_file(TARGET_FILE, self.temp_dir)
            
            self.progress_bar.setValue(60)
            self.status_label.setText('正在创建替换脚本...')
            QApplication.processEvents()
            
            # 创建替换脚本
            script_path = create_replace_script(self.processed_ico_path, backup_path, TARGET_FILE, self.temp_dir)
            
            self.progress_bar.setValue(80)
            self.status_label.setText('正在准备替换说明...')
            QApplication.processEvents()
            
            # 显示完成信息
            self.show_completion_dialog(script_path, backup_path)
            
            self.progress_bar.setValue(100)
            self.status_label.setText('图标处理完成，请查看上方说明进行手动替换')
            
        except FileNotFoundError as e:
            show_message(
                self, '文件不存在', 
                '无法找到指定的文件', 
                'critical',
                details=str(e)
            )
            self.status_label.setText('文件不存在')
        except PermissionError as e:
            show_message(
                self, '权限不足', 
                '操作失败，请确保以管理员身份运行程序', 
                'critical',
                details=str(e)
            )
            self.status_label.setText('权限不足')
        except ValueError as e:
            show_message(
                self, '参数错误', 
                '输入参数有误', 
                'warning',
                details=str(e)
            )
            self.status_label.setText('参数错误')
        except Exception as e:
            show_message(
                self, '替换失败', 
                '替换过程中出错', 
                'critical',
                details=str(e)
            )
            self.status_label.setText('替换失败')
        finally:
            self.progress_bar.setVisible(False)
            
    def show_completion_dialog(self, script_path, backup_path):
        """显示完成对话框"""
        result_dialog = QDialog(self)
        result_dialog.setWindowTitle('替换完成')
        result_dialog.setModal(True)
        result_dialog.resize(550, 500)
        result_dialog.setStyleSheet('background-color: #f8f9fa; border-radius: 10px;')
        
        layout = QVBoxLayout(result_dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        info_label = QLabel('✅ 图标处理完成！')
        info_label.setStyleSheet('font-size: 20px; font-weight: bold; color: #27ae60; padding: 10px;')
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        # 显示下一步操作
        steps = QTextEdit()
        steps.setReadOnly(True)
        steps.setStyleSheet('''
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                background-color: #ffffff;
            }
        ''')
        steps.setPlainText(f'''
图标已处理完成，但需要手动完成以下步骤：

🔧 手动替换步骤：

1. 下载 Resource Hacker 工具
   https://www.angusj.com/resourcehacker/

2. 以管理员身份运行 Resource Hacker

3. 打开文件: {TARGET_FILE}

4. 定位到图标组: Icon Group -> {ICON_RESOURCE_ID} -> 1033

5. 删除现有图标

6. 从操作菜单中选择: "添加图标资源"
   选择文件: {self.processed_ico_path}

7. 保存为新的 DLL 文件

8. 清除图标缓存:
   a. 按 Win+R，输入: ie4uinit.exe -show
   b. 重启电脑

⚠️ 注意事项:
• 操作前务必创建系统还原点
• 替换失败可能导致系统异常
• 建议在虚拟机中测试

📁 生成的文件:
• 图标文件: {self.processed_ico_path}
• 备份文件: {backup_path}
• 替换脚本: {script_path}
''')
        layout.addWidget(steps)
        
        close_btn = QPushButton('关闭')
        close_btn.clicked.connect(result_dialog.accept)
        close_btn.setMinimumHeight(35)
        close_btn.setStyleSheet(STYLES['button'])
        layout.addWidget(close_btn)
        
        result_dialog.exec_()
        
    def show_admin_warning(self):
        """显示管理员权限警告"""
        show_message(
            self, '权限警告',
            '当前程序可能没有管理员权限！\n\n' +
            '替换系统图标需要管理员权限。\n\n' +
            '请关闭程序，然后：\n' +
            '1. 右键点击程序图标\n' +
            '2. 选择"以管理员身份运行"\n\n' +
            '否则可能无法替换系统文件。',
            'warning'
        )
        
    def closeEvent(self, event):
        """清理临时文件"""
        if self.temp_dir:
            cleanup_temp_dir(self.temp_dir)
        event.accept()
