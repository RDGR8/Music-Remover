set "version=0.0.1"

:: Check if Visual C++ is installed
@echo off
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

if "%found%" == "false" (
	echo Please install Visual C++ and open the installer again
	echo Here is a link: https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170
	echo:
	echo Press any key to exit...
	pause >nul
	EXIT /B
)
endlocal

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
.\python Scripts\pip.exe install audio-separator[cpu]==0.28.5 onnx=1.16.1 numpy==2.1 -t .\CPUseparator

:: Making shortcuts
echo creating Start Menu shortcut
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Start Menu\Programs\Music Remover.lnk');$s.TargetPath='%cd%\MR.vbs';$s.Arguments='connect';$s.IconLocation='%cd%\CustomTkinter_icon_Windows.ico';$s.WorkingDirectory='%cd%';$s.WindowStyle=7;$s.Save()"
echo creating a Desktop shortcut
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Desktop\Music Remover.lnk');$s.TargetPath='%cd%\MR.vbs';$s.Arguments='connect';$s.IconLocation='%cd%\CustomTkinter_icon_Windows.ico';$s.WorkingDirectory='%cd%';$s.WindowStyle=7;$s.Save()"
