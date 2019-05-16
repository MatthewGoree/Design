#!/bin/sh
echo making project..
make

times=()
threads=()
for i in {1..24}
do 
  ibrun -np "$i" numactl --preferred=0 ./a.out 4
  
done
#echo ${times[*]}
exit 0

