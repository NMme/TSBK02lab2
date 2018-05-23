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
