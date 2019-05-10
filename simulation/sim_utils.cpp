#include <cmath>
#include <fstream>
#include <iostream>
#include "sim_utils.h"
#include "sim_phys.h"
#include <mpi.h>
using namespace std;


float find_success_rate(int n, SystemDetails sd)
{

  int ierr, world_size, world_rank;
  ierr = MPI_Comm_size(MPI_COMM_WORLD, &world_size);
  ierr = MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

  //printf("in sim_utils, about to find succ rate\n");
  float max_succ_theta = (5.0/180) * M_PI;
  float final_theta;
  int succ_cnt = 0;
  int global_cnt = 0;

  OutputStruct temp_data;

  for(int i = world_rank; i<n; i += world_size)
  {
      //printf("RUN NUMBER: %d, theta = %f \n",i,i*2*M_PI/n);
      temp_data = test(i*2*M_PI/n, sd);
      final_theta = temp_data.all_theta[temp_data.length-1];
      if(fabs(final_theta)<max_succ_theta || fabs(final_theta-M_PI)<max_succ_theta || fabs(final_theta-2*M_PI) < max_succ_theta)
      {
          //printf("succ! final_theta: %f, max_theta: %f \n", final_theta, max_succ_theta);
          succ_cnt++;
          //printf("Success!\n");
      }
      //else printf("fail: final_theta: %f, max_theta: %f \n", final_theta, max_succ_theta);
  }
  ierr = MPI_Reduce(&succ_cnt, &global_cnt, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
  
  return (float) global_cnt / n;
  
}

void write_data(char *filename, OutputStruct data)
{
  
  ofstream outfile;
  outfile.open(filename);

  outfile << "time,theta,distance\n";

  for (int i = 0; i < data.length; i++)
    {
      outfile << data.all_t[i] << "," << data.all_theta[i] << "," <<
        data.all_distance[i] << "\n";      
    }
  outfile.close();
  
}

void make_cont_magnet(float mag_range, float drange, float force, Magnet *magnets)
{
  int num_mags = round(mag_range / drange);
  if (num_mags % 2 != 0) num_mags += 1;

  float max_force = force / mag_range * drange;

  magnets[0] = createMagnet(0, max_force);
  for (int i = 1; i <  num_mags; i++)
    {
      magnets[2 * i - 1] = createMagnet(i * drange * M_PI / 180, max_force - max_force * i * drange / mag_range);
      magnets[2 * i] = createMagnet(-1 * i * drange * M_PI / 180, max_force - max_force * i * drange / mag_range);
    }
}

Magnet createMagnet(float offset, float fConst)
{
  Magnet magnet;
  magnet.offset = offset;
  magnet.fConst = fConst;
  return magnet;
};


