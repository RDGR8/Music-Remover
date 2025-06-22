# https://pytorch.org/get-started/previous-versions/
# https://pypi.org/project/audio-separator/

from tkinter import *
from tkinter.ttk import Progressbar

window = Tk()
progressText = Text(window, height=10)
bar = Progressbar(window, orient=HORIZONTAL, length=300)
bar.pack(pady=10)

directImports = ["os.path", "tkinter.messagebox", "os", "ffmpeg", "sys", "customtkinter", "tempfile", "logging" ,"webbrowser", "subprocess"]
fromImports = [["tkinter", "filedialog"], ["threading", "Thread"], ["io", "StringIO"], ["audio_separator", "separator"], ["sympy.abc", "lamda"]]

totalBar = len(directImports) + len(fromImports) + 10

for directImport in directImports:
    progressText.delete('1.0', END)
    progressText.insert(END, f"importing {directImport}")
    exec(f"import {directImport}")
    bar['value'] += 100/totalBar



with open('mode.txt', 'r') as f:
    mode = f.read()
sys.path.insert(1, f'.venv/{mode}separator/')


for i in range(len(fromImports)):
    progressText.delete('1.0', END)
    progressText.insert(END, f"importing {fromImports[i][1]} from {fromImports[i][0]} ")
    exec(f"from {fromImports[i][0]} import {fromImports[i][1]}")
    bar['value'] += 100/totalBar


progressText.delete('1.0', END)
progressText.insert(END, "Initiating the program")

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
        ".venv\Scripts\python.exe -m pip install onnx==1.16.1 -t .venv\\GPUseparator".split(),
        stdout=subprocess.PIPE, bufsize=1, text=True)
    while p.poll() is None:
        msg = p.stdout.readline().strip()  # read a line from the process output
        if msg:
            window.event_generate("<<Foo>>", when="tail")

    p = subprocess.Popen(
        ".venv\Scripts\python.exe -m pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu124 -t .venv\\GPUseparator".split(),
        stdout=subprocess.PIPE, bufsize=1, text=True)
    while p.poll() is None:
        msg = p.stdout.readline().strip()  # read a line from the process output
        if msg:
            window.event_generate("<<Foo>>", when="tail")

    p = subprocess.Popen(
        ".venv\Scripts\python.exe -m pip install numpy==2.1.2 --upgrade --index-url https://download.pytorch.org/whl/cu124 -t .venv\\GPUseparator".split(),
        stdout=subprocess.PIPE, bufsize=1, text=True)
    while p.poll() is None:
        msg = p.stdout.readline().strip()  # read a line from the process output
        if msg:
            window.event_generate("<<Foo>>", when="tail")

    p = subprocess.Popen(".venv\Scripts\python.exe -m pip install audio-separator[gpu]==0.28.5 -t .venv\\GPUseparator".split()
                         ,stdout=subprocess.PIPE, bufsize=1, text=True)
    while p.poll() is None:
        msg = p.stdout.readline().strip()  # read a line from the process output
        if msg:
            window.event_generate("<<Foo>>", when="tail")

    p = subprocess.Popen(".venv\Scripts\python.exe -m pip cache purge".split()
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

    def combobox_callback(choice):
        combobox_var.set(mode)
        with open('mode.txt', 'w') as f:
            f.write(choice)

        if(choice != mode):
            tkinter.messagebox.showinfo("Changing mode", f"Processing will be changed to {choice} after restarting the app")
        else:
            tkinter.messagebox.showinfo("Changing mode", f"Processing currently is {mode}")
    combobox_var = customtkinter.StringVar(value="GPU")
    combobox = customtkinter.CTkComboBox(master=GPUWindow, values=["CPU", "GPU"],
                                         command=combobox_callback, variable=combobox_var)
    combobox_var.set(mode)
    combobox.pack(pady=5, padx=5, side=TOP)

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
    GPUWindowTextBox.pack(pady=20, padx=20)


    GPUWindow.bind("<<Foo>>", lambda event: insertTextBox(GPUWindowTextBox))



    GPUWindowLibraries = customtkinter.CTkButton(master=GPUWindow, width=200, height=50,
                                                 text="Download GPU Python Libraries",
                                                 command=lambda: guiDownload(GPUWindowTextBox, GPUWindow))
    GPUWindowLibraries.pack(pady=20, padx=20)


    GPUWindow.protocol("WM_DELETE_WINDOW", lambda: closingGPUWindow(GPUWindow, GPUWindowTextBox))







guiGPUHelpButton = customtkinter.CTkButton(master=frame, height=100, text="Processing modes (CPU/GPU)", command=lambda: guiOpenGPUWindow() if enableOpenGPUWindow else tkinter.messagebox.showerror(
                                               'ERROR', "Please wait for the current process to finish"))

guiGPUHelpButton.pack(pady=20, padx=21)



sys.stdout = StdoutRedirector(guiProgressBarText)
sys.stderr = StdoutRedirector(guiProgressBarText)

window.destroy()

root.mainloop()

