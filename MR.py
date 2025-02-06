# https://pytorch.org/get-started/previous-versions/
# https://pypi.org/project/audio-separator/
import os.path
import tkinter.messagebox
import os
import ffmpeg
import sys

with open('mode.txt', 'r') as f:
    mode = f.read()
# Dynamically insert the path based on the mode
sys.path.insert(1, f'./{mode}separator/')
from audio_separator import separator
import customtkinter
from tkinter import filedialog
from tkinter import *
from threading import Thread
import tempfile
import logging
import webbrowser
import subprocess
from io import StringIO

from sympy.abc import lamda



temp_dir = tempfile.TemporaryDirectory()





class StdoutRedirector(object):

    def __init__(self, text_area):
        self.text_area = text_area

    def write(self, str):
        try:
            if(rf'{str[0]}' == '\r'):
                self.text_area.delete("end-1l", "end")
                self.text_area.insert(END, '\n')
        except:
            pass
        self.text_area.insert(END, str)
        self.text_area.see(END)

    def flush(self):
        pass


customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

enableOpenGPUWindow = True
GPUWindowEnableClosing = True
root = customtkinter.CTk()
root.geometry(f"{1000}x{600}+{int((root.winfo_screenwidth() - 1000) / 2)}+{int((root.winfo_screenheight() - 600) / 2)}")

root.resizable(0, 0)
root.title('Music Remover')
root.iconbitmap("icon.ico")
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=False)

separatorInitialized = False

def removeMusic(videoFile, outputLocation):
    global enableOpenGPUWindow
    global separatorInitialized
    global Separator
    enableOpenGPUWindow = False
    # Intialize the separator

    if(not separatorInitialized):
        Separator = separator.Separator(output_single_stem='Vocals', output_dir=temp_dir.name,
                                        log_formatter=logging.Formatter('%(message)s'))

        Separator.load_model('UVR-MDX-NET-Inst_HQ_3.onnx')
        separatorInitialized = True

    # Process audio
    output_files = Separator.separate(videoFile)

    # originalVideoName_withoutmusic.originalExtension
    fileName = fr"{os.path.splitext(os.path.basename(videoFile))[0]}_withoutmusic{os.path.splitext(os.path.basename(videoFile))[1]}"

    # outputlocation/fileName
    output = os.path.join(outputLocation, fileName)  # Replace with your desired output file

    # Inputting video and audio
    video_stream = ffmpeg.input(videoFile)
    audio_stream = ffmpeg.input(os.path.join(temp_dir.name, output_files[0]))

    print("Combining audio and video")
    (
        ffmpeg
        .output(video_stream['v'], audio_stream['a'], output, vcodec='copy')
        .global_args('-loglevel', 'quiet')
        .run(overwrite_output=True)
    )
    print("Done")
    enableOpenGPUWindow = True


def browse_button_output():
    guiOutputLocation.delete(0, END)
    guiOutputLocation.insert(0, filedialog.askdirectory())


def browse_button_input():
    # Allow user to select a directory and store it in global var
    # called folder_path
    guiVideoInput.delete(0, END)
    guiVideoInput.insert(0, filedialog.askopenfilename())


def installGPULibraries(textBox, window):
    global msg
    global GPUWindowEnableClosing
    GPUWindowEnableClosing = False


    p = subprocess.Popen(
        ".\python.exe Scripts\pip.exe install onnx==1.16.1 -t .\\GPUseparator".split(),
        stdout=subprocess.PIPE, bufsize=1, text=True)
    while p.poll() is None:
        msg = p.stdout.readline().strip()  # read a line from the process output
        if msg:
            window.event_generate("<<Foo>>", when="tail")

    p = subprocess.Popen(
        ".\python.exe Scripts\pip.exe install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu124 -t .\\GPUseparator".split(),
        stdout=subprocess.PIPE, bufsize=1, text=True)
    while p.poll() is None:
        msg = p.stdout.readline().strip()  # read a line from the process output
        if msg:
            window.event_generate("<<Foo>>", when="tail")

    p = subprocess.Popen(
        ".\python.exe Scripts\pip.exe install numpy==2.1.2 --upgrade --index-url https://download.pytorch.org/whl/cu124 -t .\\GPUseparator".split(),
        stdout=subprocess.PIPE, bufsize=1, text=True)
    while p.poll() is None:
        msg = p.stdout.readline().strip()  # read a line from the process output
        if msg:
            window.event_generate("<<Foo>>", when="tail")

    p = subprocess.Popen(".\python.exe Scripts\pip.exe install audio-separator[gpu]==0.28.5 -t .\\GPUseparator".split()
                         ,stdout=subprocess.PIPE, bufsize=1, text=True)
    while p.poll() is None:
        msg = p.stdout.readline().strip()  # read a line from the process output
        if msg:
            window.event_generate("<<Foo>>", when="tail")

    p = subprocess.Popen(".\python.exe Scripts\pip.exe cache purge".split()
                         ,stdout=subprocess.PIPE, bufsize=1, text=True)
    while p.poll() is None:
        msg = p.stdout.readline().strip()  # read a line from the process output
        if msg:
            window.event_generate("<<Foo>>", when="tail")

    with open('mode.txt', 'w') as f:
        f.write('GPU')


    GPUWindowEnableClosing = True

