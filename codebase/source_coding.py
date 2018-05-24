# contains functions to estimate the bitrate different sourcecodings would need
import numpy as np

# simple Huffman coding
def huffmanrate(p):
	ml=0	
	nnz = np.count_nonzero(p)
	
	if nnz > 0:
		for k in range(0,nnz-1):
			p = p[np.nonzero(p)]
			idx = np.argsort(p)
			b0 = idx[0]	
			b1 = idx[1]
			p[b1] = p[b1] + p[b0]
			p[b0] = 0
			ml += p[b1]
		ml += 1	
		print np.sum(p)

	return ml

# simple runlength coding approach
from itertools import *
def runlengthrate(B):
	return [(len(list(group)),name) for name, group in groupby(B)]

import math

def jpgrate(B):
	bpr = 15
	bits = 0
	
	# start with DC component
	dc_comp = [b[0] for b in B]	
	dc_diff = np.ediff1d(dc_comp)
	dc_size = []
	for c in dc_diff:
		if c == 0: dc_size.append(0)
		elif abs(c) == 1: dc_size.append(1)
		elif abs(c) <= 3: dc_size.append(2)
		elif abs(c) <= 7: dc_size.append(3)
		elif abs(c) <= 15: dc_size.append(4)
		elif abs(c) <= 31: dc_size.append(5)
		elif abs(c) <= 63: dc_size.append(6)
		elif abs(c) <= 127: dc_size.append(7)
		elif abs(c) <= 255: dc_size.append(8)
		elif abs(c) <= 511: dc_size.append(9)
		elif abs(c) <= 1023: dc_size.append(10)
		
	# create huffman code for size
	unique, counts = np.unique(dc_size, return_counts=True)
	dc_p= counts.astype(float)/len(dc_size)
	bits += huffmanrate(dc_p)*len(dc_size)
	bits += np.sum(dc_size)
	
	print "DC-comp rate: ", bits.astype(float)/len(dc_size)
	
	# AC component
	comp = []	
	for b in B:
		indx = np.flatnonzero(b[1:])
		indx_diff = np.ediff1d(indx)
		for i in range(0,len(indx_diff)):
			if indx_diff[i] == 1: comp.append([0, (int)(math.log(abs(b[indx[i]+1]), 2) +1)])
			elif indx_diff[i] <= bpr+1: comp.append([indx_diff[i]-1, (int)(math.log(abs(b[indx[i]+1]), 2)+1)])
			elif indx_diff[i] > bpr+1:
				for k in range(1, (int)(indx_diff[i]-1)/bpr):
					comp.append([bpr, 0])
				comp.append([(indx_diff[i]-1)%bpr, (int)(math.log(abs(b[indx[i]+1]), 2)+1)])
		if len(indx) == 0:
			comp.append([0,0])
		elif indx[-1] != len(b)-2:
			comp.append([0, 0])
		
	# huffman coderate for pairs
	comp_num = [c[0]*(bpr+1)+c[1] for c in comp]
	unique, counts = np.unique(comp_num, return_counts=True)
	comp_p = counts.astype(float)/len(comp_num)
	bits += huffmanrate(comp_p)*len(comp_num)
	bits += np.sum([c[1] for c in comp])
	rate = bits.astype(float)/np.size(B)
	
	return rate

