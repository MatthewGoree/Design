#ifndef SIM_UTILS_H
#define SIM_UTILS_H

otest test(float theta, SystemDetails sd)
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
}







#endif