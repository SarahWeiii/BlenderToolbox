import sys
sys.path.append('/Users/hsuehtil/Dropbox/BlenderToolbox/cycles')
from include import *
import bpy

outputPath = './results/demo_muscle.png'

# # init blender
imgRes_x = 720 # should set to > 2000 for paper figures
imgRes_y = 720 # should set to > 2000 for paper figures
numSamples = 50 # usually set to > 250 for high quality paper images
exposure = 1.5 # need to double check
blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

# read mesh 
meshPath = '../meshes/spot.ply'
location = (-0.3, 0.6, -0.04)
rotation = (90, 0,0)
scale = (1.5,1.5,1.5)
mesh = readPLY(meshPath, location, rotation, scale)

# # set shading
bpy.ops.object.shade_smooth()
# bpy.ops.object.shade_flat()

# # subdivision
level = 2
subdivision(mesh, level)

# # set material
useless = (0,0,0,0)
meshColor = colorObj(useless, 0.5, 1.0, 1.4, 0.0, 0.0) # the color is fixed to blood red
fiberShape = [5.0,2.0,0.4] # this controls the muscle pattern (requires tuning)
bumpStrength = 0.4 # you can leave this as default
wrinkleness = 0.03 # you can leave this as default
maxBrightness = 0.85 # you can leave this as default
minBrightness = 0.3 # you can leave this as default
setMat_muscle(mesh, meshColor, fiberShape, bumpStrength, wrinkleness, maxBrightness,minBrightness)

# # set invisible plane (shadow catcher)
groundCenter = (0,0,0)
shadowDarkeness = 0.7
groundSize = 20
invisibleGround(groundCenter, groundSize, shadowDarkeness)

# # set camera
camLocation = (1.9,2,2.2)
lookAtLocation = (0,0,0.5)
focalLength = 45
cam = setCamera(camLocation, lookAtLocation, focalLength)

# # set sunlight
lightAngle = (-15,-34,-155) 
strength = 2
shadowSoftness = 0.1
sun = setLight_sun(lightAngle, strength, shadowSoftness)

# # set ambient light
ambientColor = (0.2,0.2,0.2,1)
setLight_ambient(ambientColor)

# # save blender file
bpy.ops.wm.save_mainfile(filepath='./test.blend')

# # save rendering
renderImage(outputPath, cam)