@echo off
echo 正在检查环境...
python -c "import sys; sys.exit(0 if all(map(lambda m: m in sys.modules or __import__(m, fromlist=['']) and True, ['PyQt5', 'sqlite3'])) else 1)" 2>nul
if %errorlevel% neq 0 (
    echo 正在安装必要的库...
    pip install pyqt5
)
echo 正在启动用户管理系统...
python main.py
pause