

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
        for o in bpy.context.collection['Collection'].objects:
            o.select_set(True)
            bpy.ops.object.delete()
    except Exception:
        print(" No Object exist !")
    
    # bpy.context.collection['Collection'].name = 'env'
    for o in bpy.context.scene.objects:
        o.select_set(False)


def load_gltf_transform(path, scene, collection=None, m_json=None):
    path = path + '.gltf'
    print(path)
    if os.path.exists(path):
        mat = Matrix()
        mat.identity()

        # if scene['name'] != '44b51d4d-8740-42ad-b88c-93efe49f9d2b':
        #     return

        print(f"{scene['name']} loading !")
        if m_json is not None:
            # column-major ??
            data = np.reshape(m_json, (4, 4)).transpose()
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
        obs = []
        for obj in bpy.context.scene.objects:
            if obj.name not in collection.objects and obj.type not in ['CAMERA', 'LAMP', 'SPOT', 'LIGHT']:
                obs.append(obj)


        if len(obs) > 1:
            ctx = {}
            # # one of the objects to join
            ctx["object"] = ctx["active_object"] = obs[0]
            ctx["selected_objects"] = ctx["selected_editable_objects"] = obs
            
            bpy.ops.object.join(ctx)
            

        model = bpy.data.objects[obs[0].name]
        model.name = scene['name']
        model.select_set(state=True)
        collection.objects.link(model)
        bpy.context.scene.collection.objects.unlink(model)

        model.location = pos
        model.rotation_quaternion = rot
        model.scale = scale


def add_model(model_file, model_id):
    scene = bpy.context.scene
    bpy.context.scene.cycles.samples = 20
    scene.render.resolution_x = 256
    scene.render.resolution_y = 256
    scene.render.resolution_percentage = 100

    house_config = {}

    with open(f"{model_file}\\{model_id}\\house.json", "r") as f:
        house_config = json.load(f)

    levels = house_config['levels']
    if model_id not in bpy.data.collections.keys():
        myCol = bpy.data.collections.new(model_id)
        bpy.context.scene.collection.children.link(myCol)
    else:
        myCol = bpy.data.collections[model_id]

    for level in levels:
        nodes = level['nodes']
        for node in nodes:
            if node['type'] == 'Room':
                filename = node['modelId'] + 'c'
                file = {"name": filename}
                load_gltf_transform(
                    f"{model_file}\\{model_id}\\{filename}", scene=file, collection=myCol)
                filename = node['modelId'] + 'f'
                file = {"name": filename}
                load_gltf_transform(
                    f"{model_file}\\{model_id}\\{filename}", scene=file, collection=myCol)
                filename = node['modelId'] + 'w'
                file = {"name": filename}
                load_gltf_transform(
                    f"{model_file}\\{model_id}\\{filename}", scene=file, collection=myCol)
            elif node['type'] == 'Object':
                filename = node['modelId']
                file = {"name": filename}
                load_gltf_transform(
                    f"{model_file}\\{model_id}\\{filename}", scene=file, m_json=node['transform'], collection=myCol)
            elif node['type'] == 'Ground':
                filename = node['modelId'] + 'f'
                file = {"name": filename}
                load_gltf_transform(
                    f"{model_file}\\{model_id}\\{filename}", scene=file, collection=myCol)


clean()
add_model(
    model_file='C:\\Project\\3D-House-Blender\\scenes', model_id='0f2bcc07-85c2-41a1-8712-cee71117aff6')
