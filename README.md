# 3D-House-Blender
Render 3d house dataset with blender

## Prepare Dataset

The Format of Dataset should be like this:

- `Root`
  - `house`
    - `house_id`
      - `house.json`
    - .....
  - `object`
    - `object_id`
      - .......
  - `room`
    - `room_id`
      - `wall.obj`
      - `floor.obj`
      - ......

## Prepare Scene

- Run `node install --save obj2gltf ` in the project

- modify local setting
  -  `data_dir` : the `Root`
  - `house_id`: the Id of house
  - `dir`: Glft model's save path, default `./scene`
- Start a Terminal and change directory to Project root
  - Input `node run glfthouse.js`

## Blender with VsCode

https://huailiang.github.io/blog/2020/blender/

https://blog.csdn.net/ttm2d/article/details/102760076

To Run `Generator.py`, Open`Generator.py`  and input `Ctrl + Shift + P` Or `F1`From keyboard, Select

- `Blender: Start`

> Blender need time for installing this script 

Input `Ctrl + Shift + P` Or `F1` From keyboard, Select

- `Blender: run Script`

## Render Scene to Image

- [ ] Set Light
- [ ] Set Camera
- [ ] Render Scene to Image

