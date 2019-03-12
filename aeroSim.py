import math
from simTest import rtest, distance

def aero_test(theta):
    r=1

    prop_mass = 1
    prop_length = .762
    I_prop = prop_mass * prop_length ** 2 / 12

    # rotating part of the motor casing (mainly magnets)
    casing_mass = 1
    casing_outer_r = .2
    casing_inner_r = .1
    I_casing = (casing_inner_r + casing_outer_r)**2 / 2

    I = I_prop + I_casing 

    k = 1


    max_iter = 50000
    dt = .00005
    avel = 30
    
    all_theta = [theta]
    all_avel = [avel]
    all_dv = [0]

    # aero drag
    air_density = 1.225
    v = 26.8
    A = 6.4 * 100**-2
    Cd_front = .01
    Cd_back = .34

    for i in range(1,max_iter):
        #Friction

        # we need a new method for friction - this way increases the amount of friction when time step is decreased
        #avel = avel * .997
        # quick adjustment so time scaling is less with decreased time scale
        avel = avel - avel * (1-.997) * (dt/.001)

        #Ratchet Force

        #Aero Torque = force_back * half length of prop - force_front * half length of prop
        # Cd is adjusted for angle with the cos 
        aero_torque = (air_density * v**2 * A / 2) * (Cd_back - Cd_front) * math.fabs(math.cos(theta)) * prop_length /4

        # net torque 
        torque = aero_torque

        # just to work with rtest
        all_dv.append(1)

        #Add Changes
        dv = torque * dt / I
        avel = avel + dv
        theta = theta + avel * dt

        #reset theta to within 2pi range
        if (theta >= 2 * math.pi):
            theta = theta - (2 * math.pi)
        if (theta < 0):
            theta += 2 * math.pi

        all_theta.append(theta)
        all_avel.append(avel)

    all_t = [i * dt for i in range(max_iter)]
    all_distance = [distance(i,r) for i in all_theta]
    return {"time" : all_t, "theta" : all_theta, "avel" : all_avel,
            "distance" : all_distance, "dv" : all_dv}
        
rtest(aero_test)
