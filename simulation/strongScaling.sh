#!/bin/sh
echo making project..
make

times=()
threads=()
for i in {1..48}
do 
  printf "$i, "
  ./a.out "$i"
  
done
#echo ${times[*]}
exit 0

