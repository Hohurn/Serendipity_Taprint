import numpy as np
import matplotlib.pyplot as plt

Fs = 100
T = 1/Fs
end_time = 1
time = np.linspace(0, end_time, Fs)
amp = [2, 1, 0.5, 0.2]
freq = [10, 20, 30, 40]

signal_1 = amp[0]*np.sin(freq[0]*2*np.pi*time)
signal_2 = amp[1]*np.sin(freq[1]*2*np.pi*time)
signal_3 = amp[2]*np.sin(freq[2]*2*np.pi*time)
signal_4 = amp[3]*np.sin(freq[3]*2*np.pi*time)

signal = signal_1 + signal_2 + signal_3 + signal_4+4

plt.plot(time, signal)
plt.show()




s_fft = np.fft.fft(signal) # 추후 IFFT를 위해 abs를 취하지 않은 값을 저장한다.
amplitude = abs(s_fft)*(2/len(s_fft)) # 2/len(s)을 곱해줘서 원래의 amp를 구한다.
frequency = np.fft.fftfreq(len(s_fft), T)

print(frequency)

plt.xlim(-50, 50)
plt.stem(frequency[0:50], amplitude[0:50])
plt.grid(True)
plt.show()

t = amplitude[0:50]
max = 0
index = 0
for i in range(len(t)):
    if (max < t[i]):
        max = t[i]
        index = i

print([max, index])