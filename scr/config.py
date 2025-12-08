#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件 - 存储常量和配置信息
"""

import os
from pathlib import Path

# 系统配置
SYSTEM_ROOT = os.environ.get('SystemRoot', 'C:\\Windows')
SYSTEM32_PATH = os.path.join(SYSTEM_ROOT, 'System32')
TARGET_FILE = os.path.join(SYSTEM32_PATH, 'imageres.dll')
ICON_RESOURCE_ID = 84  # Windows启动图标资源ID

# 图标配置
TARGET_SIZES = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
DEFAULT_ICON_SIZE = (128, 128)

# 路径配置
DEFAULT_IMAGE_DIR = str(Path.home() / 'Pictures')
TEMP_DIR_PREFIX = 'icon_replacer_'

# UI配置
WINDOW_TITLE = 'Windows开机图标替换工具 - 管理员模式'
WINDOW_SIZE = (700, 600)
PREVIEW_SIZE = (150, 150)

# 消息配置
WARNING_MESSAGES = {
    'admin_required': '此程序需要管理员权限才能替换系统文件。',
    'backup_required': '请先创建系统还原点并确保有系统备份。',
    'system_file': '目标文件: C:\\Windows\\System32\\imageres.dll',
    'icon_info': '图标编号: 84 (Windows启动图标)'
}

# 文件过滤器
FILE_FILTERS = '图片文件 (*.png *.jpg *.jpeg *.bmp);;所有文件 (*.*)'

# 样式配置
STYLES = {
    'title': '''
        font-size: 28px; 
        font-weight: bold; 
        padding: 20px;
        color: #2c3e50;
        font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
    ''',
    'warning_box': '''
        QGroupBox {
            border: 2px solid #e74c3c;
            border-radius: 8px;
            background-color: #fef3f2;
            margin-top: 10px;
            padding: 5px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 10px;
            color: #e74c3c;
            font-weight: bold;
            font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
        }
    ''',
    'warning_text': '''
        color: #c0392b;
        font-weight: bold;
        padding: 10px;
        font-size: 14px;
        font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
        line-height: 1.5;
    ''',
    'group_box': '''
        QGroupBox {
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #f8f9fa;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 10px;
            color: #2c3e50;
            font-weight: bold;
            font-size: 16px;
        }
    ''',
    'button': '''
        QPushButton {
            background-color: #3498db;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            padding: 10px;
            font-size: 14px;
            border: none;
            font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
            min-height: 50px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #1f618d;
        }
        QPushButton:disabled {
            background-color: #cccccc;
        }
    ''',
    'replace_button': '''
        QPushButton {
            background-color: #27ae60;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
            border: none;
            font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
            min-height: 50px;
        }
        QPushButton:hover {
            background-color: #229954;
        }
        QPushButton:pressed {
            background-color: #1e8449;
        }
        QPushButton:disabled {
            background-color: #cccccc;
        }
    ''',
    'status_bar': '''
        padding: 12px;
        font-size: 12px;
        border-top: 1px solid #e0e0e0;
        margin-top: 15px;
        background-color: #f5f5f5;
        border-radius: 4px;
        font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
    ''',
    'preview_area': '''
        border: 2px solid #ddd;
        border-radius: 8px;
        background-color: #ffffff;
        padding: 10px;
    ''',
    'preview_label': '''
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #000;
        margin: 10px;
    ''',
    'progress_bar': '''
        QProgressBar {
            border: 2px solid #ddd;
            border-radius: 5px;
            text-align: center;
            background-color: #ffffff;
            height: 20px;
        }
        QProgressBar::chunk {
            background-color: #3498db;
            border-radius: 3px;
        }
    '''
}
