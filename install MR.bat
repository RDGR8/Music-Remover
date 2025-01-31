curl -LO "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
tar -xf python-3.11.9-embed-amd64.zip
del python-3.11.9-embed-amd64.zip
curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py
.\python get-pip.py
echo Lib >> python311._pth 
echo Lib/site-packages >> python311._pth
echo Scripts >> python311._pth
echo tcl >> python311._pth
tar -xf tkinter.zip
del tkinter.zip
.\python Scripts\pip.exe install -r requirements.txt
.\python Scripts\pip.exe install audio-separator[cpu]==0.28.5 -t .\CPUseparator
