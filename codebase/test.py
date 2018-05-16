
# This is a python script for encoding audio-signals
import numpy as np
from scipy.io import wavfile
from scipy import fftpack 
import matplotlib.pyplot as plt

fs, data = wavfile.read('../samples/heyhey01.wav')
data2 = np.ravel(data)
data_l = data2[1::2]
data_r = data2[0::2]

print data
print data_l
print data_r

s = data_l[:16]
trans = fftpack.dct(s, norm='ortho')
print "DCT:"
for i in trans:
	print i

print "Quantisiert:"
quan = [8, 7, 5, 5, 4, 4, 3, 2 ,2 ,1 ,1 ,1 ,0 ,0 ,0 ,0]
for x in range(0,len(trans)):
	if(quan[x] > 0):	trans[x] = int(trans[x]/quan[x] + 0.5)
	else: trans[x]= 0
	print trans[x]

print "reQuantisiert:"
for x in range(0,len(trans)):
	if(quan[x] > 0):	trans[x] = trans[x]*quan[x]
	else: trans[x]= 0
	print trans[x]

trans = fftpack.idct(trans, norm='ortho')
print "inverse DCT:"
for i in trans:
	print int(i)

print "Error:"
msqer = 0
for i in range(0, len(trans)):
	msqer = msqer + (s[i]-int(trans[i]))**2

msqer = msqer/16.0
print msqer

variance = 0
print "Original:"
for i in s:
	print i
	variance = variance + i**2

variance = variance/len(s)
print ("Variance: ", variance)
import math
print ("SNR: ", 10*math.log10(variance/msqer))

'''
# remove frequencies larger than sample-frequencies
spectrum = np.fft.fft(data)
spectrum = spectrum[:len(spectrum)/2]
s1 = spectrum[:5512] 
s2 = spectrum[5512:11025] 
s3 = spectrum[11025:22050]
s4 = spectrum[22050:]
plt.figure(1)
plt.plot(s2)

# signals
y1 = np.fft.ifft(s1)
y2 = np.fft.ifft(s2)
y3 = np.fft.ifft(s3)
y4 = np.fft.ifft(s4)

# downsampling
w1 = y1[1::4]
w2 = y2[1::4]
w3 = y3[1::2]
w4 = y4

# upsampling
v1 = np.zeros(len(y1), dtype=w1.dtype)
v1[::4] = w1
v2 = np.zeros(len(y2)-1, dtype=w2.dtype)
v2[::4] = w2
v3 = np.zeros(len(y3)-1, dtype=w3.dtype)
v3[::2] = w3
v4 = w4

# reconstruction
u1 = np.fft.fft(w1)
u2 = np.fft.fft(w2)
u3 = np.fft.fft(w3)
u4 = np.fft.fft(w4)

re_spectrum = np.concatenate([u1, u2, u3, u4], axis=0)
re_spectrum = np.concatenate([re_spectrum, re_spectrum[::-1]], axis=0)
output = np.fft.ifft(re_spectrum)


# apply low pass filter
low_pass= [0.002898163, -0.009972252, -0.001920936, 0.03596853, -0.01611869,  -0.09530234, 0.1067987, 0.4773469, 0.4773469, 0.1067987,  -0.09530234, -0.01611869, 0.03596853,  -0.001920936, -0.009972252, 0.002898163]

high_pass= [0.002898163, -0.009972252, -0.001920936, 0.03596853, -0.01611869,  -0.09530234, 0.1067987, 0.4773469, 0.4773469, 0.1067987,  -0.09530234, -0.01611869, 0.03596853,  -0.001920936, -0.009972252, 0.002898163]

ll_data = np.convolve( data, low_pass)


plt.figure(2)
plt.plot(u2)
plt.figure(3)
plt.plot(output)
plt.show()
'''

