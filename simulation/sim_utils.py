import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math
from sim_phys import test, torque_over_cycle, make_cont_magnet
import random as rand

def force_profile(sim_data):
    tol = 1e-4
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

def rtest(systemDetails):
    #Does a run with random initial theta
    theta_0 = rand.random() * 2 * math.pi
    a = test(theta_0,systemDetails)

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
    plt.plot(a["time"], a["force"])
    plt.xlabel("time (s)")
    plt.ylabel("Force (N)")

    plt.subplots_adjust(left=0.125, right = 0.9, bottom=.1, top=.9, wspace=.4, hspace=.7)

    plt.show()


def mtest(n, systemDetails):
    #Perform n sims with random starting angles
    #prints the percentage of successful runs
    #returns a list of distances

    results = [test(rand.random() * 2 * math.pi,systemDetails)["distance"][-1] for i in range(n)]
    s = [i for i in results if math.fabs(i) < .3]
    print("{0}%".format(len(s) * 100 / len(results)))
    return results


def otest(n, systemDetails, short=False):
    #performs n sims with angles incremented from 0 to 2pi
    #prints percentage of successful runs
    #returns a list of distances
    max_succ_dist = (5/360) * 2*math.pi*systemDetails["motor_rad"]

    results = [test(i * 2 * math.pi / n, systemDetails)['distance'][-1] for i in range(n)]
    s = [i for i in results if math.fabs(i) < max_succ_dist] #.2
    print("{0}%".format(len(s) * 100 / len(results)))
    if short == True:
        return round(len(s) * 100 / len(results))
    else:
        return results 

def theta_test(n, systemDetails, short=False):
    #performs n sims with angles incremented from 0 to 2pi
    #prints percentage of successful runs
    #returns a list of distances

    fThetas = [test(i * 2 * math.pi / n, systemDetails)['theta'][-1] for i in range(n)]
    s = []
    f = []
    for theta in fThetas:
        if (math.fabs(theta) < 5*math.pi/180 or math.fabs(theta - math.pi) < 5*math.pi/180 or math.fabs(theta - 2*math.pi) < 5*math.pi/180):
            s.append(theta)
        else:
            f.append(theta)
    print("{0}%".format(len(s) * 100 / len(fThetas)))
    rate = round(len(s) * 100 / len(fThetas))
    if short == True:
        return rate
    else:
        return [rate, s, f]

