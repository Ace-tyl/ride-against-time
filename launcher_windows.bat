@echo off
chcp 936

py main.py
if ERRORLEVEL 1 (
	py -m pip install pygame
	if ERRORLEVEL 1 (
		echo ���д����������Ƿ�װ python 3��
		echo ��δ��װ�����ڴ����ز���װ python 3: https://www.python.org/downloads/release/python-3108
		echo �벻Ҫ��װ python 3.11 �����ϰ汾����Ϊ pygame ����Щ�汾���޷����С�
		pause
		exit
	)
	py -m pip install numpy
	py -m pip install numba
	py main.py
)
