#include <iostream>
#include "sim_utils.h"
#include "sim_phys.h"
#include <cmath>
#include <omp.h>
int main(){
  //OPENMP INITIALIZATION
  //const int NT = 8;

  printf("beginning of main\n");
  Magnet mag;
  mag.offset = 0;
  mag.fConst = 1;
  int magnet_count = 30;
  Magnet *all_mags = new Magnet[magnet_count];
  for (int i = 0; i < magnet_count; i++)
    {
      all_mags[i] = mag;
    }

  SystemDetails sd;
  sd.prop_rad = 0.7/2; //change here
  sd.motor_rad = .089 / 2;
  sd.I = 0.004064 * 2 + .845 * (.089/2) * (.089 / 2) /2 ;
  sd.magnet_range = M_PI / 3;
  sd.gap = 0.015;
  sd.magnets = all_mags;
  sd.duration = 30;
  sd.magnet_count = magnet_count;
  float rate1, t0, t1;
  //printf("about to find success rate\n");
  
  t0 = omp_get_wtime();
  rate1 = find_success_rate(60,sd);
  t1 = omp_get_wtime();
  printf("Check it: %f. \n", rate1*100);
  printf("Took %f sec to check it and check it good.\n", t1-t0);

  /*
  printf("running test and writing to file\n");
  printf("matts change2\n");

  OutputStruct data = test(0,sd);

  char filename[] = {'d','a','t','a','1','.','c','s','v', '\0'};
  write_data(filename, data);
  printf("Wrote to data1.csv\n");
  */
  return 0;
}

