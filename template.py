import sys, os
sys.path.append(os.path.join(os.path.abspath(os.getcwd()))) # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
import os, bpy, bmesh
import numpy as np
import argparse

cwd = os.getcwd()

'''
RENDER AN IMAGE STEP-BY-STEP:
1. copy "template.py" to your preferred local folder
2. In "template.py":
    - change the second line to your path to the BlenderToolbox, such as "sys.path.append('path/to/BlenderToolbox/')"
    - change "meshPath"
    - set your desired material (select one from the demo scripts)
3. run "blender --background --python template.py" in terminal, then terminate the code when it starts rendering. This step outputs a "test.blend"
4. open "test.blend" with your blender software
5. In blender UI, adjust:
    - location, rotation, scale of the mesh
    - material parameters
6. In "template.py":
    - type in the adjusted parameters from GUI 
    - set outputPath and increase imgRes_x, imgRes_y, numSamples
7. run "blender --background --python template.py" again to output your final image
'''

out_path = './template.png'
mesh_path = './meshes/spot.ply'
mesh_loc_x = 1.12
mesh_loc_y = -0.14
mesh_loc_z = 0
mesh_rot_x = 90
mesh_rot_y = 0
mesh_rot_z = 227
mesh_scale_x = 1.0
mesh_scale_y = 1.0
mesh_scale_z = 1.0

if len(sys.argv) > 4:
    out_path = sys.argv[4]
if len(sys.argv) > 5:
    mesh_path = sys.argv[5]
if len(sys.argv) > 8:
    mesh_loc_x = float(sys.argv[6])
    mesh_loc_y = float(sys.argv[7])
    mesh_loc_z = float(sys.argv[8])
if len(sys.argv) > 11:
    mesh_rot_x = float(sys.argv[9])
    mesh_rot_y = float(sys.argv[10])
    mesh_rot_z = float(sys.argv[11])
if len(sys.argv) > 14:
    mesh_scale_x = float(sys.argv[12])
    mesh_scale_y = float(sys.argv[13])
    mesh_scale_z = float(sys.argv[14])


outputPath = os.path.join(cwd, out_path)

## initialize blender
imgRes_x = 1080 # recommend > 1080 
imgRes_y = 1080 # recommend > 1080 
numSamples = 100 # recommend > 200
exposure = 1.5 
use_GPU = True
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure, use_GPU)

## read mesh
meshPath = mesh_path
location = (mesh_loc_x, mesh_loc_y, mesh_loc_z) # (GUI: click mesh > Transform > Location)
rotation = (mesh_rot_x, mesh_rot_y, mesh_rot_z) # (GUI: click mesh > Transform > Rotation)
scale = (mesh_scale_x, mesh_scale_y, mesh_scale_z) # (GUI: click mesh > Transform > Scale)
mesh = bt.readMesh(meshPath, location, rotation, scale)

## set shading (uncomment one of them)
bpy.ops.object.shade_smooth() # Option1: Gouraud shading
# bpy.ops.object.shade_flat() # Option2: Flat shading
# bt.edgeNormals(mesh, angle = 10) # Option3: Edge normal shading

## subdivision
bt.subdivision(mesh, level = 1)

###########################################
## Set your material here (see other demo scripts)

# bt.colorObj(RGBA, Hue, Saturation, Value, Bright, Contrast)
RGBA = (239.0/255, 239.0/255, 240.0/255, 1)
meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
bt.setMat_plastic(mesh, meshColor)

## End material
###########################################

## set invisible plane (shadow catcher)
bt.invisibleGround(shadowBrightness=0.9)

## set camera 
## Option 1: don't change camera setting, change the mesh location above instead
camLocation = (3, 0, 2)
lookAtLocation = (0,0,0.5)
focalLength = 45 # (UI: click camera > Object Data > Focal Length)
cam = bt.setCamera(camLocation, lookAtLocation, focalLength)
## Option 2: if you really want to set camera based on the values in GUI, then
# camLocation = (3, 0, 2)
# rotation_euler = (63,0,90)
# focalLength = 45
# cam = bt.setCamera_from_UI(camLocation, rotation_euler, focalLength = 35)

## set light
## Option1: Three Point Light System 
# bt.setLight_threePoints(radius=4, height=10, intensity=1700, softness=6, keyLoc='left')
## Option2: simple sun light
lightAngle = (6, -30, -155) 
strength = 2
shadowSoftness = 0.3
sun = bt.setLight_sun(lightAngle, strength, shadowSoftness)

## set ambient light
bt.setLight_ambient(color=(0.1,0.1,0.1,1)) 

## set gray shadow to completely white with a threshold (optional but recommended)
bt.shadowThreshold(alphaThreshold = 0.05, interpolationMode = 'CARDINAL')

## save blender file so that you can adjust parameters in the UI
bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test.blend')

## save rendering
bt.renderImage(outputPath, cam)