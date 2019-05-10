main: sim_phys.o sim_utils.o main.o
	icpc -g sim_phys.o sim_utils.o main.o -O2 -xcore-avx512 -qopenmp

sim_phys.o: sim_utils.h sim_phys.h sim_phys.cpp 
	icpc -c -g sim_phys.cpp -O2 -xcore-avx512 -qopenmp

sim_utils.o: sim_utils.cpp sim_phys.o sim_utils.cpp sim_phys.h
	icpc -c -g sim_utils.cpp -O2 -xcore-avx512 -qopenmp

main.o: sim_utils.o main.cpp
	icpc -c -g sim_utils.o main.cpp -O2 -xcore-avx512 -qopenmp
