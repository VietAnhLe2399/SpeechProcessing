import tkinter as tk
from tkinter import W, S, N, E
from tkinter.filedialog import askopenfilename
from trainModel import get_mfcc
import pyaudio
import wave
import threading
import pickle
from record import Record

recording = False
chunk = 1024
sample_format = pyaudio.paInt16
channels = 2
fs = 44100
frames = []

# def start_record(p):
#     global frames
#     stream = p.open(format=sample_format, channels=channels, rate=fs,
#                                   frames_per_buffer=chunk, input=True)
#     print('Recording')
#     t = threading.Thread(target=record_data)
#     t.start()

# def stop_record(p):
#     global frames
#     print(frames)
#     print('recording complete')
#     filename = 'data.wav'
#     wf = wave.open(filename, 'wb')
#     wf.setnchannels(channels)
#     wf.setsampwidth(p.get_sample_size(sample_format))
#     wf.setframerate(fs)
#     wf.writeframes(b''.join(frames))
#     wf.close()
#     frames.clear()

# def record_data():
#     global frames
#     global stream
#     while recording:
#         data = stream.read(chunk)
#         frames.append(data)
#         print("FRAMES: ", frames)

# def record():
#     global recording
#     # frames = []
#     p = pyaudio.PyAudio()
#     if recording == True:
#         btn_record.config(text="Start Record")
#         record_state.config(text="")
#         recording = False
#         stop_record(p)
#     elif recording == False:
#         btn_record.config(text="Stop Record")
#         record_state.config(text="Recording ...")
#         start_record(p)
#         recording = True


def record():
    global recording
    record = Record()
    if recording == True:
        btn_record.config(text="Start Record")
        record_state.config(text="")
        recording = False
        record.stop_record()
    elif recording == False:
        btn_record.config(text="Stop Record")
        record_state.config(text="Recording ...")
        record.start_record()
        recording = True


def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Sound Files", "*.wav"), ("All Files", "*.*")])
    if not filepath:
        return
    file_name.config(text=filepath.split('/')[-1])

def predict():
    result_text.config(text="")

window = tk.Tk()
window.title("Speech Recognition")
window.geometry('400x200')

file_name = tk.Label(text="No file selected")
record_state = tk.Label(text="")
result_text = tk.Label(text="Result: ")

WIDTH_BTN, HEIGHT_BTN = 12, 2
btn_record = tk.Button(window, text = "Start Record", width = WIDTH_BTN, command=record)
# btn_stop_record = tk.Button(window, text = "Stop Record", width = WIDTH_BTN, command=stop_record)
btn_select = tk.Button(window, text = "Select File", width = WIDTH_BTN, command=open_file)
btn_predict = tk.Button(window, text = "Predict", width = WIDTH_BTN, height = HEIGHT_BTN)

btn_record.grid(row=0, column=0, padx = 5, pady = 10)
# btn_stop_record.grid(row=0, column=3, padx = 5, pady = 10)
record_state.grid(row=0, column=1, sticky=W, padx = 20)
btn_select.grid(row=1, column=0, padx = 5, pady = 10)
file_name.grid(row=1, column=1, sticky=W, padx = 20)
btn_predict.grid(row=2, column=0, rowspan=2, pady = 25)
# btn_predict.place(x=300, y=15)
result_text.grid(row=2, column=1, sticky=W, padx = 20, pady=50)

window.mainloop()