def insertTextBox(textBox):
    textBox.insert(END, f"{msg}\n")
    textBox.see('end')


def closingGPUWindow(window, textBox):
    if (GPUWindowEnableClosing):
        window.destroy()
    else:
        tkinter.messagebox.showerror('ERROR', "Please wait for the current process to finish")




label = customtkinter.CTkLabel(master=frame, text="Music Remover", font=("Arial", 24))
label.pack(pady=20, padx=10)

guiVideoInput = customtkinter.CTkEntry(master=frame, width=300, placeholder_text="Video Location")
guiVideoInput.pack(pady=5, padx=10)

guiVideoInputButton = customtkinter.CTkButton(master=frame, height=30, text="Select Video Location",
                                              command=browse_button_input)
guiVideoInputButton.pack(pady=5, padx=0)

guiOutputLocation = customtkinter.CTkEntry(master=frame, width=300, placeholder_text="Output Location")
guiOutputLocation.pack(pady=12, padx=10)

guiOutputLocationButton = customtkinter.CTkButton(master=frame, height=30, text="Select Output Location",
                                                  command=browse_button_output)
guiOutputLocationButton.pack(pady=5, padx=0)


def guiStart():
    t = Thread(target=removeMusic, args=(str(guiVideoInput.get()), str(guiOutputLocation.get())))
    t.start()


guiStartButton = customtkinter.CTkButton(master=frame, height=50, text="Start", command=guiStart)
guiStartButton.pack(pady=10, padx=10)

progressText = StringVar()

guiProgressBarText = customtkinter.CTkTextbox(master=frame, font=("Arial", 10), width=750, height=150)
guiProgressBarText.bind("<Key>", lambda e: "break")
guiProgressBarText.pack(pady=20, padx=20)



def guiDownload(textBox, window):
    t = Thread(target=installGPULibraries, args=(textBox, window))
    t.start()

def guiOpenGPUWindow():
    global GPUWindowEnableClosing
    GPUWindowEnableClosing = True
    GPUWindow = customtkinter.CTkToplevel(root)
    GPUWindow.focus_force()
    GPUWindow.grab_set()
    GPUWindow.geometry(
        f"{500}x{450}+{int((root.winfo_screenwidth() - 500) / 2)}+{int((root.winfo_screenheight() - 450) / 2)}")
    GPUWindow.title("Using GPU")
    GPUWindow.resizable(0, 0)


    GPUWindowLabel = customtkinter.CTkLabel(master=GPUWindow, text="How to use the GPU", font=("Arial", 20))
    GPUWindowLabel.pack(pady=10, padx=20, side=TOP)

    GPUWindowRequirements = customtkinter.CTkLabel(master=GPUWindow, wraplength=400,
                                                   text="Important notes:\nNVIDIA GPUs only, a minimum requirement of GTX 1060 6GB, and at least 8GBs ofV-RAM are recommended.\nRestart the app after downloading the GPU Python Libraries.\nIf you face issues or the app doesn't work, open the file mode.txt in the directory of the app and change it to CPU",
                                                   font=("Arial", 12))
    GPUWindowRequirements.pack(pady=10, padx=20, side=TOP)

    GPUWindowCuda = customtkinter.CTkButton(master=GPUWindow, width=200, height=50, text="Download CUDA 12.4",
                                            command=lambda: webbrowser.open(
                                                "https://developer.nvidia.com/cuda-12-4-0-download-archive"))
    GPUWindowCuda.pack(pady=0, padx=20)





    GPUWindowTextBox = customtkinter.CTkTextbox(master=GPUWindow, font=("Arial", 10), width=400, height=100)
    GPUWindowTextBox.bind("<Key>", lambda event: "break")
    GPUWindowTextBox.pack(pady=20, padx=20, side=BOTTOM)


    GPUWindow.bind("<<Foo>>", lambda event: insertTextBox(GPUWindowTextBox))



    GPUWindowLibraries = customtkinter.CTkButton(master=GPUWindow, width=200, height=50,
                                                 text="Download GPU Python Libraries",
                                                 command=lambda: guiDownload(GPUWindowTextBox, GPUWindow))
    GPUWindowLibraries.pack(pady=20, padx=20)


    GPUWindow.protocol("WM_DELETE_WINDOW", lambda: closingGPUWindow(GPUWindow, GPUWindowTextBox))







guiGPUHelpButton = customtkinter.CTkButton(master=frame, height=100, text="How to Use GPU", command=lambda: guiOpenGPUWindow() if enableOpenGPUWindow else tkinter.messagebox.showerror(
                                               'ERROR', "Please wait for the current process to finish"))

guiGPUHelpButton.pack(pady=20, padx=21)



sys.stdout = StdoutRedirector(guiProgressBarText)
sys.stderr = StdoutRedirector(guiProgressBarText)


root.mainloop()

