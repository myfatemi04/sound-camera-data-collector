from picamera import PiCamera
import pyaudio
import time
import scipy.io.wavfile as wavfile
import numpy as np

def record(name: str, duration: int, delay: int = 5, audio_sample_rate = 16000):
  print(f"Starting recording in {delay} seconds")
  time.sleep(delay)

  pyaudio_instance = pyaudio.PyAudio()
  audio_stream = pyaudio_instance.open(audio_sample_rate, 8, pyaudio.paInt16, input_device_index=1)
  audio_chunks = []
  audio_chunk_size = 1024
  audio_chunk_count = (duration * audio_sample_rate) // audio_chunk_size

  camera = PiCamera()
  camera.start_recording('./recordings/' + name + '.mp4')

  # PiCamera recording is done in the background. Instead of making a separate thread to perform recording with PyAudio, we'll just do it here.
  print("Recording")
  
  for _ in range(audio_chunk_count):
    audio_chunk = audio_stream.read(audio_chunk_count)
    audio_chunks.append(audio_chunk)

  camera.stop_recording()

  audio = np.frombuffer(b''.join(audio_chunks), dtype=np.int16)
  audio = audio.reshape((audio_chunk_count * audio_chunk_size, 8))

  wavfile.write('./recordings/' + name + '.wav', audio_sample_rate, audio)
