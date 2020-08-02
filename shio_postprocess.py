# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import ctypes
import scipy.io.wavfile as wavf

def main():
    np.set_printoptions(threshold=sys.maxsize)
    
    # Directories
    curr_directory = os.getcwd()
    log_directory = curr_directory + "/../shio-logs"
    file_path = log_directory + "/shio_mic_3_41_48 PM.txt"
    mic_sample = np.array([]).astype('int16')
    
    # Sampling Parameters
    fs = 50000
    
    if not os.path.isfile(file_path):
       print("File path {} does not exist. Exiting...".format(file_path))
       sys.exit()
       
    # Parse PCM mic data
    with open(file_path) as fp:
       line = fp.readline()
       line = line.strip()
       while line:
           temp = np.flip(line.split(" "))
           si = iter(temp)
           pair_iter = (c+next(si, '') for c in si)
           samples = [int(s, 16) for s in list(pair_iter)]
           
#           temp = line.split(" ")
#           samples = [int(x+y, 16) for x, y in zip(temp[0::2], temp[1::2])]
           for sample in samples:
               signed_sample = ctypes.c_int16(sample).value
               mic_sample = np.append(mic_sample, signed_sample)
               
           line = fp.readline()
           line = line.strip()
    
#    mic_sample = mic_sample.astype('int16')
    print(mic_sample)
    
    # Plot PCM mic data
    plt.figure(0)
    x = np.arange(0,len(mic_sample),1)   # x axis data
    y = mic_sample                      # y axis data
    plt.stem(x,y, use_line_collection='true')
    plt.title('mic_sample')           # set the title
    plt.xlabel('Sample')                     # set the x axis label
    plt.ylabel('Amplitude')                     # set the y axis label
    plt.xlim(0, len(mic_sample))        # set the x axis range
    plt.ylim(-5000, 5000)                     # set the y axis range
    plt.grid()                          # enable the grid 
    plt.show()
#    plt.savefig('shio_mic_plot.png')
#    plt.close()
    
    wav_file = "shio_mic_test.wav"
    wavf.write(wav_file, fs, mic_sample)
    
if __name__ == '__main__':
    main()