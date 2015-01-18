
from flask import Flask
import numpy as np
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
    # for i in range(100):
    #     for b in getSinusoid(1):
    #         sineWave[curBit] = b
    #         curBit += 1

    for bit in bitStream:
        newSinusoid = getSinusoid(bit)
        for b in newSinusoid:
            sineWave[curBit] = b
            curBit += 1

    # for i in range(100):
    #     for b in getSinusoid(1):
    #         sineWave[curBit] = b
    #         curBit += 1

    np.set_printoptions(threshold='nan')
    # print sineWave

    wav.write(os.path.dirname(__file__) + '/../static/audio/' + fName + '.wav', SAMPLE_RATE, sineWave)
    os.remove(os.path.dirname(__file__) + '/../static/tmp/' + fName + '.html.gz')
    return 0

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
    sineWave = np.append(sineWave, sineWave2)

    MEMO[bit] = sineWave
    return sineWave
