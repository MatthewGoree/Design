#ifndef SIM_UTILS_H
#define SIM_UTILS_H

struct Magnet
{
  float offset;
  float fConst;
};

Magnet createMagnet(float offset, float fConst);

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

float find_success_rate(int n, SystemDetails sd);
void write_data(char *filename, OutputStruct data);
void make_cont_magnet(float mag_range, float drange, float force, Magnet *magnets);
void magnum(int total_mags, float mag_range, float max_force, SystemDetails &sd);

#endif
