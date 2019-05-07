#include <cmath>
#include <iostream>
#include "sim_structs.h"
#include "sim_phys.h"

float find_success_rate(int n, SystemDetails sd)
{
  float max_succ_dist = (5/180) *M_PI * sd.prop_rad;
  float final_dist;
  int succ_cnt = 0;

  OutputStruct temp_data;

  for(int i = 0; i<n; i++)
  {
      temp_data = test(i*2*M_PI/n, sd);
      final_dist = temp_data.all_distance[temp_data.length-1];
      if(fabs(final_dist)<max_succ_dist)
      {
          succ_cnt++;
      }
  }

  return (float) succ_cnt/n;
}
