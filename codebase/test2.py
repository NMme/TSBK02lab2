# import modules
import numpy as np
from scipy.io import wavfile
from scipy import fftpack 
from scipy import stats
import matplotlib.pyplot as plt

# Parameters
path = '../samples/heyhey.wav'
bl_size = 4096

# read wavefile
fs, data_all = wavfile.read(path)
data = np.ravel(data_all)
#data2 = data_all[1::2]
#data = np.subtract(data2, data_all[0::2])

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

print quan_table
print r_coeff 
print np.mean(r_coeff)

# quantize according to the statistics
for i in range(0,len(blocks)):
	for j in range(0, bl_size):
		blocks[i][j] = blocks[i][j] / quan_table[j]
	blocks[i] = blocks[i].astype(int)
	#print blocks[i]

hists = []
bins = []
for i in range(0, bl_size):
	bins.append(np.zeros(2**r_coeff[i] +1).astype(int))
	bins[i][0] = int(round(minmax_coeff[i][0]))
	bins[i][len(bins[i])-1] = int(round(minmax_coeff[i][1]))
	hist, bin_edges = np.histogram(coeff[i], bins=(round(minmax_coeff[i][1])-round(minmax_coeff[i][0])))
	hists.append(hist)
	print hists
	print hists[i]
	#plt.plot(hists[i])
	#plt.show()
	equ_size = np.sum(hists[i])/(2.0**r_coeff[i])
	print equ_size
	print np.sum(hists[i][0:len(hists[i])])
	for j in range(1,len(bins[i])):
		s = 1
		start = abs(bins[i][j-1]-bins[i][0])
		#print start
		while np.sum(hists[i][ start : start+s ]) < equ_size and start+s <len(hists[i]) :		
			s = s+1
			#print s
			#print hists[i][s]
			#print np.sum(hists[i][ abs(bins[i][j-1]-bins[i][0]) : abs(bins[i][j-1]-bins[i][0])+s ])
		bins[i][j] = bins[i][j-1] +s
	print bins[i]
	

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

blocks = np.ravel(blocks)

msqer = 0
for i in range(0,len(blocks)): msqer += (data[i]-blocks[i])**2
msqer = msqer/len(blocks)

print ("SNR: ", 10*math.log10(np.var(data)/msqer))
