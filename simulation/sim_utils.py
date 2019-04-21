import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math
from sim_phys import test
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
    
    #values = [math.fabs(i) for i in a["force"][-5020:-4950]]
    #plt.plot(a["theta"][-5020:-4950], values)
    #plt.xlabel("Theta (rad)")
    #plt.ylabel("force (N)")

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


def otest(n, systemDetails):
    #performs n sims with angles incremented from 0 to 2pi
    #prints percentage of successful runs
    #returns a list of distances

    results = [test(i * 2 * math.pi / n, systemDetails)['distance'][-1] for i in range(n)]
    s = [i for i in results if math.fabs(i) < .2]
    print("{0}%".format(len(s) * 100 / len(results)))
    return results

