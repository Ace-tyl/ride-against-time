@echo off

py main.py
if ERRORLEVEL 1 (
	py -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pygame
	if ERRORLEVEL 1 (
		echo Error! Please check whether you have installed Python 3.
		echo If not, please download Python 3 from https://www.python.org/downloads/release/python-3108 and install.
		echo Please don't install Python 3.11, because Pygame is not compatible with this version.
		pause
		exit
	)
	py -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy
	py -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numba
	py main.py
)
