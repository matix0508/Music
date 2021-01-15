#!/bin/bash
# zapisuje (lub zamienia) nagranie w formacie .wav
# do pliku file.wav, lokalnie

sec=$1
filename=$2
echo
echo recording ...
echo
arecord -D dmic_sv -c2 -r 48000 -f S32_LE -t wav -V mono -d $sec -q temp.wav
sox temp.wav $filename.wav remix 1
echo
echo new file is made
echo
