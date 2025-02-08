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

set "version=0.0.1"

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
if not exist "%location%" (
	echo Folder does not exist or none was chosen
	pause
	exit()
cd %location%

echo App Setup

echo 	Downloading and extracting the app
curl -L "https://github.com/RDGR8/Music-Remover/archive/refs/tags/v%version%.zip" -o MusicRemoverSourceCode.zip
tar -xf MusicRemoverSourceCode.zip
del MusicRemoverSourceCode.zip
cd Music-Remover-%version%


:: extract and install some stuff needed for the program to work
echo 	Extracting ffmpeg
tar -xf ffmpeg.zip
del ffmpeg.zip

py -3.11 -m venv .venv
call .venv/Scripts/activate.bat

echo 	Installing dependencies 
pip install -r requirements.txt
pip install audio-separator[cpu]==0.28.5 onnx==1.16.1 -t .venv\CPUseparator
pip cache purge

call .venv/Scripts/deactivate.bat

:: Making shortcuts
echo Creating Start Menu shortcut
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Start Menu\Programs\Music Remover.lnk');$s.TargetPath='%cd%\MR.vbs';$s.Arguments='connect';$s.IconLocation='%cd%\icon.ico';$s.WorkingDirectory='%cd%';$s.WindowStyle=7;$s.Save()"
echo creating a Desktop shortcut
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Desktop\Music Remover.lnk');$s.TargetPath='%cd%\MR.vbs';$s.Arguments='connect';$s.IconLocation='%cd%\icon.ico';$s.WorkingDirectory='%cd%';$s.WindowStyle=7;$s.Save()"
echo Installation Finished
pause
