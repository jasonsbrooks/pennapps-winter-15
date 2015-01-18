
from flask import Flask
import numpy as np
import scipy.fftpack as fft
import scipy.io.wavfile as wav
import matplotlib.pylab as plt
import itertools
import minifier
import sys
import binascii
import gzip
import hashlib
from bs4 import BeautifulSoup
import requests
import re
import os.path
import html2text
import markdown2
import pdb
import urllib2

SAMPLE_RATE = 44100.0

BASE_FREQUENCY = 2200.0
DELTA_FREQUENCY = 480.0
WINDOW_SIZE_0 = 26

MEMO = {}

def encode(url):
    fName = hashlib.sha224(url).hexdigest()
    zipLoc = download(url, fName)
    f = open(os.path.dirname(__file__) + '/' + zipLoc)
    bitStream = bits(f.read())
    numOfBits = sum(1 for i in bitStream) + 5200
    sineWave = np.zeros(WINDOW_SIZE_0 * numOfBits * 2)
    
    f.seek(0)
    bitStream = bits(f.read())


    curBit = 0
    for i in range(200):
        for b in getSinusoid(0):
            sineWave[curBit] = b
            curBit += 1

    for bit in bitStream:
        newSinusoid = getSinusoid(bit)
        for b in newSinusoid:
            sineWave[curBit] = b
            curBit += 1

    for i in range(200):
        for b in getSinusoid(0):
            sineWave[curBit] = b
            curBit += 1

    intSineWave = np.int16(sineWave * 32767)
    wav.write(os.path.dirname(__file__) + '/../static/audio/' + fName + '.wav', SAMPLE_RATE, intSineWave)
    os.remove(os.path.dirname(__file__) + '/../static/tmp/' + fName + '.html.gz')
    return "http://browser.ngrok.com/static/audio/%s.wav" %(fName)

def download(url, filename):
    response = requests.get(url)
    response.encoding = 'ascii'
    html_doc = response.text
    # print html_doc
    soup = BeautifulSoup(html_doc)

    #remove unnecessary
    elements = soup.findAll(['img', 'link', 'meta', 'style', 'script'])
    [element.extract() for element in elements]

    #remove attributes
    soup = removeAttrs(soup)

    for span in soup.findAll('span'):
        span.parent.insert(span.parent.index(span)+1, span.text)
        span.extract()

    #strip whitespace
    htmlString = str(soup)
    htmlString = removeWhitespace(htmlString)
    htmlString = html2text.html2text(unicode(htmlString, errors='ignore'))
    htmlString = markdown2.markdown(htmlString)
    return compress(htmlString, filename)

def compress(string, filename):
    fName = '../static/tmp/' + filename + '.html.gz'
    f = gzip.open(os.path.dirname(__file__) + '/../static/tmp/' + filename + '.html.gz', 'wb')
    f.write(string.decode('utf-8'))
    f.close()
    return fName

def removeWhitespace(string):
    whitespace = ['\t', '\n', '\r']
    for character in whitespace:
        string = string.replace(character, '')

    return string

def removeAttrs(soup):
    for tag in soup.findAll(True): 
        tag.attrs = {}
    return soup

def bits(f):
    bytes = (ord(b) for b in f)
    for b in bytes:
        for i in reversed(range(8)):
            yield (b >> i) & 1


# 10 or 01
def getSinusoid(bit):
    if bit in MEMO:
        return MEMO[bit]
    frequency = BASE_FREQUENCY

    if bit == 1:
        frequency += DELTA_FREQUENCY
    else:
        frequency -= DELTA_FREQUENCY
    
    period = 1.0/frequency
    windowSize = SAMPLE_RATE * period
    t = np.linspace(0, period, windowSize)

    sineWave = np.sin(2*np.pi*frequency*t)

    if bit == 0:
        frequency += DELTA_FREQUENCY
    else:
        frequency -= DELTA_FREQUENCY
    period = 1/frequency
    windowSize = SAMPLE_RATE * period
    t = np.linspace(0, period, windowSize)
    sineWave2 = np.sin(2*np.pi*frequency*t)
    sineWave = np.append(sineWave[:-1], sineWave2[:-1])

    MEMO[bit] = sineWave

    return sineWave

def getWav(filename):
    newfile= filename.split('/')[-1]
    wavfile = urllib2.urlopen(filename)
    output = open(newfile, 'wb')
    output.write(wavfile.read())
    output.close()

    (sample_rate, data) = wav.read(newfile)
    bandlimit = sample_rate/7 #every 50 ms
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
        elif(((1600 < values[important_peaks[lcount]] < 1680) and (680 < values[important_peaks[l2count]] < 710)) or \
                ((1600 < values[important_peaks[l2count]] < 1680) and (690 < values[important_peaks[lcount]] < 710))):
            print "Tone is: A"
        elif(((1600 < values[important_peaks[lcount]] < 1680) and (750 < values[important_peaks[l2count]] < 790)) or \
                ((1600 < values[important_peaks[l2count]] < 1680) and (750 < values[important_peaks[lcount]] < 790))):
            print "Tone is: B"
        elif(((1590 < values[important_peaks[lcount]] < 1680) and (830 < values[important_peaks[l2count]] < 880)) or \
                ((1600 < values[important_peaks[l2count]] < 1680) and (830 < values[important_peaks[lcount]] < 880))):
            print "Tone is: C"
        elif(((1600 < values[important_peaks[lcount]] < 1680) and (900 < values[important_peaks[l2count]] < 990)) or \
                ((1600 < values[important_peaks[l2count]] < 1680) and (900 < values[important_peaks[lcount]] < 990))):
            print "Tone is: D"

        j+=bandlimit
