# This file contains the encoder

# import modules
import numpy as np
from scipy.io import wavfile
from scipy import fftpack 
from scipy import stats
import matplotlib.pyplot as plt

# Parameters
path = '../samples/heyhey.wav'
bl_size = 8192 

# read wavefile
fs, data = wavfile.read(path)
data = np.ravel(data)
#data = data[1::2]

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
	r_coeff[i] = round(7 + 0.5*math.log(var_coeff[i]/nenner ,2))

# find wertebereich
minmax_coeff = np.zeros((bl_size, 2))
for i in range(0,bl_size):
	minmax_coeff[i][0] = np.amin(coeff[i])
	minmax_coeff[i][1] = np.amax(coeff[i])

quan_table = np.zeros(bl_size)
for i in range(0,bl_size):
	quan_table[i] = round( (minmax_coeff[i][1] - minmax_coeff[i][0])/(2.0**r_coeff[i]) )

print quan_table
print r_coeff 
print np.mean(r_coeff)

# quantize according to the statistics
for i in range(0,len(blocks)):
	for j in range(0, bl_size):
		blocks[i][j] = blocks[i][j] / quan_table[j]
	blocks[i] = blocks[i].astype(int)
	#print blocks[i]

# some statistics for sourcecoding
#print (float)(len(np.ravel(blocks)) - np.count_nonzero(np.ravel(blocks))) / len(np.ravel(blocks))

import source_coding

# calculate bitrate with huffman coding
hist, bin_edges = np.histogram( np.ravel(blocks), bins=np.arange(np.amin(blocks),np.amax(blocks), 1), density=True)
hist = hist*np.diff(bin_edges)
print bin_edges
rh = source_coding.huffmanrate(hist)
print "rate huffman: ", rh


# calculate bitrate using runlength coding
#rr = source_coding.runlengthrate(np.ravel(blocks))
#print len(rr)
#print len(np.ravel(blocks))
rj = source_coding.jpgrate(blocks)
print "rate jpg: ", rj 

# -------------------------------------------

# decoding 
for i in range(0,len(blocks)):
	for j in range(0, bl_size):
		blocks[i][j] = blocks[i][j] * quan_table[j]
	blocks[i] = fftpack.idct(blocks[i], norm='ortho')
	blocks[i] = blocks[i].astype(int)

blocks = np.ravel(blocks)

msqer = ((data - blocks) ** 2).mean()
print ("SNR: ", 10*math.log10(np.var(data)/msqer))

out_l = blocks[1::2]
out_r = blocks[0::2]
out = [[b[i], b[i+1]] for i in range(0,len(blocks)/2)]
wavfile.write("out.wav", fs, out)
