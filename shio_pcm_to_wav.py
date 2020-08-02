# -*- coding: utf-8 -*-
import sys
import wave

for arg in sys.argv[1:]:
    with open(arg, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
    with wave.open(arg+'.wav', 'wb') as wavfile:
        wavfile.setparams((1, 2, 50000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)