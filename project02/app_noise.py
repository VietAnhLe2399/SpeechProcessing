import tkinter as tk
from tkinter import W, S, N, E
from tkinter.filedialog import askopenfilename
import pyaudio
import wave
import os
import pickle
from train_model import get_mfcc
import librosa, librosa.display
import scipy as sp
import soundfile as sf
import matplotlib.pyplot as plt

class App:
    def __init__(self, chunk=1024, sample_format=pyaudio.paInt16, channels=2, rate=44100, p=pyaudio.PyAudio()):
        # For recording
        self.CHUNK = chunk
        self.FORMAT = sample_format
        self.CHANNELS = channels
        self.RATE = rate
        self.p = p
        self.frames = []
        self.st = 1
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        self.recording = False

        # For model
        self.models = pickle.load(open("models_noise.pkl", "rb"))
        self.file_path = ""
        # self.predict = ""

        # For App
        self.main = tk.Tk()
        self.main.geometry('400x250')
        self.main.title('Speech Recognition')

        self.file_name = tk.Label(text="No file selected")
        self.record_state = tk.Label(text="")
        self.result_text = tk.Label(text="Result: ")
        self.noise_text = tk.Label(text="")

        self.btn_record = tk.Button(self.main, text = "Start Record", width = 12, command=self.record)
        self.btn_select = tk.Button(self.main, text = "Select File", width = 12, command=self.open_file)
        self.btn_predict = tk.Button(self.main, text = "Predict", width = 12, command=self.predict)
        self.btn_remove = tk.Button(self.main, text = "Remove Noise", width = 12, command=self.remove_noise)


        self.btn_record.grid(row=0, column=0, padx = 5, pady = 10)
        self.record_state.grid(row=0, column=1, sticky=W, padx = 20)
        self.btn_select.grid(row=1, column=0, padx = 5, pady = 10)
        self.file_name.grid(row=1, column=1, sticky=W, padx = 20)
        self.btn_remove.grid(row=2, column=0, padx = 5, pady = 10)
        self.noise_text.grid(row=2, column=1, sticky=W, padx = 20)
        self.btn_predict.grid(row=3, column=0, rowspan=2, pady = 10)
        self.result_text.grid(row=3, column=1, sticky=W, padx = 20, pady=50)
        self.main.mainloop()

    def start_record(self):
        self.result_text.config(text="Result: ")
        self.st = 1
        self.frames = []
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        print("start recording")
        while self.st == 1:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            self.main.update()
        stream.close()
        wf = wave.open('test.wav', 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def stop_record(self):
        self.st = 0
        print("recording completed")

    def record(self):
        if self.recording == True:
            self.btn_record.config(text="Start Record")
            self.record_state.config(text="")
            self.noise_text.config(text="")
            self.recording = False
            self.stop_record()
            self.file_path = "test.wav"
        elif self.recording == False:
            self.btn_record.config(text="Stop Record")
            self.record_state.config(text="Recording ...")
            self.recording = True
            self.start_record()

    def open_file(self):
        """Predict from recorded file"""
        self.result_text.config(text="Result: ")
        self.noise_text.config(text="")
        self.file_path = askopenfilename(
            filetypes=[("WAV Files", "*.wav"), ("All Files", "*.*")])
        if not self.file_path:
            return
        print("File Selected")
        self.file_name.config(text=self.file_path.split('/')[-1])

    def predict(self):
        print("predicting file: ", self.file_path)
        if not self.file_path:
            print("NO file")
            return
        O = get_mfcc(self.file_path)
        score = {cname : model.score(O, [len(O)]) for cname, model in self.models.items()}
        predict = max(score, key=score.get)
        print("predicted")
        self.result_text.config(text="Result: "+predict)

    def remove_noise(self):
        y,sr = librosa.load(self.file_path, duration=10)
        y_filted = sp.signal.medfilt(y,3)
        y_filted, index = librosa.effects.trim(y_filted, top_db=25)
        # y, index = librosa.effects.trim(y, top_db=10)

        # plot waveform
        # plt.figure()
        # plt.subplot(3,1,1)
        # librosa.display.waveplot(y_filted, sr = sr)

        # write file
        sf.write('noise_removed.wav',y_filted, sr, 'PCM_24')
        self.file_path = 'noise_removed.wav'
        self.noise_text.config(text="Noise removed")
        print(f"Noise removed: {librosa.get_duration(y)} (s) -> {librosa.get_duration(y_filted)} (s)")


# Create an object of the ProgramGUI class to begin the program.
# main = tk.Tk()
# main.title('Speech Recognition')
# main.geometry('400x200')
app = App()
# main.mainloop()