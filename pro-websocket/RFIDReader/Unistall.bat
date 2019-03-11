

@echo off
rem 正在停止服务
net stop Srvany

@echo off  
rem 正在卸载
sc delete Srvany
pause  