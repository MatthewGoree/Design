import math
import sys
sys.path.append('./simulation')
import sim_utils
import matplotlib.pyplot as plt

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
    "magnets": [(0,3)],
    "duration" : 20,
    "start_rpm": 360,
    "in_flight": False,
    "testing": False
}

#print(sim_utils.make_cont_magnet(12,6,2.2))

systemDetails["prop_rad"] = systemDetails["prop_length"] / 2
systemDetails["motor_I"] = systemDetails["motor_mass"] * systemDetails["motor_rad"]**2 / 2
systemDetails["I"] =  systemDetails["motor_I"] + systemDetails["prop_I"]

#sim_utils.torque_profile(systemDetails, 90, 360+90)
#sim_utils.plot_failzone(systemDetails,60)

#print(sim_utils.make_cont_magnet(30,15,12))

#systemDetails["magnets"] = sim_utils.make_cont_magnet(15,5,2.5)
#sim_utils.torque_profile(systemDetails, 90, 360+90)
#sim_utils.plot_failzone(systemDetails,60)
#sim_utils.rtest(systemDetails)
sim_utils.failzone_per_pull(systemDetails)

#sim_utils.succ_per_pull_aero(systemDetails, endForce=75, n=60)
