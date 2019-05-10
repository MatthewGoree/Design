#include <iostream>
#include "sim_utils.h"
#include "sim_phys.h"
#include <cmath>
#include <ctime>

int main(){
  // this is serial 
  printf("beginning of main\n");
  Magnet mag;
  mag.offset = 0;
  mag.fConst = 1;
  int magnet_count = 30;
  Magnet *all_mags = new Magnet[magnet_count];
  for(int i=0; i<magnet_count; i++) all_mags[i]=mag;
  SystemDetails sd;
  sd.prop_rad = 0.7/2; //change here
  sd.motor_rad = .089 / 2;
  sd.I = 0.004064 * 2 + .845 * (.089/2) * (.089 / 2) /2 ;
  sd.magnet_range = M_PI / 3;
  sd.gap = 0.015;
  sd.magnets = all_mags;
  sd.duration = 30;
  sd.magnet_count = magnet_count;
  float rate1;
  //printf("about to find success rate\n");
  

  clock_t t0 = clock();
  rate1 = find_success_rate(30,sd);
  clock_t t1 = clock();
  printf("Check it: %f\n", rate1*100);
  printf("finished in %f seconds\n", ((double) t1-t0)/CLOCKS_PER_SEC);

  //printf("running test and writing to file\n");
  //printf("matts change2\n");

return 0;
}

