#include <iostream>
#include "sim_utils.h"
#include <cmath>

int main(){

  Magnet mag;
  mag.offset = 0;
  mag.fConst = 13;
  Magnet *all_mags = new Magnet[1];
  all_mags[0] = mag;
  SystemDetails sd;
  sd.prop_rad = 0.7;
  sd.motor_rad = .089 / 2;
  sd.I = 0.004064 * 2 + .845 * (.089/2) * (.089 / 2) /2 ;
  sd.magnet_range = M_PI / 3;
  sd.gap = 0.015;
  sd.magnets = all_mags;
  sd.duration = 40;
  float rate1;
  rate1 = find_success_rate(60,sd);
  printf("Check it: %f\n", rate1);
  return 0;
}

