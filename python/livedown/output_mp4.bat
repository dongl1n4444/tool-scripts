@echo off
rem use utf-8 encode
chcp 65001
setlocal enabledelayedexpansion  

set k1=%1
set k2=%2

for /f %%i in (.\tmp.dat) do (
	echo %%i
	echo %%i | findstr /c:".flv" && (
		echo !k1!
		set k1=%%i
	) || (
		echo !k2!
		set k2=%%i
	)
)

echo %k1%
echo %k2%

.\ffmpeg\bin\ffmpeg.exe -y -i %k1% -r 24 %k2%