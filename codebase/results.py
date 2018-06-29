# This file contains the encoder

# import modules
import numpy as np
from scipy.io import wavfile
from scipy import fftpack 
from scipy import stats
import math
import source_coding

# Parameters
path = '../samples/nuit01.wav'

def codemusic(avg_q, bl_size):
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
	rj = source_coding.jpgrate(blocks)
	#print "rate jpg: ", rj 

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
	snr = 10*math.log10(np.var(data)/msqer)
	#print ("SNR: ", snr)

	return [2*rj, snr]


# skript zur auswertung
results = np.zeros((8, 6, 2))
q_vals = np.arange(2, 8, 1)
for b in range(6,14):
	bl_s = 2**b
	for idx, q in enumerate(q_vals):
		stats =	codemusic(q,b)
		#stats = [1, 4]
		results[b-6][idx][0] = stats[0]
		results[b-6][idx][1] = stats[1]
	print bl_s, " done!!"

print results		
import matplotlib.pyplot as plt
for r in results:
	x = [i[0] for i in r] 
	y = [i[1] for i in r] 
	plt.plot(x,y)
plt.ylabel('SNR in dBs')
plt.xlabel('Bitrate in bits per samples')
plt.legend()
plt.show()
