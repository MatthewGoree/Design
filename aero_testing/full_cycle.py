import math
import matplotlib.pyplot as plt


air_density = 1.225
v = 26.8
A = .03726039
Cd_front = .0651667
Cd_back = .0626377
prop_rad = .7/2

theta_degs = range(0,361,1)
theta_rads = [deg*math.pi/180 for deg in theta_degs]

torques = []

for theta in theta_rads:
    front_force = air_density * Cd_front * A * (v)**2 / 2
    back_force = air_density * Cd_back * A * (v)**2 / 2
    total_aero_force = (back_force - front_force) * math.cos(theta) # adjusting for cd changes with rotating
    aero_torque = total_aero_force * math.cos(theta) * prop_rad /2 # only want force tangent to prop
    torques.append(math.fabs(aero_torque))

plt.plot(theta_degs,torques)
plt.xlabel('Leading Propeller Angle [Degrees]')
plt.ylabel('Aerodynamic Torque [N]')
plt.title('Aerodynamic Torque During a Full Cycle', fontsize=20)
plt.show()