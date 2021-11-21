

import bpy
import os
import json
import numpy as np
from decimal import Decimal
from mathutils import Vector, Matrix


def clean():
    # setting
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links
    # Clear default nodes
    for n in tree.nodes:
        tree.nodes.remove(n)

    # Delete default cube
    # clean out the scene
    try:
        for o in bpy.context.scene.objects:
            o.select_set(True)
            bpy.ops.object.delete()
    except Exception:
        print(" No Object exist !")


def load_gltf_transform(path, scene, m_json=None, receive_shadow=None):
    path = path + '.gltf'
    if os.path.exists(path):
        mat = Matrix()
        mat.identity()
        print(scene['name'])
        if m_json is not None:
            # column-major ??
            data = np.reshape(m_json, (4,4)).transpose()
            mat = Matrix(data).to_4x4()

        t, q, s = mat.decompose()

        # blender_pos_x = x
        # blender_pos_y = -z
        # blender_pos_z = y

        # blender_rot_w = w``
        # blender_rot_x = x
        # blender_rot_y = z
        # blender_rot_z = y
        t[1], t[2] = -t[2], t[1]
        q[2], q[3] = q[3], q[2]
        s[1], s[2] = s[2], s[1]

        

        pos = t.to_tuple()
        rot = q
        scale = s.to_tuple()
        

        for o in bpy.context.scene.objects:
            o.select_set(False)

        bpy.ops.import_scene.gltf(filepath=path)
        
        model = bpy.data.objects['Node']
        model.name = scene['name']
        model.select_set(state=True)

        # model.matrix_basis = mat.copy()
        bpy.context.view_layer.objects.active = model
        model.location = pos
        model.rotation_quaternion = rot
        model.scale = scale

def add_model(model_file):
    scene=bpy.context.scene
    bpy.context.scene.cycles.samples=20
    scene.render.resolution_x=256
    scene.render.resolution_y=256
    scene.render.resolution_percentage=100

    house_config={}

    with open(f"{model_file}\\house.json", "r") as f:
        house_config=json.load(f)

    levels=house_config['levels']
    for level in levels:
        nodes=level['nodes']
        for node in nodes:
            if node['type'] == 'Room':
                filename=node['modelId'] + 'c'
                file = {"name":filename}
                load_gltf_transform(f"{model_file}\\{filename}", file)
                filename=node['modelId'] + 'f'
                file = {"name":filename}
                load_gltf_transform(f"{model_file}\\{filename}", file)
                filename=node['modelId'] + 'w'
                file = {"name":filename}
                load_gltf_transform(f"{model_file}\\{filename}", file)
            elif node['type'] == 'Object':
                filename=node['modelId']
                file = {"name":filename}
                load_gltf_transform(
                    f"{model_file}\\{filename}", file, node['transform'])
            elif node['type'] == 'Ground':
                filename=node['modelId'] + 'f'
                file = {"name":filename}
                load_gltf_transform(f"{model_file}\\{filename}", file)



clean()
add_model(
    model_file='C:\\Project\\3D-House-Blender\\scenes\\00c0c75e-1c12-46b3-9fc8-0561b1b1b510')
