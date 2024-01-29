import glob, sys, time, math, random, asyncio, bpy, os, re, io, json, ctypes
from ctypes import *


object_to_hide = []
car_meshes = {}
curent_car_paint = 'GAT'
curent_interior_trim = 'A'
curent_eim = 'GLVALG2Z34ZUA-----'

def remove_object(context, obj_to_remove):
    if obj_to_remove == None:
        obj_to_remove = bpy.context.selected_objects
    if obj_to_remove != None:
        bpy.ops.object.delete()


def add_cube():
    # bpy.ops.mesh.primitive_cube_add()
    cube = bpy.ops.mesh.primitive_cube_add(size=4, location=(0, 0, 0))
    new_mat = bpy.data.materials.new(name="Material")
    new_mat.use_nodes = True
    bsdf = new_mat.node_tree.nodes["Principled BSDF"]
    color_ramp = new_mat.node_tree.nodes.new("ShaderNodeValToRGB")
    color_ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1)
    new_mat.node_tree.links.new(bsdf.inputs['Base Color'], color_ramp.outputs['Color'])

    cube = bpy.context.selected_objects
    for obj in cube:
        obj.data.materials.append(new_mat)


def randomMove(context, cube):
    if cube is None or cube == []:
        cube = bpy.context.selected_objects
    if cube is not None:
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)
        z = random.randint(-10, 10)
        cube[0].location = (x, y, z)


def diffMate(context, cube):
    if cube is None or cube is []:
        cube = bpy.context.object
        # print(cube)
    if cube is not None:
        try:
            material_basic = bpy.data.materials['Basic Mat']        
        except:
            material_basic = bpy.data.materials.new(name='Basic Mat')
        material_basic.use_nodes = True
        principled_node = material_basic.node_tree.nodes.get('Principled BSDF')
        r = random.random()
        g = random.random()
        b = random.random()
        m = random.random()
        roug = random.random()
        ior = random.random() * random.randint(1, 3)
        # print(f'Ref:{r}, Blue:{b}, green: {g}')
        principled_node.inputs[0].default_value = (r, g, b, 1)
        principled_node.inputs[1].default_value = m
        principled_node.inputs[2].default_value = roug
        principled_node.inputs[3].default_value = ior
        textur_node = material_basic.node_tree.nodes.get('ShaderNodeTexImage')
        if textur_node == None:
            textur_node = material_basic.node_tree.nodes.new('ShaderNodeTexImage')
        textur_node.location = (-380, 300)
        images_list = list(glob.glob("D:\BlenderAddons\Maker\Images\*"))
        random_image = images_list[random.randint(0, len(images_list)-1)]
        textur_node.image = bpy.data.images.load(random_image)
        material_basic.node_tree.links.new(textur_node.outputs[0], principled_node.inputs[0])
        cube.active_material = material_basic


def abc_import_synconus(self, context):
    abc_list = list(glob.glob("D:\\alembicCar\\*"))
    t_start = time.time()
    for n in abc_list:
        bpy.ops.wm.alembic_import(filepath=n, relative_path=True, as_background_job=False)
        try:
            tem_name = os.path.basename(n).split('.')[0]
            obj = bpy.context.object
            obj.name = tem_name
            self.car_meshes[tem_name] = True
        except:
            print('Missing mesh')
    t_end = time.time()

    print(f'Total importing time: {t_end - t_start}')


def get_all():
    t_start = time.time()
    car_meshes.clear()
    for ob in bpy.data.objects:
        _name = ob.name
        car_meshes[_name] = not bpy.data.objects[_name].hide_viewport
    t_end = time.time()
    print(f'Select all objects in scene: {t_end - t_start}, objects: {len(car_meshes)}')
    return car_meshes


def hide_random_third_of_car(self, context):
    t_start = time.time()
    if len(self.object_to_hide) > 0:
        self.unhide_random_third_of_car(self, context)
    one_third = len(self.car_meshes) // 3
    for i in range(one_third):
        temp = self.get_random_car_part()
        self.object_to_hide.append(temp)
        bpy.data.objects[temp].hide_viewport = True
    t_end = time.time()
    print(f'Hide random one/third: {t_end - t_start}')
    

def unhide_random_third_of_car(self, context):
    if len(self.car_meshes.items()) == 0:
        self.get_all()
    t_start = time.time()
    for key, value in self.car_meshes.items():
        if not value:
            bpy.data.objects[key].hide_viewport = False
            self.car_meshes[key] = True
    self.object_to_hide.clear()
    t_end = time.time()
    print(f'Unhide objects: {t_end - t_start}')    


def save_scene(context, filepath = 'D:\BlenderAddons\Scenes\Test'):
    t_start = time.time()
    extension = '.blend'
    filename = filepath
    counter = 1
    filepath = f'{filepath}{extension}'
    while os.path.exists(filepath):
        filepath = f'{filename}({counter}){extension}'
        counter += 1

    bpy.ops.wm.save_as_mainfile(filepath=f'{filepath}')
    t_end = time.time()
    print(f'Scene saved to: {filepath}, took: {t_end - t_start} sec')

def create_and_parent(whole_data: str):
    memo = {}
    pattern = f'(def Xform [ "A-Za-z_]+)'
    buf = whole_data.splitlines()
    for n in buf:
        temp = re.findall(pattern, n)
        if temp:
            indent = n.index(temp[0])
            temp_name = temp[0].strip().split('"')[-2]
            # print(f'TEMP NAME:: \n\n\n {temp_name}' )
            bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            temp_obj = bpy.context.active_object
            temp_obj.name = temp_name
            objects = bpy.data.objects
            if indent == 1:
                indent = 4
            else:
                a = objects[memo[indent-4]]
                b = objects[temp_name]
                b.parent = a
            # print(f'{temp_name} line {indent}')
            memo[indent] = temp_name
    return memo

def create_rig():
    pattern = f'(def Xform [ "A-Za-z_]+)'
    with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\RigData.usda', 'r') as data:
        whole_data = data.read()
        idx = whole_data.index('def Xform "RIG_Main"') -1 
        last_bracket_idx = whole_data.rindex('}')
        out = re.findall(pattern, whole_data[idx:last_bracket_idx])
        i_name = str(out[0][:-1]).strip().split('"')[-1]
        if not i_name:
            i_name  = str(out[0][:-1]).strip().split('"')[-2]
        create_and_parent(whole_data[idx: last_bracket_idx])