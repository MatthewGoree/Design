import math
import sys
sys.path.append('./simulation')
import sim_utils

motor_mass = .845 #kg
propeller_mass = .300 #kg
added_mass = .2 #weight of whatever we add to motor (kg)
m  = motor_mass + propeller_mass + added_mass
prop_length = .7 #meter
prop_rad = prop_length / 2
motor_rad = .089 / 2 #meters

systemDetails = {
    "motor_mass": .845,
    "propeller_mass": .3,
    "added_mass": .2,
    "prop_length": .7, # meters
    "motor_rad": .089/2,
    "prop_I": 0.004064 * 2,
    "magnet_range": math.pi/2,
    "gap": .015,
    "magnets": [(0, 13)], # about 5.2 lbs,
    "duration" : 400,
    "start_rpm": 360,
    "in_flight": False
}
systemDetails["prop_rad"] = systemDetails["prop_length"] / 2
systemDetails["motor_I"] = systemDetails["motor_mass"] * systemDetails["motor_rad"]**2 / 2
systemDetails["I"] =  systemDetails["motor_I"] + systemDetails["prop_I"]

sim_utils.torque_profile(systemDetails)
