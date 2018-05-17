# This file contains the encoder

# import modules
import numpy as np
from scipy.io import wavfile
from scipy import fftpack 
from scipy import stats
import matplotlib.pyplot as plt

# Parameters
path = '../samples/heyhey01.wav'
bl_size = 128

# read wavefile
fs, data = wavfile.read(path)
data = np.ravel(data)

# divide data in blocks
l_over = len(data)%bl_size
rest = data[len(data)-l_over :]
data = data[: len(data)-l_over]
blocks = [data[i:i+bl_size] for i in range(0, len(data), bl_size/2)]

# transform blocks with DTC and Quantize them
for b in blocks:
	b = fftpack.dct(b, norm='ortho')
	b = stats.threshold(b, threshmin=10)
	b = b/16
	b = b + 0.5
	b = b.astype(int)
	b = np.clip(b, 0, 256)

