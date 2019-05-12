#include <iostream>
#include "sim_utils.h"
#include "sim_phys.h"
#include <cmath>
#include <omp.h>
#include <mpi.h>
int main(int argc, char **argv){
  //OPENMP INITIALIZATION
  //const int NT = 8;
 //fdsfds 
  int ierr;
  ierr = MPI_Init(&argc, &argv);
  int world_size;
  ierr = MPI_Comm_size(MPI_COMM_WORLD, &world_size);
  int world_rank;
  ierr = MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);


  printf("beginning of main\n");
  Magnet mag;
  mag.offset = 0;
  mag.fConst = 1;
  int magnet_count = 360;
  /*Magnet *all_mags = new Magnet[magnet_count];
  for (int i = 0; i < magnet_count; i++)
    {
      all_mags[i] = mag;
    }
  */

  SystemDetails sd;
  // number of magnets, angle you want to spread over (on one side), total pull force 
  magnum(7, 30, 12, sd);  

  sd.prop_rad = 0.7/2; //change here
  sd.motor_rad = .089 / 2;
  sd.I = 0.004064 * 2 + .845 * (.089/2) * (.089 / 2) /2 ;
  sd.magnet_range = M_PI / 3;
  sd.gap = 0.015;
  //sd.magnets = all_mags;
  sd.duration = 30;
  //sd.magnet_count = magnet_count;
  float rate1;
  double t0, t1, netT;
  
  t0 = omp_get_wtime();

  rate1 = find_success_rate(60,sd);
  t1 = omp_get_wtime();
  netT = t1-t0;
  if (world_rank == 0){
  printf("Check it: %f. \n", rate1*100);
  printf("Took %f sec to check it and check it good.\n", netT);
  }
  
  ierr = MPI_Finalize();

  return 0;
}

