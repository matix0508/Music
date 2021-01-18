#!/bin/bash

touch freq
> freq

./record.sh 1 output
./find_freq.py output.wav
