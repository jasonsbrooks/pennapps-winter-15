import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pylab as plt
import itertools
import minifier
import sys
import binascii
import gzip

SAMPLE_RATE = 44100.0

BASE_FREQUENCY = 2200.0
DELTA_FREQUENCY = 480.0
WINDOW_SIZE_0 = 26

MEMO = {}

#very bad need to remove

def encode(url, filename):
    # url = sys.argv[1]
    # filename = sys.argv[2]
    minifier.download(url, filename)
    f = open(filename)
    bitStream = bits(f.read())
    numOfBits = sum(1 for i in bitStream)
    sineWave = np.zeros(WINDOW_SIZE_0 * numOfBits * 2)
    
    f.close()
    f = open(filename)
    bitStream = bits(f.read())

    #bitList = []

    curBit = 0

    for bit in bitStream:
    #   bitList.append(str(bit))
        newSinusoid = getSinusoid(bit)
        for b in newSinusoid:
            sineWave[curBit] = b
            curBit += 1


    wav.write(filename + '.wav', SAMPLE_RATE, sineWave)


def decode(file):
    bitList = 0
    bitIndex = 7
    (rate, data) = wav.read(file)
    
    zeroCrosses = 0
    positive = True
    begIdx = 0
    relevantBit = True
    with open(file, mode = 'wb') as f:
        for i, bit in enumerate(data[1:]):
            idx = i + 1
            if bit >= 0 and not positive:
                zeroCrosses += 1
                
                positive = True
            elif bit < 0 and positive:
                zeroCrosses += 1
                positive = False

            if zeroCrosses >= 2:
                
                sinusoid = data[begIdx:idx]
                
                begIdx = idx
                frequency = SAMPLE_RATE/len(sinusoid)
                zeroCrosses = 0

                relevantBit = not relevantBit
                if relevantBit:
                    continue
                
                if frequency > BASE_FREQUENCY:
                    bitList |= (1 << bitIndex)
                bitIndex -= 1
                if bitIndex < 0:
                    f.write(chr(bitList))
                    bitIndex = 7
                    bitList = 0
    f.close()


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


if __name__ == '__main__':
    if sys.argv[1] == 'encode':
        encode('http://www.google.com', 'temp/google')
    else:
        decode('temp/google.wav')

