import bpy
import os
import json
import numpy as np
from decimal import Decimal
from mathutils import Vector, Matrix
import argparse
import numpy as np
import sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__)+'/tools')

from tools.utils import *
from tools.blender_interface import BlenderInterface

if __name__ == '__main__':

    p = argparse.ArgumentParser(description='Renders given obj file by rotation a camera around it.')
    p.add_argument('--mesh_fpath', type=str, required=True, help='The path the output will be dumped to.')
    p.add_argument('--output_dir', type=str, required=True, help='The path the output will be dumped to.')
    p.add_argument('--num_observations', type=int, required=True, help='The path the output will be dumped to.')
    p.add_argument('--sphere_radius', type=float, required=True, help='The path the output will be dumped to.')
    p.add_argument('--mode', type=str, required=True, help='Options: train and test')

    argv = sys.argv
    argv = sys.argv[sys.argv.index("--") + 1:]

    opt = p.parse_args(argv)

    instance_name = opt.mesh_fpath.split('/')[-3]
    instance_dir = os.path.join(opt.output_dir, instance_name)

    # Start Render
    renderer = BlenderInterface(resolution=128)
    
    if opt.mode == 'train':
        cam_locations = sample_spherical(opt.num_observations, opt.sphere_radius)
    elif opt.mode == 'test':
        cam_locations = get_archimedean_spiral(opt.sphere_radius, opt.num_observations)

    obj_location = np.zeros((1,3))

    cv_poses = look_at(cam_locations, obj_location)
    blender_poses = [cv_cam2world_to_bcam2world(m) for m in cv_poses]

    shapenet_rotation_mat = np.array([[1.0000000e+00,  0.0000000e+00,  0.0000000e+00],
                                    [0.0000000e+00, -1.0000000e+00, -1.2246468e-16],
                                    [0.0000000e+00,  1.2246468e-16, -1.0000000e+00]])
    rot_mat = np.eye(3)
    hom_coords = np.array([[0., 0., 0., 1.]]).reshape(1, 4)
    obj_pose = np.concatenate((rot_mat, obj_location.reshape(3,1)), axis=-1)
    obj_pose = np.concatenate((obj_pose, hom_coords), axis=0)

    renderer.import_mesh(opt.mesh_fpath, scale=1., object_world_matrix=obj_pose)
    renderer.render(instance_dir, blender_poses, write_cam_params=True)