#ifndef SIM_STRUCTS_H
#define SIM_STRUCTS_H

struct Magnet
{
  float offset;
  float fConst;
};

struct OutputStruct
{
  float *all_t;
  float *all_theta;
  float *all_distance;
};

struct SystemDetails
{
  float duration;
  int magnet_count;
  Magnet *magnets;
  float magnet_range;
  float motor_rad;
  float gap;
  float I;
  float prop_rad;
};

#endif
