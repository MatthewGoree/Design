
showconsole()
mydir="./"
open(mydir .. "force_calc.fem")
mi_saveas(mydir .. "temp.fem")
mi_seteditmode("group")

angles = {}
x_forces = {}
y_forces = {}
torques = {}


for n=0,(180 * 5) do
    mi_analyze()
    mi_loadsolution()
    mo_groupselectblock(1)
    xf=mo_blockintegral(18)
    yf=mo_blockintegral(19)


    mi_selectgroup(1)
    mi_moverotate(3.5/2.0 ,1.26/2.0,.2 )

    print(n)
    print(xf)
    print(yf)
    x_forces[n] = xf
    y_forces[n] = yf
    angles[n] = n / 5.0


end

fangles = {}
gammas = {}
for i = 0, (180 * 5) do
   xf = x_forces[i]
   yf = y_forces[i]
   fmag = sqrt(xf * xf + yf * yf)
   fangle = atan(yf / xf)
   if xf < 0 then fangle = fangle + pi end
   print(fangle)
   print(fmag)
   fangles[i] = fangle
   gammas[i] = cos(fangle - angles[i])
   torques[i] = fmag * (.089/2) * cos(-1.0 * fangle + (angles[i] * pi / 180))
   print(torque)
   print("\n")
end



fp=openfile(mydir .. "force-results.txt","w")
for k = 0,(180 * 5) do
  write(fp, angles[k], ",", x_forces[k], ",",y_forces[k], "," , torques[k], "\n")
end
closefile(fp);

mo_close()
mi_close()
