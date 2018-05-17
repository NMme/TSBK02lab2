# This file contains the encoder

# import modules
import numpy as np
from scipy.io import wavfile
from scipy import fftpack 
import matplotlib.pyplot as plt

# Parameters
path = '../samples/heyhey01.wav'
bl_size = 128

# read wavefile
fs, data = wavfile.read(path)
data = np.ravel(data)

l_over = len(data)%bl_size
rest = data[len(data)-l_over :]
data = data[: len(data)-l_over]
blocks = [data[i:i+bl_size] for i in range(0, len(data), bl_size/2)]
