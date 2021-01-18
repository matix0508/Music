#!/bin/bash
n=$1
touch freq
> freq
touch current

for (( i=1; i<=$n; i++ ))
do
  echo '1'
  > current

  ./record.sh 1 output
  echo 'recorded'
  ./find_freq.py output.wav
  echo 'found'
  ./color.py $(<current)
  echo 'color'
done

echo 'registered frequencies: '
cat freq
