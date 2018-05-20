# import modules
import numpy as np
from scipy.io import wavfile
from scipy import fftpack 
from scipy import stats
import matplotlib.pyplot as plt

# Parameters
path = '../samples/heyhey01.wav'
bl_size = 512 

# read wavefile
fs, data = wavfile.read(path)
data = np.ravel(data)

# divide data in blocks
l_over = len(data)%bl_size
rest = data[len(data)-l_over :]
data = data[: len(data)-l_over]
blocks = [data[i:i+bl_size] for i in range(0, len(data), bl_size)]

# transform blocks with DTC and Quantize them
for i in range(0,len(blocks)):
	blocks[i] = fftpack.dct(blocks[i], norm='ortho')
	#blocks[i] = stats.threshold(blocks[i], threshmin=1)
	#blocks[i] = blocks[i]/16
	#blocks[i] = blocks[i] + 0.5
	#blocks[i] = blocks[i].astype(int)
	#blocks[i] = np.clip(blocks[i], None, 256)

# calculate variance of transform coefficients
coeff = np.zeros((bl_size, len(blocks)))
for i in range(0,len(blocks)):
	for j in range(0, bl_size):
		coeff[j][i] = blocks[i][j]

var_coeff = np.zeros(bl_size)
for i in range(0,len(coeff)):
	var_coeff[i] = np.var(coeff[i])

import math
r_coeff = np.zeros(bl_size)
nenner = np.prod( np.power(var_coeff, 1.0/bl_size))
for i in range(0, len(var_coeff)):
	r_coeff[i] = round(4.3 + 0.5*math.log(var_coeff[i]/nenner ,2))

# find wertebereich
minmax_coeff = np.zeros((bl_size, 2))
for i in range(0,bl_size):
	minmax_coeff[i][0] = np.amin(coeff[i])
	minmax_coeff[i][1] = np.amax(coeff[i])

quan_table = np.zeros(bl_size)
for i in range(0,bl_size):
	quan_table[i] = round( (minmax_coeff[i][1] - minmax_coeff[i][0])/(2.0**r_coeff[i]) )

# quantize according to the statistics
for i in range(0,len(blocks)):
	for j in range(0, bl_size):
		blocks[i][j] = blocks[i][j] / quan_table[j]
	blocks[i] = blocks[i].astype(int)

# decoding for testing
for i in range(0,len(blocks)):
	for j in range(0, bl_size):
		blocks[i][j] = blocks[i][j] * quan_table[j]
	blocks[i] = fftpack.idct(blocks[i], norm='ortho')
	blocks[i] = blocks[i].astype(int)

'''
signal = blocks[0]
for i in range(1,len(blocks)):
	signal[i*bl_size/2 :] = (signal[i*bl_size/2 : ] + blocks[i][ : bl_size/2 ])/2
	signal = np.append(signal, blocks[i][bl_size/2 :])
'''
signal = np.array([])
for b in blocks:
	signal = np.append(signal, b)

msqer = 0
for i in range(0,len(signal)):
	msqer += (data[i]-signal[i])**2
msqer = msqer/len(signal)

print ("SNR: ", 10*math.log10(np.var(data)/msqer))
