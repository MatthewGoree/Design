#ifndef SIM_STRUCTS_H
#define SIM_STRUCTS_H

struct Magnet
{
  float offset;
  float fConst;
};

Magnet createMagnet(float offset, float fConst)
{
  Magnet magnet;
  magnet.offset = offset;
  magnet.fConst = fConst;
  return magnet;
};

struct OutputStruct
{
  float *all_t;
  float *all_theta;
  float *all_distance;
  int length;
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
