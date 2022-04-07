# Copyright 2020 Hsueh-Ti Derek Liu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import bpy

def setMat_pointCloud(mesh, \
                ptColor, \
                ptSize): 
    # initialize a primitive sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius = 1.0, location = (1e7,1e7,1e7))
    sphere = bpy.context.object
    bpy.ops.object.shade_smooth()
    mat = bpy.data.materials.new(name="sphereMat")
    sphere.data.materials.append(mat)
    sphere.active_material = mat
    mat.use_nodes = True
    tree = mat.node_tree
    HSVNode = tree.nodes.new('ShaderNodeHueSaturation')
    HSVNode.inputs['Color'].default_value = ptColor.RGBA
    HSVNode.inputs['Saturation'].default_value = ptColor.S
    HSVNode.inputs['Value'].default_value = ptColor.V
    HSVNode.inputs['Hue'].default_value = ptColor.H

    # set color brightness/contrast
    BCNode = tree.nodes.new('ShaderNodeBrightContrast')
    BCNode.inputs['Bright'].default_value = ptColor.B
    BCNode.inputs['Contrast'].default_value = ptColor.C
    tree.links.new(HSVNode.outputs['Color'], BCNode.inputs['Color'])
    tree.links.new(BCNode.outputs['Color'], tree.nodes['Principled BSDF'].inputs['Base Color'])

    # init particle system
    mesh.modifiers.new("part", type='PARTICLE_SYSTEM')
    ps = mesh.particle_systems[0]
    ps.settings.count = len(mesh.data.vertices)
    ps.settings.frame_start = 0
    ps.settings.frame_end = 0
    ps.settings.emit_from = 'VERT'
    ps.settings.physics_type = 'NO'
    ps.settings.particle_size = ptSize
    ps.settings.render_type = 'OBJECT'
    ps.settings.instance_object = sphere
    ps.settings.use_emit_random = False

