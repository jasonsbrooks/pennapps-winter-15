import scipy.io.wavfile
import scipy.fftpack as fft
import matplotlib.pyplot as plt
import heapq
import numpy as np
from scipy.signal import argrelextrema
import hermes
from scipy import signal

def getWav(filename):
	(sample_rate, data) = scipy.io.wavfile.read(filename)
	bandlimit = sample_rate/10 #every 50 ms
	n = len(data)
	t = [x/float(sample_rate) for x in range(n)]
	j = 1
	#loop through band limited samples
	for i in range(bandlimit, len(data), bandlimit):
		if(i >= len(data)):
			i=len(data)-1
		frequencies = abs(scipy.fft(data[j:i]))
		values = [x*float(sample_rate/(bandlimit)) for x in range(bandlimit-1)]
		peaks = argrelextrema(frequencies, np.greater)
		# print peaks
		important_peaks = filter(lambda x:values[x]>500 and values[x]<1800,peaks[0])
		important = [frequencies[peak] for peak in important_peaks]
		# print important	
		largest, second_largest, lcount, l2count = 0,0,0,0
		for counter in range(len(important)):
			if(important[counter] > largest):
				second_largest = largest
				l2count = lcount
				largest = important[counter]
				lcount = counter
			elif(important[counter] > second_largest):
				second_largest = important[counter]
				l2count = counter
		if(((1190 < values[important_peaks[lcount]] < 1235) and (680 < values[important_peaks[l2count]] < 710)) or \
				((1190 < values[important_peaks[l2count]] < 1220) and (690 < values[important_peaks[lcount]] < 710))):
			print "Tone is: 1"
		elif(((1325< values[important_peaks[lcount]] < 1370) and (680 < values[important_peaks[l2count]] < 710)) or \
				((1325< values[important_peaks[l2count]] < 1370) and (690 < values[important_peaks[lcount]] < 710))):
			print "Tone is: 2"
		elif(((1440 < values[important_peaks[lcount]] < 1500) and (680 < values[important_peaks[l2count]] < 710)) or \
				((1440 < values[important_peaks[l2count]] < 1500) and (680 < values[important_peaks[lcount]] < 710))):
			print "Tone is: 3"
		elif(((1190 < values[important_peaks[lcount]] < 1235) and (750 < values[important_peaks[l2count]] < 790)) or \
				((1190 < values[important_peaks[l2count]] < 1235) and (750 < values[important_peaks[lcount]] < 790))):
			print "Tone is: 4"
		elif(((1325 < values[important_peaks[lcount]] <1370) and (750 < values[important_peaks[l2count]] < 790)) or \
				((1325 < values[important_peaks[l2count]] <1370) and (750 < values[important_peaks[lcount]] < 790))):
			print "Tone is: 5"
		elif(((1440 < values[important_peaks[lcount]] < 1500) and (750 < values[important_peaks[l2count]] < 790)) or \
				((1440 < values[important_peaks[l2count]] < 1500) and (750 < values[important_peaks[lcount]] < 790))):
			print "Tone is: 6"
		elif(((1190 < values[important_peaks[lcount]] < 1235) and (830 < values[important_peaks[l2count]] < 880)) or \
				((1190 < values[important_peaks[l2count]] < 1235) and (830 < values[important_peaks[lcount]] < 880))):
			print "Tone is: 7"
		elif(((1325< values[important_peaks[lcount]] < 1370) and (830 < values[important_peaks[l2count]] < 880)) or \
				((1325< values[important_peaks[l2count]] < 1370) and (830 < values[important_peaks[lcount]] < 880))):
			print "Tone is: 8"
		elif(((1440 < values[important_peaks[lcount]] < 1500) and (830 < values[important_peaks[l2count]] < 880)) or \
				((1440 < values[important_peaks[l2count]] < 1500) and (830 < values[important_peaks[lcount]] < 880))):
			print "Tone is: 9"
		elif(((1325 < values[important_peaks[lcount]] <1370) and (900 < values[important_peaks[l2count]] < 990)) or \
				((1325 < values[important_peaks[l2count]] <1370) and (900 < values[important_peaks[lcount]] < 990))):
			print "Tone is: 0"
		elif(((1190 < values[important_peaks[lcount]] < 1235) and (900 < values[important_peaks[l2count]] < 990)) or \
				((1190 < values[important_peaks[l2count]] < 1235) and (900 < values[important_peaks[lcount]] < 990))):
			print "Tone is: *"
		elif(((1440 < values[important_peaks[lcount]] < 1500) and (900 < values[important_peaks[l2count]] < 990)) or \
				((1440 < values[important_peaks[l2count]] < 1500) and (900 < values[important_peaks[lcount]] < 990))):
			print "Tone is: #"
		elif(((1590 < values[important_peaks[lcount]] < 1680) and (680 < values[important_peaks[l2count]] < 710)) or \
				((1590 < values[important_peaks[l2count]] < 1680) and (690 < values[important_peaks[lcount]] < 710))):
			print "Tone is: A"
		elif(((1590 < values[important_peaks[lcount]] < 1680) and (750 < values[important_peaks[l2count]] < 790)) or \
				((1590 < values[important_peaks[l2count]] < 1680) and (750 < values[important_peaks[lcount]] < 790))):
			print "Tone is: B"
		elif(((1590 < values[important_peaks[lcount]] < 1680) and (830 < values[important_peaks[l2count]] < 880)) or \
				((1590 < values[important_peaks[l2count]] < 1680) and (830 < values[important_peaks[lcount]] < 880))):
			print "Tone is: C"
		elif(((1590 < values[important_peaks[lcount]] < 1680) and (900 < values[important_peaks[l2count]] < 990)) or \
				((1590 < values[important_peaks[l2count]] < 1680) and (900 < values[important_peaks[lcount]] < 990))):
			print "Tone is: D"

		j+=bandlimit

getWav('audio_12345678987654321.wav')
