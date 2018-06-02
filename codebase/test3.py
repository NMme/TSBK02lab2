# import modules
import numpy as np
from scipy.io import wavfile
from scipy import fftpack 
from scipy import stats
import matplotlib.pyplot as plt
import mdct

# Parameters
path = '../samples/heyhey01.wav'
bl_size = 512 

# read wavefile
fs, data = wavfile.read(path)
data = np.ravel(data)
data = data[1::2]

spectrum = mdct.mdct(data)
print len(spectrum[0])
