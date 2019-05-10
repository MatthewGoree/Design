main: sim_phys.o sim_utils.o main.o
	mpicc -g sim_phys.o sim_utils.o main.o -O2 -xcore-avx512 -qopenmp

sim_phys.o: sim_utils.h sim_phys.h sim_phys.cpp 
	mpicc -c -g sim_phys.cpp -O2 -xcore-avx512 -qopenmp

sim_utils.o: sim_utils.cpp sim_phys.o sim_utils.cpp sim_phys.h
	mpicc -c -g sim_utils.cpp -O2 -xcore-avx512 -qopenmp

main.o: sim_utils.o main.cpp
	mpicc -c -g sim_utils.o main.cpp -O2 -xcore-avx512 -qopenmp
