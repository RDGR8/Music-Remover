:: Open folder dialog and get path, variable %location%, cd into it
set "psCommand="(new-object -COM 'Shell.Application').BrowseForFolder(0,'Please where you want to download Music Remover.',0x010,17).self.path""
for /f "usebackq delims=" %%I in (`powershell %psCommand%`) do set "location=%%I
cd %location%

curl -L "https://github.com/RDGR8/Music-Remover/archive/refs/tags/v0.0.0.zip" -o MusicRemoverSourceCode.zip
tar -xf MusicRemoverSourceCode.zip
del MusicRemoverSourceCode.zip
cd Music-Remover-0.0.0

:: Download embedded python 3.11.9
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
tar -xf tkinter.zip
del tkinter.zip
tar -xf ffmpeg.zip
del ffmpeg.zip
.\python Scripts\pip.exe install -r requirements.txt
.\python Scripts\pip.exe install audio-separator[cpu]==0.28.5 -t .\CPUseparator

:: Making shortcuts
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Start Menu\Programs\Music Remover.lnk');$s.TargetPath='%cd%\MR.vbs';$s.Arguments='connect';$s.IconLocation='%cd%\CustomTkinter_icon_Windows.ico';$s.WorkingDirectory='%cd%';$s.WindowStyle=7;$s.Save()"
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Desktop\Music Remover.lnk');$s.TargetPath='%cd%\MR.vbs';$s.Arguments='connect';$s.IconLocation='%cd%\CustomTkinter_icon_Windows.ico';$s.WorkingDirectory='%cd%';$s.WindowStyle=7;$s.Save()"
