#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主入口文件 - 整合所有模块
"""

import sys
import warnings
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

# 导入自定义模块
from gui import SystemIconReplacer
from utils import is_admin, run_as_admin, show_message

# 忽略警告
warnings.filterwarnings('ignore')

def main():
    """主函数"""
    # 创建应用程序
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # 检查权限
    if not is_admin():
        ret = show_message(
            None, '权限警告',
            '此程序需要管理员权限才能替换系统文件。\n\n是否继续运行？',
            'question'
        )
        
        if ret == QMessageBox.No:
            sys.exit(1)
        
        # 尝试以管理员身份重新运行
        if run_as_admin():
            sys.exit(0)
    
    try:
        # 创建主窗口
        window = SystemIconReplacer()
        window.show()
        
        # 运行应用程序
        sys.exit(app.exec_())
    except Exception as e:
        # 捕获全局异常
        print(f"程序运行错误: {str(e)}")
        show_message(
            None, '程序错误',
            f'程序运行时发生错误:\n{str(e)}\n\n请联系开发者或检查日志文件。',
            'critical'
        )
        sys.exit(1)

if __name__ == '__main__':
    main()
