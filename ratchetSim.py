def test(theta):
    mass = 1
    length = .8
    I = m * length * length / 12
    max_iter = 5000
    dt = .01
    avel = 10
    
    
    all_theta = [theta]
    all_avel = [avel]
    all_dv = [0]

    for i in range(1,max_iter):
        #Friction
        avel = avel * .997

        #Magnet Force
        if (theta < magnet_range) or ((theta < math.pi + magnet_range) and (theta > math.pi)):
            f = -1 * math.fabs(math.sin(theta)) * f_const
            all_dv.append(-1)
            #print("neg force: theta = {0}".format(theta * 180 / math.pi))

        elif (theta > math.pi - magnet_range) or ((theta < math.pi) and theta > math.pi - magnet_range):
            f = 1 * math.fabs(math.sin(theta)) * f_const
            all_dv.append(1)
            #print("pos force: theta = {0}".format(theta * 180 / math.pi))
        else:
            f = 0
            all_dv.append(0)
            #print("no force: theta = {0}".format(theta * 180 / math.pi))

        torque = f * l
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
        

