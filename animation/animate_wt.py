import bpy  
import math
from mathutils import Vector
import numpy as np
import os
import sys

def fmap(force,fmin,fmax):
    left_angle = .61
    right_angle = -.61

    return (force - fmax) * left_angle / (fmin - fmax) + (force - fmin) * right_angle / (fmax - fmin)

#DEFAULT COMMAND WITH NO PATHS SPECIFIED HAS 5 ARGS
if len(sys.argv) != 7:
    DATA_PATH = r"C:\Users\mattg\OneDrive\Documents\Design\DesignRepo\animation\29failure3.csv"
    RENDER_PATH = r"C:\Users\mattg\OneDrive\Documents\Design\DesignRepo\output.mp4"
else:
    DATA_PATH = sys.argv[-2]
    RENDER_PATH = os.path.join(os.getcwd(),sys.argv[-1])

#-.605 right
#.61 left

print(sys.argv)
print(DATA_PATH)
print(RENDER_PATH)

AUTO_RENDER = False

# useful shortcut
scene = bpy.context.scene

#render settings
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = "H264"
scene.render.image_settings.color_mode = 'RGB'
scene.render.resolution_percentage = 50
scene.render.filepath = RENDER_PATH

# Finding objects 
prop_name = 'full propeller - Standard Blade-1'
motor_name = "KDE8218XF-120KV.001"
prop = scene.objects[prop_name]
prop.animation_data_clear()

if motor_name in scene.objects.keys():
    motor = scene.objects[motor_name]
    motor.animation_data_clear()
    dial = scene.objects["Dial"]
    dial.animation_data_clear()
    torque = scene.objects["Torque"]
    torque.animation_data_clear()


else:
    motor = None
    

#loading data
data = np.genfromtxt(DATA_PATH,usecols=(0,1,2), delimiter=',')
angles = [i[1] for i in data]
times = [i[0] for i in data]
forces = [i[2] for i in data]



fmin = min(forces)
fmax = max(forces)

dial_angles = [fmap(i,fmin,fmax) for i in forces] 


### animation
positions_prop = [( math.pi/2,0,i) for i in angles]
positions_motor = [(math.pi,0,i) for i in angles]
positions_dial = [(0,0,i) for i in dial_angles]

# start with frame 0
number_of_frame = 0

def my_handler(scene):
    frame = scene.frame_current
    torque.data.body = "{:.3}".format(str(forces[frame]))
    
    
for i in range(len(positions_prop)):
    prop_pos = positions_prop[i]
    motor_pos = positions_motor[i]
    dial_pos = positions_dial[i]
    torque_val = forces[i]
    # now we will describe frame with number $number_of_frame
    scene.frame_set(number_of_frame)
    prop.rotation_euler = prop_pos
    
    
    if not motor == None:
        motor.rotation_euler = motor_pos
        motor.keyframe_insert(data_path="rotation_euler", index=-1)
        dial.rotation_euler = dial_pos
        dial.keyframe_insert(data_path="rotation_euler", index=-1)
            
    prop.keyframe_insert(data_path="rotation_euler", index=-1)
    
    
    # move next 10 frames forward - Blender will figure out what to do between this time
    number_of_frame += 1
    
    
scene.frame_start = 0
scene.frame_end = len(positions_prop) - 1
#render
if AUTO_RENDER:
    print(scene.render.filepath)
    bpy.ops.render.render(animation=True)


bpy.app.handlers.frame_change_pre.append(my_handler)


