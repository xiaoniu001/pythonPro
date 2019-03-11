
@echo off
rem 正在复制动态链接库文件
copy "%~dp0pywintypes36.dll" "C:\Windows\System32\"
copy "%~dp0instsrv.exe" "C:\Windows\System32\"
copy "%~dp0srvany.exe" "C:\Windows\System32\"
copy "%~dp0instsrv.exe" "C:\Windows\SysWOW64\"
copy "%~dp0srvany.exe" "C:\Windows\SysWOW64\"

@echo off
rem 正在安装服务
instsrv Srvany C:\Windows\System32\srvany.exe
reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Srvany\Parameters\ /v AppDirectory /t REG_SZ /d "%~dp0\" /f

reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Srvany\Parameters\ /v Application /t REG_SZ /d "%~dp0run.exe" /f 

@echo off
net start Srvany
pause



