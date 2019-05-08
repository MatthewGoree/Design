#include <iostream>
#include "sim_utils.h"
#include "sim_phys.h"
#include <cmath>

int main(){
  printf("beginning of main\n");
  Magnet mag;
  mag.offset = 0;
  mag.fConst = 13;
  Magnet *all_mags = new Magnet[1];
  all_mags[0] = mag;
  SystemDetails sd;
  sd.prop_rad = 0.7/2; //change here
  sd.motor_rad = .089 / 2;
  sd.I = 0.004064 * 2 + .845 * (.089/2) * (.089 / 2) /2 ;
  sd.magnet_range = M_PI / 3;
  sd.gap = 0.015;
  sd.magnets = all_mags;
  sd.duration = 30;
  float rate1;
  //printf("about to find success rate\n");
  rate1 = find_success_rate(360,sd);
  printf("Check it: %f\n", rate1*100);

  printf("running test and writing to file\n");

  OutputStruct data = test(0,sd);
  char filename[] = {'d','a','t','a','1','.','c','s','v', '\0'};
  write_data(filename, data);
  printf("Wrote to data1.csv\n");
  return 0;
}

