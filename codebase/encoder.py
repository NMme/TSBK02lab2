# This is a python script for encoding audio-signals
import numpy as np
from scipy.io import wavfile

fs, data = wavfile.read('../samples/heyhey01.wav')
data = np.ravel(data)
data = data[1::2]

# Create histogram
#hist, bins = np.histogram(data, bins=range(-32768, 32767)) 
