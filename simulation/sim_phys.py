import math
import numpy as np

def distance(theta, radius):
    deg = theta * 180 / math.pi
    if (deg <= 90):
        return theta * radius
    if (deg > 270):
        return (theta - 2 * math.pi) * radius
    if (deg > 90) and (deg <= 180):
        return (math.pi - theta) * radius
    if (deg > 180) and (deg <= 270):
        return (math.pi - theta) * radius
    else:
        print(deg)

def sas_solver(theta, r, gap):
    b = r + gap
    c = r
    dist = math.sqrt(b**2 + c**2 - 2*b*c*math.cos(theta))

    ratio = (r*(1-math.cos(theta)) + gap) / dist 
    # fix comp errors
    if 1 < ratio < 1.0000001:
        ratio = 1
    phi = math.asin( ratio )

    return dist, phi

def magnetForce(theta, magnets, magnet_range, r, gap):
    # assuming all magnets come in pairs 
    # magnet thetas should include the angle from 0 the first magnet is placed at 
    # magnet range is assumed to be the same for all 

    # the sum of magnet forces init at 0 (will be returned)
    f_sum = 0

    #Magnet Force
    for magnet in magnets:

        magnet_offset = magnet[0]
        f_const = magnet[1]

        f_const = f_const * gap**2 # f const that is entered is actually the pulling force

        # get theta value relative to the magnet (original should not have theta change)
        rel_theta = theta - magnet_offset

        # make sure the relative angle is between 0 and 2*pi 
        if rel_theta < 0:
            rel_theta += 2*math.pi 
        if (rel_theta >= 2 * math.pi):
            rel_theta = rel_theta % (2*math.pi)
    
        # sas solver needs everything between 0 and pi 
        if rel_theta < math.pi / 2: # pull 
            dist, phi = sas_solver(rel_theta, r, gap)
        elif rel_theta > math.pi/2 and rel_theta <= math.pi: # push 
            dist, phi = sas_solver(math.pi - rel_theta, r, gap)
        elif rel_theta > math.pi and rel_theta <= 3*math.pi /2: # pull
            dist, phi = sas_solver(rel_theta - math.pi, r, gap)
        else: # push
            dist, phi = sas_solver(2*math.pi - rel_theta, r, gap)

        # magnetic force 
        if (rel_theta < magnet_range) or ((rel_theta < math.pi + magnet_range) and (rel_theta > math.pi)):
            f_sum += -1 * math.fabs( f_const * math.cos(phi) / (dist**2))

        elif (rel_theta > 2*math.pi - magnet_range) or ((rel_theta < math.pi) and rel_theta > math.pi - magnet_range):
            f_sum += math.fabs( f_const * math.cos(phi) / (dist**2) )

    return f_sum

def make_cont_magnet(mag_range, drange, force):
    magnets = []
    num_mags = round(mag_range/drange)
    # trigger if even
    if not num_mags % 2:
        num_mags += 1 

    max_force = force/mag_range * drange

    magnets = [(0,max_force)]
    for i in range(1, num_mags):
        magnets.append( (i*drange * (math.pi/180), max_force - max_force*i*drange/mag_range ) )
        magnets.insert(0, (-i*drange * (math.pi/180), max_force - max_force*i*drange/mag_range ) )

    return magnets 

def test(theta, systemDetails):
    #performs a sim with given starting angle
    prop_rad = systemDetails["prop_rad"]
    motor_rad = systemDetails["motor_rad"]
    I = systemDetails["I"]
    magnet_range = systemDetails["magnet_range"]
    gap  = systemDetails["gap"]
    magnets = systemDetails["magnets"]

    dt = .0005
    max_iter = math.floor(30/dt)

    avel = 360 * math.pi/30 # 360 rpm to rad/sec


    all_theta = [theta]
    all_avel = [avel]
    all_dv = [0]
    all_f = [0]
    
    # aero drag values
    air_density = 1.225
    v = 26.8
    A = 6.4 * 100**-2
    Cd_front = .01
    Cd_back = .34

    LINEAR_FINISH = True
    
    for i in range(1,max_iter):

        #Friction
        if LINEAR_FINISH:
            if avel > 30:
                avel = avel * .99955
            elif (avel > 0.0001):
                avel = avel - 12.8 * dt
            elif (avel < 0 and avel>-30):
                avel = avel + 12.8 * dt
        else:
            avel = avel * .99955

        # this f is now the sum of forces 
        f1 = magnetForce(theta, magnets, magnet_range, motor_rad, gap)

        #f2 = magnetForce(theta + math.pi/2, magnets, magnet_range, motor_rad, gap)
        # no negative needed for the new style 
        #f2 = -1 * magnetForce(theta + math.pi/2, magnets, magnet_range, motor_rad, gap)
        f = f1 #+ f2

        all_f.append(f)
        
        #Aero Torque = force_back * half length of prop - force_front * half length of prop
        # Cd is adjusted for angle with the cos 
        #aero_torque = (air_density * v**2 * A / 2) * (Cd_back - Cd_front) * math.fabs(math.cos(theta)) * prop_length /4

        torque = f * motor_rad #+ aero_torque
        dv = torque * dt / I

        all_dv.append(dv)
        avel = avel + dv
        theta = theta + avel * dt

        #reset theta to within 2pi range
        if (theta >= 2 * math.pi):
            theta = theta % (2*math.pi)
        if (theta < 0):
            theta += 2 * math.pi

        all_theta.append(theta)
        all_avel.append(avel)

    all_t = [i * dt for i in range(max_iter)]
    all_distance = [distance(i,prop_rad) for i in all_theta]

    return {"time" : all_t, "theta" : all_theta, "avel" : all_avel,
            "distance" : all_distance, "dv" : all_dv, "force": all_f}

def torque_over_cycle(systemDetails, polar=False):
    thetas = range(0,3610,1)
    torques = []
    motor_rad = systemDetails["motor_rad"]
    magnet_range = systemDetails["magnet_range"]
    gap  = systemDetails["gap"]
    magnets = systemDetails["magnets"]
    cartesian_x = []
    cartesian_y = []

    thetas = [ x / 10 for x in thetas]

    for theta in thetas:
        
        rad_theta = theta * math.pi / 180

        if (rad_theta >= 2 * math.pi):
            rad_theta = rad_theta % (2*math.pi)
        if (rad_theta < 0):
            rad_theta += 2 * math.pi

        torque = magnetForce(rad_theta, magnets, magnet_range, motor_rad, gap) * motor_rad
        torques.append(torque)

        x = math.cos(rad_theta) * math.fabs(torque)
        y = math.sin(rad_theta) * math.fabs(torque)

        cartesian_x.append(x)
        cartesian_y.append(y)

    if polar == True:
        return cartesian_x,cartesian_y
    else:
        return thetas, torques
