#!/bin/bash
n=$1
touch freq
> freq
# touch current

for (( i=1; i<=$n; i++ ))
do
  # > current
  ./record.sh 1 output
  ./find_freq.py output.wav
  # ./color.py $(<current)
done

echo 'registered frequencies: '
cat freq
