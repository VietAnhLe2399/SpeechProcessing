# Import the necessary modules.
import tkinter
import tkinter as tk
import tkinter.messagebox
import pyaudio
import wave
import os


class RecAUD:

    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=2, rate=44100, py=pyaudio.PyAudio()):

        # Start Tkinter and set Title
        self.main = tkinter.Tk()
        self.collections = []
        self.main.geometry('500x300')
        self.main.title('Record')
        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.frames = []
        self.st = 1
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        self.file_name = "nhân viên_"
        self.file_count = 0

        # Set Frames
        self.buttons = tkinter.Frame(self.main, padx=120, pady=20)

        # Pack Frame
        self.buttons.pack(fill=tk.BOTH)



        # Start and Stop buttons
        self.strt_rec = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Start Recording', command=lambda: self.start_record())
        self.strt_rec.grid(row=0, column=0, padx=50, pady=5)
        self.stop_rec = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Stop Recording', command=lambda: self.stop())
        self.stop_rec.grid(row=1, column=0, columnspan=1, padx=50, pady=5)

        tkinter.mainloop()

    def start_record(self):
        self.st = 1
        self.frames = []
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        print("* recording")
        while self.st == 1:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            self.main.update()

        stream.close()

        wf = wave.open(self.file_name+str(self.file_count)+'.wav', 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        self.file_count += 1

    def stop(self):
        self.st = 0


# Create an object of the ProgramGUI class to begin the program.
guiAUD = RecAUD()