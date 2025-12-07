#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统操作模块 - 封装文件系统和系统操作
"""

import os
import shutil
import subprocess
from config import TARGET_FILE, SYSTEM32_PATH


def backup_system_file(target_path, backup_dir):
    """备份系统文件"""
    try:
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"目标文件不存在: {target_path}")
        
        backup_filename = os.path.basename(target_path) + '.backup'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # 检查目标目录
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir, exist_ok=True)
        
        # 尝试复制文件
        shutil.copy2(target_path, backup_path)
        
        if not os.path.exists(backup_path):
            raise Exception("备份文件创建失败")
        
        return backup_path
        
    except PermissionError:
        raise PermissionError(
            "无法备份系统文件。请确保：\n" +
            "1. 以管理员身份运行此程序\n" +
            "2. 关闭所有资源管理器窗口\n" +
            "3. 暂时禁用杀毒软件\n" +
            "4. 关闭所有可能正在使用该文件的程序"
        )
    except FileNotFoundError as e:
        raise FileNotFoundError(f"系统文件不存在: {str(e)}")
    except IOError as e:
        raise IOError(f"文件读写错误: {str(e)}")
    except Exception as e:
        raise Exception(f"备份系统文件失败: {str(e)}")


def create_replace_script(icon_path, backup_path, target_path, output_dir):
    """创建替换脚本"""
    try:
        script_path = os.path.join(output_dir, 'replace_icon.bat')
        
        script_content = f'''
@echo off
echo Windows开机图标替换脚本
echo ===================================
echo.
echo 此脚本需要以管理员身份运行！
echo.

REM 取得文件所有权
echo 正在取得文件所有权...
takeown /f "{target_path}" >nul 2>&1
icacls "{target_path}" /grant Administrators:F >nul 2>&1

echo.
echo 正在备份原文件...
copy "{target_path}" "{backup_path}" /y >nul 2>&1

REM 注意：这里需要Resource Hacker工具
echo.
echo 请手动使用Resource Hacker替换图标：
echo 1. 下载并安装 Resource Hacker
echo 2. 以管理员身份运行 Resource Hacker
echo 3. 打开文件: {target_path}
echo 4. 定位到图标组: Icon Group -> 84 -> 1033
echo 5. 删除现有图标
echo 6. 添加新图标: {icon_path}
echo 7. 保存文件

echo.
echo 操作完成！可能需要重启电脑才能生效。
pause
'''
        
        with open(script_path, 'w', encoding='gbk') as f:
            f.write(script_content)
        
        return script_path
        
    except Exception as e:
        raise Exception(f"创建替换脚本失败: {str(e)}")


def check_file_access(file_path):
    """检查文件访问权限"""
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return False, "文件不存在"
        
        # 检查读权限
        with open(file_path, 'rb') as f:
            f.read(1)
        
        # 检查写权限
        if not os.access(file_path, os.W_OK):
            return False, "没有写权限"
        
        return True, ""
        
    except PermissionError:
        return False, "没有访问权限"
    except Exception as e:
        return False, str(e)


def get_system_info():
    """获取系统信息"""
    try:
        # 检查Windows版本
        import sys
        if sys.platform != 'win32':
            return "非Windows系统"
        
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
            product_name = winreg.QueryValueEx(key, "ProductName")[0]
            current_build = winreg.QueryValueEx(key, "CurrentBuild")[0]
            
        return f"Windows {product_name} (Build {current_build})"
        
    except Exception as e:
        return f"获取系统信息失败: {str(e)}"


def clear_icon_cache():
    """清除图标缓存"""
    try:
        # 使用ie4uinit.exe清除图标缓存
        subprocess.run(["ie4uinit.exe", "-show"], capture_output=True, check=True)
        return True
    except Exception as e:
        return False


def create_restore_point(description="图标替换前备份"):
    """创建系统还原点"""
    try:
        # 使用wmic创建系统还原点
        cmd = f"wmic.exe /Namespace:\\\\root\\default Path SystemRestore Call CreateRestorePoint \"{description}\", 100, 7"
        subprocess.run(cmd, shell=True, capture_output=True, check=True)
        return True
    except Exception as e:
        return False
