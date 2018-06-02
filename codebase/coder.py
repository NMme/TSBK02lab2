# This file contains the encoder

# import modules
import numpy as np
from scipy.io import wavfile
from scipy import fftpack 
from scipy import stats
import math

# Parameters
path = '../samples/nuit.wav'
bl_size = 2048	
avg_q = 5.4

# read wavefile
fs, data = wavfile.read(path)
data = np.ravel(data)					# flatten array to 1-dim

# divide data in blocks
l_over = len(data)%bl_size
rest = data[len(data)-l_over :]
data = data[: len(data)-l_over]
blocks = np.array([data[i:i+bl_size] for i in range(0, len(data), bl_size)], dtype=np.int32)
#blocks = np.append(blocks, rest)

# transform blocks with DTC and Quantize them
for i in range(0,len(blocks)):
	blocks[i] = fftpack.dct(blocks[i], norm='ortho')

# group all coeffiecents
coeff = np.zeros((bl_size, len(blocks)))
for i in range(0,len(blocks)):
	for j in range(0, bl_size):
		coeff[j][i] = blocks[i][j]

# calculate variance for each coefficient
var_coeff = [np.var(c) for c in coeff]

# calculate quantization levels per coefficient 
nenner = np.prod( np.power(var_coeff, 1.0/bl_size))
r_coeff = [(int)(avg_q + 0.5*math.log(v/nenner ,2)) for v in var_coeff]

# find uniform quantization intervals  
quan_table = [( (np.amax(coeff[i])- np.amin(coeff[i]))/(2.0**r_coeff[i]) ) for i in range(0,bl_size)]

# quantize according to the table
for i in range(0,len(blocks)):
	for j in range(0, bl_size):
		blocks[i][j] = blocks[i][j] / quan_table[j] 	# this is the quantization
	blocks[i] = blocks[i].astype(int)

# estimate bitrate with jpg source coding
import source_coding
rj = source_coding.jpgrate(blocks)
print "rate jpg: ", rj 
print "bits per second: ", rj*2*fs

# -------------------------------------------

# Decoding 
for i in range(0,len(blocks)):
	for j in range(0, bl_size):
		blocks[i][j] = blocks[i][j] * quan_table[j]				# reconstruction
	blocks[i] = fftpack.idct(blocks[i], norm='ortho')		# inverse dct
	blocks[i] = blocks[i].astype(int)										# integer casting

blocks = np.ravel(blocks)

# Calculate SNR
msqer = ((data - blocks) ** 2).mean()
print ("SNR: ", 10*math.log10(np.var(data)/msqer))

#out = np.array([ np.array([blocks[i], blocks[i+1]], dtype=np.int16) for i in range(0,len(blocks),2)], dtype=np.int16 ) 
#wavfile.write("out.wav", fs, out)
