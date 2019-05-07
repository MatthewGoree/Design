main: sim_phys.o sim_utils.o main.o
	g++ sim_phys.o sim_utils.o main.o

sim_phys.o: sim_utils.h sim_phys.h sim_phys.cpp 
	g++ -c sim_phys.cpp

sim_utils.o: sim_utils.cpp sim_phys.o sim_utils.cpp sim_phys.h
	g++ -c sim_utils.cpp

main.o: sim_utils.o main.cpp
	g++ -c sim_utils.o main.cpp