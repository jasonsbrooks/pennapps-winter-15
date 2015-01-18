import scipy.io.wavfile
import scipy.fftpack as fft
import matplotlib.pyplot as plt
import heapq
import numpy as np
from scipy.signal import argrelextrema
import hermes
from scipy import signal
import urllib2

def getWav(filename):
	newfile= filename.split('/')[-1]
	wavfile = urllib2.urlopen(filename)
	output = open(newfile, 'wb')
	output.write(wavfile.read())
	output.close()

	(sample_rate, data) = scipy.io.wavfile.read(newfile)
	bandlimit = sample_rate/7 #every 50 ms
	n = len(data)
	t = [x/float(sample_rate) for x in range(n)]
	j = 1
	bitList = 0
	hexvar = ""
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
	        # print "Tone is: 1"
	        hexvar = hexvar + hex(0)
	    elif(((1325< values[important_peaks[lcount]] < 1370) and (680 < values[important_peaks[l2count]] < 710)) or \
	            ((1325< values[important_peaks[l2count]] < 1370) and (690 < values[important_peaks[lcount]] < 710))):
	        # print "Tone is: 2"
	        hexvar = hexvar + hex(1)
	    elif(((1440 < values[important_peaks[lcount]] < 1500) and (680 < values[important_peaks[l2count]] < 710)) or \
	            ((1440 < values[important_peaks[l2count]] < 1500) and (680 < values[important_peaks[lcount]] < 710))):
	        # print "Tone is: 3"
	        hexvar = hexvar + hex(2)
	    elif(((1190 < values[important_peaks[lcount]] < 1235) and (750 < values[important_peaks[l2count]] < 790)) or \
	            ((1190 < values[important_peaks[l2count]] < 1235) and (750 < values[important_peaks[lcount]] < 790))):
	        # print "Tone is: 4"
	        hexvar = hexvar + hex(4)     
	    elif(((1325 < values[important_peaks[lcount]] <1370) and (750 < values[important_peaks[l2count]] < 790)) or \
	            ((1325 < values[important_peaks[l2count]] <1370) and (750 < values[important_peaks[lcount]] < 790))):
	        # print "Tone is: 5"
	        hexvar = hexvar + hex(5)            
	    elif(((1440 < values[important_peaks[lcount]] < 1500) and (750 < values[important_peaks[l2count]] < 790)) or \
	            ((1440 < values[important_peaks[l2count]] < 1500) and (750 < values[important_peaks[lcount]] < 790))):
	        # print "Tone is: 6"
	        hexvar = hexvar + hex(6)            
	    elif(((1190 < values[important_peaks[lcount]] < 1235) and (830 < values[important_peaks[l2count]] < 880)) or \
	            ((1190 < values[important_peaks[l2count]] < 1235) and (830 < values[important_peaks[lcount]] < 880))):
	        # print "Tone is: 7"
	        hexvar = hexvar + hex(8)            
	    elif(((1325< values[important_peaks[lcount]] < 1370) and (830 < values[important_peaks[l2count]] < 880)) or \
	            ((1325< values[important_peaks[l2count]] < 1370) and (830 < values[important_peaks[lcount]] < 880))):
	        # print "Tone is: 8"
	        hexvar = hexvar + hex(9)            
	    elif(((1440 < values[important_peaks[lcount]] < 1500) and (830 < values[important_peaks[l2count]] < 880)) or \
	            ((1440 < values[important_peaks[l2count]] < 1500) and (830 < values[important_peaks[lcount]] < 880))):
	        # print "Tone is: 9"
	        hexvar = hexvar + hex(10)
	    elif(((1325 < values[important_peaks[lcount]] <1370) and (900 < values[important_peaks[l2count]] < 990)) or \
	            ((1325 < values[important_peaks[l2count]] <1370) and (900 < values[important_peaks[lcount]] < 990))):
	        # print "Tone is: 0"
	        hexvar = hexvar + hex(13)            
	    elif(((1190 < values[important_peaks[lcount]] < 1235) and (900 < values[important_peaks[l2count]] < 990)) or \
	            ((1190 < values[important_peaks[l2count]] < 1235) and (900 < values[important_peaks[lcount]] < 990))):
	        # print "Tone is: *"
	        hexvar = hexvar + hex(12)           
	    elif(((1440 < values[important_peaks[lcount]] < 1500) and (900 < values[important_peaks[l2count]] < 990)) or \
	            ((1440 < values[important_peaks[l2count]] < 1500) and (900 < values[important_peaks[lcount]] < 990))):
	        # print "Tone is: #"
	        hexvar = hexvar + hex(14)
	    elif(((1600 < values[important_peaks[lcount]] < 1680) and (680 < values[important_peaks[l2count]] < 710)) or \
	            ((1600 < values[important_peaks[l2count]] < 1680) and (690 < values[important_peaks[lcount]] < 710))):
	        # print "Tone is: A"
	        hexvar = hexvar + hex(3)           
	    elif(((1600 < values[important_peaks[lcount]] < 1680) and (750 < values[important_peaks[l2count]] < 790)) or \
	            ((1600 < values[important_peaks[l2count]] < 1680) and (750 < values[important_peaks[lcount]] < 790))):
	        # print "Tone is: B"
	        hexvar = hexvar + hex(7)
	    elif(((1590 < values[important_peaks[lcount]] < 1680) and (830 < values[important_peaks[l2count]] < 880)) or \
	            ((1600 < values[important_peaks[l2count]] < 1680) and (830 < values[important_peaks[lcount]] < 880))):
	        # print "Tone is: C"
	        hexvar = hexvar + hex(11)
	    elif(((1600 < values[important_peaks[lcount]] < 1680) and (900 < values[important_peaks[l2count]] < 990)) or \
	            ((1600 < values[important_peaks[l2count]] < 1680) and (900 < values[important_peaks[lcount]] < 990))):
	        # print "Tone is: D"
	        hexvar = hexvar + hex(15)
	    j+=bandlimit
	return hexvar

getWav('http://dialabc.com/i/cache/dtmfgen/wavpcm8.100/12131415.wav')
