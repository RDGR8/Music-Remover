@echo off

:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"=""
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------


if exist "%temp%\consoleSettingsBackup.reg" regedit /S "%temp%\consoleSettingsBackup.reg" & DEL /F /Q "%temp%\consoleSettingsBackup.reg" & goto START
regedit /S /e "%temp%\consoleSettingsBackup.reg" "HKEY_CURRENT_USER\Console"
reg add "HKCU\Console" /v QuickEdit /t REG_DWORD /d 0 /f
start "" "cmd" /c ""%~dpnx0" & exit"
exit

: START

set "version=0.0.2"

:: Check if Visual C++ is installed
echo Checking if Visual C++ is installed
setlocal enabledelayedexpansion
set "found=false"
set "psCommand2="( Get-WmiObject -Class win32_product ^| Select-Object -Property Name )""

for /f "usebackq delims=" %%I in (`powershell %psCommand2%`) do (
    set programName=%%I
    IF "!programName:~0,20!" == "Microsoft Visual C++" (
        set "found=true"
    )
)

IF "%found%" == "false" (
	echo Visual C++ is not installed, downloading will begin
	curl -sSL "https://aka.ms/vs/17/release/vc_redist.x64.exe" -o "%temp%\vc_redist.x64.exe"
	echo starting install
	%temp%\VC_redist.x64.exe /quiet /norestart
	echo finished install


) ELSE echo 	Visual C++ is installed
endlocal




goto :CHECK_PYTHON

:CHECK_PYTHON
	echo Checking Python 3.11
	py -3.11 -V >nul 2>nul && (goto :PYTHON_311_FOUND)
s
	goto :PYTHON_311_NOT_FOUND


:PYTHON_311_NOT_FOUND
	echo 	Couldn't find Python 3.11
	echo 	Downloading Python 3.11 installer 
	curl -sSL "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe" -o "%temp%\python-3.11.9-amd64.exe"
	echo 	Installing Python 3.11
	%temp%\python-3.11.9-amd64.exe /silent PrependPath=1

:PYTHON_311_FOUND
	echo 	Python 3.11 is installed



:: Open folder dialog and get path, variable %location%, cd into it
set "psCommand="(new-object -COM 'Shell.Application').BrowseForFolder(0,'Please where you want to download Music Remover.',0x010,17).self.path""
for /f "usebackq delims=" %%I in (`powershell %psCommand%`) do set "location=%%I
cd %location%

echo Downloading and extracting the app
curl -L "https://github.com/RDGR8/Music-Remover/archive/refs/tags/v%version%.zip" -o MusicRemoverSourceCode.zip
tar -xf MusicRemoverSourceCode.zip
del MusicRemoverSourceCode.zip
cd Music-Remover-%version%

:: Download embedded python 3.11.9
echo Downloading embedded python
curl -LO "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
tar -xf python-3.11.9-embed-amd64.zip
del python-3.11.9-embed-amd64.zip

:: Download script to install python for embedded python
curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py
.\python get-pip.py
echo Lib >> python311._pth 
echo Lib/site-packages >> python311._pth
echo Scripts >> python311._pth
echo tcl >> python311._pth

:: extract and install some stuff needed for the program to work
echo extracting tkiner and ffmpeg
tar -xf tkinter.zip
del tkinter.zip
tar -xf ffmpeg.zip
del ffmpeg.zip
.\python Scripts\pip.exe install -r requirements.txt
.\python Scripts\pip.exe install audio-separator[cpu]==0.28.5 onnx==1.16.1 -t .\CPUseparator
.\python Scripts\pip.exe cache purge

:: Making shortcuts
echo creating Start Menu shortcut
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Start Menu\Programs\Music Remover.lnk');$s.TargetPath='%cd%\MR.vbs';$s.Arguments='connect';$s.IconLocation='%cd%\icon.ico';$s.WorkingDirectory='%cd%';$s.WindowStyle=7;$s.Save()"
echo creating a Desktop shortcut
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Desktop\Music Remover.lnk');$s.TargetPath='%cd%\MR.vbs';$s.Arguments='connect';$s.IconLocation='%cd%\icon.ico';$s.WorkingDirectory='%cd%';$s.WindowStyle=7;$s.Save()"
