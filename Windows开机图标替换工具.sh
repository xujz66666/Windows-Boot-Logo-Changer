#!/bin/bash

# Windows开机图标替换工具启动脚本 (Linux)

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未检测到Python环境，请先安装Python 3.6及以上版本。"
    read -p "按Enter键退出..."
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查是否在虚拟环境中，如果有则激活
if [ -d ".venv/bin" ]; then
    echo "检测到虚拟环境，正在激活..."
    source .venv/bin/activate
fi

# 启动程序
echo "正在启动Windows开机图标替换工具..."
python3 scr/main.py

# 等待用户按任意键退出
read -p "按Enter键退出..."
