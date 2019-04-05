import math
import matplotlib.pyplot as plt
import random as rand
import numpy as np
from mpl_toolkits import mplot3d

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
    phi = math.asin( (r*(1-math.cos(theta)) + gap) / dist )

    return dist, phi

def force_profile(sim_data):
    tol = 1e-15
    force = sim_data["force"]
    time = sim_data["time"]

    markers = [i for i in range(len(force) - 1) if (math.fabs(force[i]) < tol and math.fabs(force[i+1]) > tol)]
    f1 = force[markers[0] : markers[2]]
    t1 = time[markers[0] : markers[2]]

    force = force[markers[0]:]
    time = time[markers[0]:]
    all_f = []
    all_t = []
    f_c = []
    t_c = []

    save_flag = False
    for i in range(len(force)-1):
        if math.fabs(force[i]) > tol:
            save_flag = True
            f_c.append(force[i])
            t_c.append(time[i])
        elif save_flag == True:
            all_f.append(f_c)
            all_t.append(t_c)
            f_c = []
            t_c = []
            save_flag = False
        
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    for i in range(len(all_t)):
        zline = [i for j in range(len(all_t[i]))]
        ax.plot3D(all_t[i],zline,all_f[i])
    plt.show()
    
    

    return (all_t,all_f)


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

        # get theta value relative to the magnet (original should not have theta change)
        rel_theta = theta - magnet_offset

        # make sure the relative angle is between 0 and 2*pi 
        if rel_theta < 0:
            rel_theta += 2*math.pi 

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
            f_sum += -1 * math.fabs( f_const * math.cos(phi) / (dist**2  * 7067))
            #print('neg')
            #print(rel_theta)
            #print(f_sum)
            #f_sum  += -1 * math.fabs(math.cos(rel_theta)) * f_const

        elif (rel_theta > 2*math.pi - magnet_range) or ((rel_theta < math.pi) and rel_theta > math.pi - magnet_range):
            f_sum += math.fabs( f_const * math.cos(phi) / (dist**2  * 7067) )
            #print('pos')
            #print(rel_theta)
            # f_sum  += math.fabs(math.cos(rel_theta)) * f_const
            #print(f_sum)

    return f_sum

# added test as an argument so this can be used with multiple sims
def rtest(sim_test):
    #Does a run with random initial theta
    theta_0 = rand.random() * 2 * math.pi
    a = sim_test(theta_0)

    print('Starting angle: ', theta_0)

    print('Final angle: ', a["theta"][-1] * 180/math.pi)
    print('Final distance: ', a["distance"][-1])
    print('Final avel', a["avel"][-1])

    plt.subplot(3,3,1)
    plt.plot(a["time"], a["theta"])
    plt.xlabel("time (s)")
    plt.ylabel("Theta (rad)")

    plt.subplot(3,3,2)
    plt.plot(a["time"], a["avel"])
    plt.xlabel("time (s)")
    plt.ylabel("avel (rad/s)")

    plt.subplot(3,3,3)
    plt.plot(a["time"], a["dv"])
    plt.xlabel("time (s)")
    plt.ylabel("dv (rad/s)")

    plt.subplot(3,3,4)
    plt.plot(a["time"], a["distance"])
    plt.xlabel("time (s)")
    plt.ylabel("distance (m)")

    plt.subplot(3,3,5)
    
    #values = [math.fabs(i) for i in a["force"][-5020:-4950]]
    #plt.plot(a["theta"][-5020:-4950], values)
    #plt.xlabel("Theta (rad)")
    #plt.ylabel("force (N)")

    plt.plot(a["time"], a["force"])
    plt.xlabel("time (s)")
    plt.ylabel("Force (N)")


    plt.subplots_adjust(left=0.125, right = 0.9, bottom=.1, top=.9, wspace=.4, hspace=.7)

    plt.show()


def mtest(n):
    #Perform n sims with random starting angles
    #prints the percentage of successful runs
    #returns a list of distances

    results = [test(rand.random() * 2 * math.pi)["distance"][-1] for i in range(n)]
    s = [i for i in results if math.fabs(i) < .3]
    print("{0}%".format(len(s) * 100 / len(results)))
    return results


def otest(n):
    #performs n sims with angles incremented from 0 to 2pi
    #prints percentage of successful runs
    #returns a list of distances

    results = [test(i * 2 * math.pi / n)['distance'][-1] for i in range(n)]
    s = [i for i in results if math.fabs(i) < .2]
    print("{0}%".format(len(s) * 100 / len(results)))
    return results


def test(theta):
    #performs a sim with given starting angle
    motor_mass = .845 #kg
    propeller_mass = .300 #kg
    added_mass = .2 #weight of whatever we add to motor (kg)

    m = motor_mass + propeller_mass + added_mass
    prop_length = .7 #meter
    prop_rad = prop_length / 2
    motor_rad = .089 / 2 #meters


    prop_I = 0.004064 * 2
    motor_I = (motor_mass * motor_rad ** 2) / 2 #I = m * r ^2 for thin shelled cylinder, assume only half of motor mass is spinning
    #I = m * 4 * r / 12

    I = prop_I + motor_I

    f_const = 8.89644 #2 lbs of force

    dt = .0005
    max_iter = math.floor(30/dt)

    #avel = 15000 * math.pi/30 # 15000 rpm to rad/sec

    avel = 1000 * math.pi/30 # 15000 rpm to rad/sec

    # for testing 
    #avel =  2 * (13/5) * math.pi 

    #magnet_range = math.pi/6
    magnet_range = math.pi/2.5

    gap  = .01

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

    # magnet = (offset_angle, f_const)

    #magnets = [(0, 8.89644), (math.pi/6, 8.89644/4), (math.pi - math.pi/6, 8.89644/4)]
    #magnets = [(0, 8.89644)]
    #magnets = [(0,8.89644), (math.pi/6,-8.89644/4), (math.pi/6 + math.pi, -8.89644/4)]

    magnets = [(0,2*8.89644)] #, (math.pi/2, -8.89644)]
    
    for i in range(1,max_iter):

        #Friction
        #avel = avel * .9963
        avel = avel * .99963

        # this f is now the sum of forces 
        f1 = magnetForce(theta, magnets, magnet_range, motor_rad, gap)
        #f2 = magnetForce(theta + math.pi/2, magnets, magnet_range, motor_rad, gap)
        
        # no negative needed for the new style 
        #f2 = -1 * magnetForce(theta + math.pi/2, magnets, magnet_range, motor_rad, gap)
        f = f1 #+ f2

        all_f.append(f)
        
        '''
        if f1 or f2 and i % 10000 > 9999:
            print('_____it begins____')
            print('theta1:', theta * 180/math.pi)
            print('theta2:', theta * 180/math.pi + 90)
            print('force 1:', f1)
            print('force 2:', f2)
            print('total force:',f)
        '''

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

    # r probably out of date here 
    all_distance = [distance(i,prop_rad) for i in all_theta]
    return {"time" : all_t, "theta" : all_theta, "avel" : all_avel,
            "distance" : all_distance, "dv" : all_dv, "force": all_f}

def save_data(test, fname):
    np.savetxt(fname, np.c_[test["time"], test["theta"], test["distance"]], delimiter = ',')

if __name__ == '__main__':
    a = test(math.pi/3)
    t,f = force_profile(a)
    #rtest(test)
    #print('mtest')
    #otest(50)
