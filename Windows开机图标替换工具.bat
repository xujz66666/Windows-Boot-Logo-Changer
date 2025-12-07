@echo off
setlocal

REM Windows开机图标替换工具启动脚本
cd /d "%~dp0"

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Python环境，请先安装Python 3.6及以上版本。
    pause
    exit /b 1
)

REM 检查是否在虚拟环境中，如果有则激活
if exist .venv\Scripts\activate.bat (
    echo 检测到虚拟环境，正在激活...
    call .venv\Scripts\activate.bat
)

REM 启动程序
echo 正在启动Windows开机图标替换工具...
python scr/main.py

REM 等待用户按任意键退出
pause
endlocal