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

    return dist, theta-phi

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
        n_const = f_const/(gap**-3.882) * 7.2
        f_const = f_const * gap**2 * 3.4# f const that is entered is actually the pulling force
        #f_const = 1.7 * f_const * gap**2 # f const that is entered is actually the pulling force

        # get theta value relative to the magnet (original should not have theta change)
        rel_theta = theta - magnet_offset

        # make sure the relative angle is between 0 and 2*pi 
        if rel_theta < 0:
            rel_theta += 2*math.pi 
        if (rel_theta >= 2 * math.pi):
            rel_theta = rel_theta % (2*math.pi)
    
        # sas solver needs everything between 0 and pi 
        if rel_theta < math.pi / 2: # pull 
            dist, gamma = sas_solver(rel_theta, r, gap)
        elif rel_theta > math.pi/2 and rel_theta <= math.pi: # push 
            dist, gamma = sas_solver(math.pi - rel_theta, r, gap)
        elif rel_theta > math.pi and rel_theta <= 3*math.pi /2: # pull
            dist, gamma = sas_solver(rel_theta - math.pi, r, gap)
        else: # push
            dist, gamma = sas_solver(2*math.pi - rel_theta, r, gap)

        # magnetic force 
        if (rel_theta < magnet_range) or ((rel_theta < math.pi + magnet_range) and (rel_theta > math.pi)):
            #f_sum += -1 * math.fabs( f_const * math.cos(gamma) / (dist**2))
            f_sum += -1 * math.fabs( n_const *  dist**-3.882 * math.cos(gamma) )
        elif (rel_theta > 2*math.pi - magnet_range) or ((rel_theta < math.pi) and rel_theta > math.pi - magnet_range):
            #f_sum += math.fabs( f_const * math.cos(gamma) / (dist**2))
            f_sum += math.fabs( n_const *  dist**-3.882 * math.cos(gamma))

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
    linear = not systemDetails["testing"]
    
    dt = .0005
    max_iter = math.floor(systemDetails["duration"]/dt)
    avel = systemDetails["start_rpm"] * math.pi/30 # 360 rpm to rad/sec

    all_theta = [theta]
    all_avel = [avel]
    all_dv = [0]
    all_f = [0]
    all_torque = []
    
    if systemDetails["in_flight"]: 
        # aero drag values
        air_density = 1.225
        v = 26.8
        A = .03726039
        Cd_front = .0651667
        Cd_back = .0626377

    LINEAR_FINISH = True
    #linear = True # set this to true to kill prints
    #linear = False
    linear_start =  30 #* math.pi/30
    linear_slope = 12.8 #* math.pi/30
    #linear_slope = 4
    #print('avel: ', avel)
    
    for i in range(1,max_iter):

        #Friction
        if LINEAR_FINISH:
            if math.fabs(avel) > linear_start:
                avel = avel * .99955
            elif (avel > linear_slope*dt):
                avel = avel - linear_slope * dt
                if not linear:
                    print('start+ ', dt*i)
                    linear = True
            elif (avel < -linear_slope * dt):
                avel = avel + linear_slope * dt
                if not linear:
                    print('start- ', dt*i)
                    linear = True
            elif math.fabs(avel) <= linear_slope*dt:
                avel = 0
                if not linear:
                    print('start0 ', dt*i) 
                    linear = True  
        else:
            avel = avel * .99955

        # this f is now the sum of forces
        f1 = magnetForce(theta, magnets, magnet_range, motor_rad, gap)

        #f2 = magnetForce(theta + math.pi/2, magnets, magnet_range, motor_rad, gap)
        # no negative needed for the new style 
        #f2 = -1 * magnetForce(theta + math.pi/2, magnets, magnet_range, motor_rad, gap)
        f = f1 #+ f2

        all_f.append(f)
        torque = f * motor_rad #+ aero_torque
        #print('torque: ', torque)
        
        
        if systemDetails["in_flight"]: 
            #Aero Torque = force_back * half length of prop - force_front * half length of prop
            #Cd is adjusted for angle with the cos 
            
            #print('front force: ', (air_density * (v+ math.sin(theta)* avel*prop_rad/2)**2 * A / 2) * (Cd_front))
            #print('back force:', (air_density * (v+ math.sin(theta)* avel*prop_rad/2)**2 * A / 2) * (Cd_back))

            front_force = air_density * Cd_front * A * (v + avel*prop_rad/2*math.cos(theta))**2 / 2
            back_force = air_density * Cd_back * A * (v - avel*prop_rad/2*math.cos(theta))**2 / 2
            #front_force = air_density * Cd_front * A * (v )**2 / 2
            #back_force = air_density * Cd_back * A * (v )**2 / 2

            total_aero_force = (back_force - front_force) * math.cos(theta) # adjusting for cd changes with rotating
            aero_torque = total_aero_force * math.cos(theta) * prop_rad /2 # only want force tangent to prop
            torque += aero_torque        

        all_torque.append(torque)
        
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
            "distance" : all_distance, "dv" : all_dv, "force": all_f, "torque" : all_torque}

def torque_over_cycle(systemDetails, start_angle=0, finish_angle=360, polar=False):
    thetas = range(start_angle*10,finish_angle*10 + 10,10)
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


    if (polar == False and start_angle != 0):
        thetas = [theta - start_angle for theta in thetas]
    if polar == True:
        return cartesian_x,cartesian_y
    else:
        return thetas, torques
