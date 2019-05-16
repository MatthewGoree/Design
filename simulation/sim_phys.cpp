#include <cmath>
#include <iostream>
#include "sim_utils.h"
#include "sim_phys.h"
#include <omp.h>

using namespace std;
const int MAX_THREADS = 4;

float distance(float theta, float radius);
void sas_solver(float theta, float r, float gap, float &dist, float &phi);
float magnetForce(float theta, Magnet *magnets, float magnet_range, float r, float gap, int magnet_count, int thread_count);
OutputStruct test(float theta, SystemDetails systemDetails);
float distance(float theta, float radius);

OutputStruct test(float theta, SystemDetails sd)
{
  float dt = 0.0005;
  int max_iter = floor(sd.duration / dt);
  float avel = 360 * M_PI / 30;
  float *all_theta = new float[max_iter];
  float *all_distance = new float[max_iter];
  float *all_t = new float[max_iter];
  float *all_avel = new float[max_iter];
  float *all_f = new float[max_iter];
  float *all_torque = new float[max_iter];
  float torque, dv;
  // aero drag values
  float air_density = 1.225;
  float v = 26.8;
  float A = .03726039;
  float Cd_front = 0.0651667;
  float Cd_back = .0626377;

  all_theta[0] = theta;
  all_t[0] = 0;
  all_distance[0] = distance(theta, sd.prop_rad);

  double t0,t1,total_force_time;
  t0 = omp_get_wtime();
  bool LINEAR_FINISH = true;
  float f1;
  total_force_time = 0;
  for (int i = 1; i < max_iter; i++)
    {

      //Friction
      if (LINEAR_FINISH == true)
        {
          if (avel > 30) avel = avel * .99955;
          else if (avel > 0.0001) avel = avel - 12.8 * dt;
          else if (avel < 0 && avel > -30) avel = avel + 12.8 * dt;
        }
      else avel = avel * .99955;
      
      //t0 = omp_get_wtime();
      f1 = magnetForce(theta, sd.magnets, sd.magnet_range, sd.motor_rad, sd.gap, sd.magnet_count, sd.thread_count);
      //t1 = omp_get_wtime();
      //printf("%f\n", (t1 - t0));
      //total_force_time += (t1 - t0);
     
      all_f[i] = f1;
      torque = f1 * sd.motor_rad;
      //if (i==1) printf("NEW TEST\n");
      //if (i<10) printf("magent force: %f \n", f1);

      // aero force section 
      float front_force, back_force, total_aero_force, aero_torque;

      front_force = air_density * Cd_front * A * pow(v+avel*sd.prop_rad/2 * cos(theta) , 2) / 2;
      back_force = air_density * Cd_back * A * pow(v-avel*sd.prop_rad/2 * cos(theta) , 2) / 2;

      total_aero_force = (back_force - front_force) * cos(theta);
      aero_torque = total_aero_force * cos(theta) * sd.prop_rad / 2;
      
      torque += aero_torque;
      

      all_torque[i] = torque;

      dv = torque * dt / sd.I;
      avel += dv;
      theta = theta + avel * dt;

      //reset theta to between 0 and 2pi
      //if (i<1000) printf("theta: %f \n", theta);

      if (theta >= 2 * M_PI) theta = fmod(theta, 2*M_PI);
      if (theta < 0) theta += 2 * M_PI;

      all_theta[i] = theta;
      all_avel[i] = avel;
      all_t[i] = i * dt;
      all_distance[i] = distance(theta, sd.prop_rad);
    }

  OutputStruct data;
  data.length = max_iter;
  data.all_theta = all_theta;
  data.all_t = all_t;
  data.all_distance = all_distance;
  
  t1 = omp_get_wtime();
  total_force_time += (t1 - t0);
  printf("%.9lf\n", total_force_time);
  return data;

}

float magnetForce(float theta, Magnet *magnets, float magnet_range, float r, float gap, int magnetCount, int thread_count)
{
  float magnet_offset, f_const, n_const, rel_theta, dist, phi, f_sum = 0;
  
  
#pragma omp parallel for reduction(+:f_sum) num_threads(thread_count) private(magnet_offset,rel_theta, f_const, n_const, dist, phi)
  for (int i = 0; i < magnetCount; i++)
    {
      magnet_offset = magnets[i].offset;
      f_const = magnets[i].fConst;
      n_const = f_const/pow(gap,-3.882) * 7.2;

      rel_theta = theta - magnet_offset;

      if (rel_theta < 0) rel_theta += 2 * M_PI;
      if (rel_theta >= 2 * M_PI) rel_theta = fmod(rel_theta, 2*M_PI); 

      if (rel_theta < M_PI / 2) sas_solver(rel_theta, r, gap, dist, phi);
      else if (rel_theta > M_PI / 2 && rel_theta <= M_PI)
        sas_solver(M_PI - rel_theta, r, gap, dist, phi);
      else if (rel_theta > M_PI && rel_theta <= 3 * M_PI / 2)
        sas_solver(rel_theta - M_PI, r, gap, dist, phi);
      else sas_solver(2 * M_PI - rel_theta, r, gap, dist, phi);

      if ((rel_theta < magnet_range) || (rel_theta < M_PI + magnet_range && rel_theta > M_PI))
        f_sum += -1 * fabs(n_const * cos(phi) * pow(dist, -3.882));
      else if ((rel_theta > 2 * M_PI - magnet_range) || (rel_theta < M_PI && rel_theta > M_PI - magnet_range))
        f_sum += fabs(n_const * cos(phi) * pow(dist, -3.882));

    }


  return f_sum;
}


void sas_solver(float theta, float r, float gap, float &dist, float &phi)
{
  float b = r + gap;
  float c = r;
  dist = sqrt(b * b + c * c - 2 * b * c * cos(theta));

  float ratio = (r * (1 - cos(theta)) + gap) / dist;

  if ((1 < ratio) && ratio < 1.0000001) ratio = 1;

  phi = asin(ratio);
  phi = theta - phi;
}
float distance(float theta, float radius)
{
  float deg = theta * 180 / M_PI;
  if (deg <= 90) return theta * radius;
  if (deg > 270) return (theta - 2 * M_PI) * radius;
  if ((deg > 90) && (deg <= 180)) return (M_PI - theta) * radius;
  if ((deg > 180) && (deg <= 270)) return (M_PI - theta) * radius;
  else return -100000000000;
}


