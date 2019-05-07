#include <cmath>
#include <fstream>

float find_success_rate(int n, SystemDetails sd)
{
    return 0;
  /*float max_succ_dist = (5*360) * 


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
  float Cd_back = .0626377;*/
}

void write_data(char *filename, OutputStruct data)
{
  
  ofstream outfile;
  outfile.open(filename);

  outfile << "time,theta,distance\n";

  for (int i = 0; i < data.length; i++)
    {
      outfile << data.all_t[i] << "," << data.all_theta << "," <<
        data.all_distance << "\n";      
    }
  outfile.close();
  
}
