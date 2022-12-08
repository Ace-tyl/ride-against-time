@echo off
chcp 936

py main.py
if ERRORLEVEL 1 (
	py -m pip install pygame
	if ERRORLEVEL 1 (
		echo 运行错误！请检查你是否安装 python 3。
		echo 若未安装，请在此下载并安装 python 3: https://www.python.org/downloads/release/python-3108
		echo 请不要安装 python 3.11 及以上版本，因为 pygame 在这些版本下无法运行。
		pause
		exit
	)
	py -m pip install numpy
	py -m pip install numba
	py main.py
)
