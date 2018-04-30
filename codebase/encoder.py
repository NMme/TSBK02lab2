# This is a python script for encoding audio-signals
import numpy as np
from scipy.io import wavfile

fs, data = wavfile.read('../samples/heyhey01.wav')
data = np.ravel(data)
data = data[1::2]

# remove frequencies larger than sample-frequencies
spectrum = np.fft.fft(data)
spectrum = spectrum[:44100]
s1 = spectrum[:5512] 
s2 = spectrum[5512:11025] 
s3 = spectrum[11025:22050]
s4 = spectrum[22050:]

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
output = np.fft.ifft(re_spectrum)


# apply low pass filter
low_pass= [0.002898163, -0.009972252, -0.001920936, 0.03596853, -0.01611869,  -0.09530234, 0.1067987, 0.4773469, 0.4773469, 0.1067987,  -0.09530234, -0.01611869, 0.03596853,  -0.001920936, -0.009972252, 0.002898163]

high_pass= [0.002898163, -0.009972252, -0.001920936, 0.03596853, -0.01611869,  -0.09530234, 0.1067987, 0.4773469, 0.4773469, 0.1067987,  -0.09530234, -0.01611869, 0.03596853,  -0.001920936, -0.009972252, 0.002898163]

ll_data = np.convolve( data, low_pass)


import matplotlib.pyplot as plt
plt.figure(1)
plt.plot(data)
plt.figure(2)
plt.plot(output)
plt.show()
