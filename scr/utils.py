#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数文件 - 封装通用功能
"""

import sys
import ctypes
import tempfile
import shutil
import os
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox, QApplication


def is_admin():
    """检查是否以管理员身份运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"检查管理员权限时出错: {e}")
        return False


def run_as_admin():
    """尝试以管理员身份重新运行程序"""
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        return True
    except Exception as e:
        print(f"以管理员身份重新运行失败: {e}")
        return False


def create_temp_dir(prefix=""):
    """创建临时目录"""
    try:
        return tempfile.mkdtemp(prefix=prefix)
    except Exception as e:
        print(f"创建临时目录失败: {e}")
        return None


def cleanup_temp_dir(temp_dir):
    """清理临时目录"""
    if temp_dir and os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            return True
        except Exception as e:
            print(f"清理临时目录失败: {e}")
            return False
    return True


def show_message(parent, title, message, message_type='information', details=None, buttons=QMessageBox.Ok):
    """显示消息框，支持详细信息和自定义按钮"""
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(buttons)
    
    # 设置消息类型和图标
    if message_type == 'information':
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setInformativeText('操作已完成')
    elif message_type == 'warning':
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setInformativeText('请谨慎操作')
    elif message_type == 'critical':
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setInformativeText('操作失败')
    elif message_type == 'question':
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setInformativeText('请选择操作')
    elif message_type == 'info':  # 保持向后兼容
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setInformativeText('操作已完成')
    
    # 添加详细信息
    if details:
        msg_box.setDetailedText(details)
    
    return msg_box.exec_()


def show_confirmation(parent, title, message):
    """显示确认对话框"""
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg_box.setDefaultButton(QMessageBox.No)
    
    return msg_box.exec_() == QMessageBox.Yes


def safe_copy(source, destination):
    """安全复制文件"""
    try:
        shutil.copy2(source, destination)
        return True
    except PermissionError:
        raise PermissionError(f"无法复制文件: 权限不足\n源: {source}\n目标: {destination}")
    except FileNotFoundError:
        raise FileNotFoundError(f"无法复制文件: 文件不存在\n源: {source}")
    except Exception as e:
        raise Exception(f"复制文件时出错: {str(e)}")


def get_file_info(file_path):
    """获取文件信息"""
    try:
        from PIL import Image
        img = Image.open(file_path)
        return {
            "size": img.size,
            "format": img.format,
            "mode": img.mode
        }
    except Exception as e:
        raise Exception(f"获取文件信息失败: {str(e)}")


def format_file_size(size_in_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"


def clear_icon_cache():
    """清除图标缓存"""
    try:
        import subprocess
        subprocess.run(["ie4uinit.exe", "-show"], check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"清除图标缓存失败: {e}")
        return False
