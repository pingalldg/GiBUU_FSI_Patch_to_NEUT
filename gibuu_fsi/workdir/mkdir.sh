#!/bin/bash

start=$1
end=$2

for ((i=$start; i<=$end; i++))
do
  mkdir $i
  cp generate_inputfile.py $i/
  cd $i
  python3 generate_inputfile.py $i
  cd ../
done
