main: sim_phys.o sim_utils.o main.o
	g++ -g sim_phys.o sim_utils.o main.o

sim_phys.o: sim_utils.h sim_phys.h sim_phys.cpp 
	g++ -c -g sim_phys.cpp

sim_utils.o: sim_utils.cpp sim_phys.o sim_utils.cpp sim_phys.h
	g++ -c -g sim_utils.cpp

main.o: sim_utils.o main.cpp
	g++ -c -g sim_utils.o main.cpp