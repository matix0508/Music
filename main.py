from numpy import array, diff, where, split
import sys
from numpy import arange
from scipy.fftpack import fft
import soundfile
import numpy, scipy
import copy
import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use('tkagg')

from math import log2, pow

A4 = 440
C0 = A4*pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def note(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)

def findPeak(magnitude_values, noise_level=2000):

    splitter = 0
    # zero out low values in the magnitude array to remove noise (if any)
    magnitude_values = numpy.asarray(magnitude_values)
    low_values_indices = magnitude_values < noise_level  # Where values are low
    magnitude_values[low_values_indices] = 0  # All low values will be zero out

    indices = []

    flag_start_looking = False

    both_ends_indices = []

    length = len(magnitude_values)
    for i in range(length):
        # print(magnitude_values[i])
        if magnitude_values[i] != splitter:
            if not flag_start_looking:
                flag_start_looking = True
                both_ends_indices = [0, 0]
                both_ends_indices[0] = i
        else:
            if flag_start_looking:
                flag_start_looking = False
                both_ends_indices[1] = i
                # add both_ends_indices in to indices
                indices.append(both_ends_indices)

    return indices

def extractFrequency(indices, freq_threshold=1):

    extracted_freqs = []

    for index in indices:
        freqs_range = freq_bins[index[0]: index[1]]
        avg_freq = round(numpy.average(freqs_range))

        if avg_freq not in extracted_freqs:
            extracted_freqs.append(avg_freq)

    # group extracted frequency by nearby=freq_threshold (tolerate gaps=freq_threshold)
    group_similar_values = split(extracted_freqs, where(diff(extracted_freqs) > freq_threshold)[0]+1 )

    # calculate the average of similar value
    extracted_freqs = []
    for group in group_similar_values:
        extracted_freqs.append(round(numpy.average(group)))

    print("freq_components", extracted_freqs)
    return extracted_freqs

if __name__ == '__main__':
    # print("exe")

    file_path = sys.argv[1]
    # print('Open audio file path:', file_path)

    audio_samples, sample_rate  = soundfile.read(file_path, dtype='int16')
    number_samples = len(audio_samples)
    # print('Audio Samples: ', audio_samples)
    # print('Number of Sample', number_samples)
    # print('Sample Rate: ', sample_rate)

    # duration of the audio file
    duration = round(number_samples/sample_rate, 2)
    # print('Audio Duration: {0}s'.format(duration))

    # list of possible frequencies bins
    freq_bins = arange(number_samples) * sample_rate/number_samples
    # print('Frequency Length: ', len(freq_bins))
    # print('Frequency bins: ', freq_bins)

#     # FFT calculation
    fft_data = fft(audio_samples)
    # print('FFT Length: ', len(fft_data))
    # print('FFT data: ', fft_data)

    freq_bins = freq_bins[range(number_samples//2)]
    normalization_data = fft_data/number_samples
    magnitude_values = normalization_data[range(len(fft_data)//2)]
    magnitude_values = numpy.abs(magnitude_values)

    indices = findPeak(magnitude_values=magnitude_values, noise_level=100)
    frequencies = extractFrequency(indices=indices)
    # print("frequencies:", frequencies)

    x_asis_data = freq_bins
    y_asis_data = magnitude_values
    print(len(magnitude_values))
    print(magnitude_values[1000])
    magnitude_values[freq_bins<20] = 0
    print(freq_bins[magnitude_values.argmax()])