def cont_mag_plts(systemDetailsOg):
    # takes total amount of magnets and shows what distributed magnets will look like
    systemDetails = systemDetailsOg.copy()
    magnets = systemDetails["magnets"]
    n = 180

    force_sum = 0
    for magnet in magnets:
        force_sum += math.fabs(magnet[1])
    
    systemDetails["magnets"] = [(0,force_sum)]
    theta0, torque0 = torque_over_cycle(systemDetails)
    print('0')
    magDeg = [(magnet[0] * 180/math.pi, magnet[1]) for magnet in systemDetails["magnets"]]
    print('Magnets: ', magDeg)
    #rtest(systemDetails)
    res0 = otest(n, systemDetails, short=True)

    systemDetails["magnets"] = make_cont_magnet(15, 5, force_sum)
    theta15, torque15 = torque_over_cycle(systemDetails)
    print('15')
    magDeg = [(magnet[0] * 180/math.pi, magnet[1]) for magnet in systemDetails["magnets"]]
    print('Magnets: ', magDeg)
    #rtest(systemDetails)
    res15 = otest(n, systemDetails, short=True)

    systemDetails["magnets"] = make_cont_magnet(30, 10, force_sum)
    theta30, torque30 = torque_over_cycle(systemDetails)
    print('30')
    magDeg = [(magnet[0] * 180/math.pi, magnet[1]) for magnet in systemDetails["magnets"]]
    print('Magnets: ', magDeg)
    #rtest(systemDetails)
    res30 = otest(n, systemDetails, short=True)

    systemDetails["magnets"] = make_cont_magnet(45, 15, force_sum)
    theta45, torque45 = torque_over_cycle(systemDetails)
    print('45')
    magDeg = [(magnet[0] * 180/math.pi, magnet[1]) for magnet in systemDetails["magnets"]]
    print('Magnets: ', magDeg)
    #rtest(systemDetails)
    res45 = otest(n, systemDetails, short=True)

    systemDetails["magnets"] = make_cont_magnet(60, 15, force_sum)
    theta60, torque60 = torque_over_cycle(systemDetails)
    print('60')
    magDeg = [(magnet[0] * 180/math.pi, magnet[1]) for magnet in systemDetails["magnets"]]
    print('Magnets: ', magDeg)
    #rtest(systemDetails)
    res60 = otest(n, systemDetails, short=True)

    f1, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5,1, sharex = True, sharey = True)
    f1.text(0.05, 0.5, 'Torque [Nm]', ha='center', va='center', rotation='vertical')
    plt.suptitle('Torque During Cycle with ' + str(force_sum) + ' [N] Combined Pull Force')
    ax1.plot(theta0, torque0, 'b', label='0 Degrees')
    ax1.set_title('Success Rate: ' + str(res0) + '%', loc='left')
    ax1.legend(loc='lower right')
    
    ax2.plot(theta15, torque15, 'g', label='30 Degrees')
    ax2.legend(loc='lower right')
    ax2.set_title('Success Rate: ' + str(res15) + '%', loc='left')

    ax3.plot(theta30, torque30, 'r', label='60 Degrees')
    ax3.legend(loc='lower right')
    ax3.set_title('Success Rate: ' + str(res30) + '%', loc='left')

    ax4.plot(theta45, torque45, 'y', label='90 Degrees')
    ax4.legend(loc='lower right')
    ax4.set_title('Success Rate: ' + str(res45) + '%', loc='left')

    ax5.plot(theta60, torque60, 'c', label='120 Degrees')
    ax5.legend(loc='lower right')
    ax5.set_title('Success Rate: ' + str(res60) + '%', loc='left')

    plt.xlabel('Leading Angle [Degrees]')
    plt.subplots_adjust(left=0.125, right = 0.9, bottom=.1, top=.9, wspace=.4, hspace=.7)
    plt.show()

def succ_per_pull(systemDetails):
    pullForces = [ i for i in range(0,60,2)]
    n = 90
    res = []
    for force in pullForces:
        systemDetails["magnets"] = [(0,force)]
        res.append(theta_test(n, systemDetails, short=True))

    plt.figure()
    plt.plot(pullForces, res)
    plt.xlabel('Pull Force [N]')
    plt.ylabel('Success Rate %')
    plt.show()

def failzone_per_pull(systemDetails):
    pullForces = [ i for i in range(0,60,5)]
    n = 90
    for force in pullForces:
        f_x = []
        f_y = []
        s_x = []
        s_y = []
        systemDetails["magnets"] = [(0,force)]
        rate, s_thetas, f_thetas = theta_test(n, systemDetails)
        for f_theta in f_thetas:
            f_x.append(math.cos(f_theta))
            f_y.append(math.sin(f_theta))
        for s_theta in s_thetas:
            s_x.append(math.cos(s_theta))
            s_y.append(math.sin(s_theta))
        plt.figure(1)
        plt.title('Pull Force: ' + str(force) + ' [N] |'+ 'Success Rate: ' + str(rate))
        plt.plot(f_x,f_y,'ro')
        plt.plot(s_x,s_y,'bo')
        plt.show()

def save_animation_data(test,fname,frame_rate=60):
    #CUTS OUT ALL POINTS THAT DON'T LIE ON FRAME TIMESTEP
    #saves file as csv with two columns, time and theta
    #frame_rate = fps value, 
    
    time = test["time"]
    angles = test["theta"]
    forces = test["force"]

    dt = time[1] - time[0]
    datapoints_per_frame = int(1 / (frame_rate * dt))

    animation_time = [time[i * datapoints_per_frame] for i in range(int(len(time)/datapoints_per_frame))]
    animation_angles = [angles[i * datapoints_per_frame] for i in range(int(len(angles)/datapoints_per_frame))]
    animation_forces = [forces[i * datapoints_per_frame] for i in range(int(len(forces)/datapoints_per_frame))]
    np.savetxt(fname,np.c_[animation_time,animation_angles, animation_forces],delimiter=',')

