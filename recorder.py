import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading

class VoiceRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recorder")
        self.root.geometry("300x200")
        self.root.configure(bg="#1e1e1e")  # Dark background
        self.is_recording = False
        self.fs = 44100  # Sample rate
        self.frames = []

        # Title Label
        title_label = tk.Label(root, text="Voice Recorder", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#ffffff")
        title_label.pack(pady=10)

        # Instructions Label
        instruction_label = tk.Label(root, text="Press Start to begin recording", font=("Arial", 10), bg="#1e1e1e", fg="#aaaaaa")
        instruction_label.pack(pady=5)

        # Start button
        self.start_button = tk.Button(root, text="Start Recording", font=("Arial", 12), bg="#28a745", fg="#ffffff",
                                      activebackground="#218838", activeforeground="#ffffff", width=15, command=self.start_recording)
        self.start_button.pack(pady=10)

        # Stop button
        self.stop_button = tk.Button(root, text="Stop Recording", font=("Arial", 12), bg="#dc3545", fg="#ffffff",
                                     activebackground="#c82333", activeforeground="#ffffff", width=15, state=tk.DISABLED, command=self.stop_recording)
        self.stop_button.pack(pady=10)

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.record_thread = threading.Thread(target=self.record)
        self.record_thread.start()

    def record(self):
        with sd.InputStream(samplerate=self.fs, channels=1, callback=self.callback):
            while self.is_recording:
                sd.sleep(100)

    def callback(self, indata, frames, time, status):
        if self.is_recording:
            self.frames.append(indata.copy())

    def stop_recording(self):
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_recording()

    def save_recording(self):
        audio_data = np.concatenate(self.frames, axis=0)
        write("output.wav", self.fs, audio_data)
        messagebox.showinfo("Voice Recorder", "Recording saved as output.wav")

# Running the application
root = tk.Tk()
app = VoiceRecorder(root)
root.mainloop()
