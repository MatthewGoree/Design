import bpy  
import math
from mathutils import Vector
import numpy as np
import os

# useful shortcut
scene = bpy.context.scene

# this shows you all objects in scene
scene.objects.keys()
prop_name = 'full propeller - Standard Blade-1'
motor_name = "KDE8218XF-120KV.001"
prop = scene.objects[prop_name]
prop.animation_data_clear()

if motor_name in scene.objects.keys():
    motor = scene.objects[motor_name]
    motor.animation_data_clear()
else:
    motor = None




path = r"C:\Users\mattg\OneDrive\Documents\Design\DesignRepo\anim_data.csv"
data = np.genfromtxt(path,usecols=(0,1), delimiter=',')
angles = [i[1] for i in data]
times = [i[0] for i in data]

### animation
positions_prop = [( math.pi/2,0,i) for i in angles]
positions_motor = [(math.pi,0,i) for i in angles]
print(os.getcwd())
# start with frame 0
number_of_frame = 0  
for i in range(len(positions_prop)):
    prop_pos = positions_prop[i]
    motor_pos = positions_motor[i]
    # now we will describe frame with number $number_of_frame
    scene.frame_set(number_of_frame)
    prop.rotation_euler = prop_pos
    
    if not motor == None:
        motor.rotation_euler = motor_pos
        motor.keyframe_insert(data_path="rotation_euler", index=-1)
    
    prop.keyframe_insert(data_path="rotation_euler", index=-1)
    
    
    # move next 10 frames forward - Blender will figure out what to do between this time
    number_of_frame += 1
