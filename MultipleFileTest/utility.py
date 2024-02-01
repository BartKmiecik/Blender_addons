import glob, sys, time, math, random, asyncio, bpy, os, re, io, json, ctypes, re
from ctypes import *

object_to_hide = []
car_meshes = {}
curent_car_paint = 'GAT'
curent_interior_trim = 'A'
curent_eim = 'GLVALG2Z34ZUA-----'

alembic_meshes = []

def remove_object(context, obj_to_remove):
    if obj_to_remove == None:
        obj_to_remove = bpy.context.selected_objects
    if obj_to_remove != None:
        bpy.ops.object.delete()


def add_cube():
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

def getChildren(myObject, children = []): 
    for ob in bpy.data.objects: 
        if ob.parent == myObject: 
            children.append(ob)
            getChildren(ob, children)
    return children 

def abc_import_synconus(self, context):
    global alembic_meshes
    alembic_meshes.clear()
    abc_list = list(glob.glob("D:\\alembicCar\\*"))
    t_start = time.time()
    for n in abc_list:
        bpy.ops.wm.alembic_import(filepath=n, relative_path=True, as_background_job=False)
        try:
            tem_name = os.path.basename(n).split('.')[0]
            # h = len(tem_name) + 1
            # tem_name = tem_name[:min(63, h)]
            obj = bpy.context.object
            obj.name = tem_name
            self.car_meshes[tem_name] = True
            childs = getChildren(obj)
            for child in childs:
                print(child)
                if child.type == 'MESH' and not child.name in alembic_meshes:
                    alembic_meshes.append(child.name)
                    
        except:
            print('Missing mesh')
    t_end = time.time()

    print(f'Total importing time: {t_end - t_start}')


def get_all():
    global alembic_meshes
    alembic_meshes.clear()
    # abc_list = list(glob.glob("D:\\alembicCar\\*"))
    # tem_name = os.path.basename(n).split('.')[0]
    # old_to_new_name
    
    t_start = time.time()
    car_meshes.clear()
    for ob in bpy.data.objects:
        _name = ob.name
        if ob.type == 'MESH' and not ob.name in alembic_meshes:
            alembic_meshes.append(ob.name)
        car_meshes[_name] = not bpy.data.objects[_name].hide_viewport
    t_end = time.time()
    print(f'Select all objects in scene: {t_end - t_start}, objects: {len(car_meshes)}')
    # print(alembic_meshes)
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


def assignee_material():
    print('Assigne Mat')
    global alembic_meshes 
    with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\MaterialAssignments.json', 'r') as config:
        t_config = config.read()
        g_config = json.loads(t_config)
        
        # print(f'Material: {g_config["A54_"]}')
        for key in g_config:
            try:
                mat = bpy.data.materials[key]        
            except:
                mat = bpy.data.materials.new(name=key)
            mat.use_nodes = True
            r = random.random()
            g = random.random()
            b = random.random()
            m = random.random()
            roug = random.random()
            ior = random.random() * random.randint(1, 3)
            principled_node = mat.node_tree.nodes.get('Principled BSDF')
            principled_node.inputs[0].default_value = (r, g, b, 1)
            principled_node.inputs[1].default_value = m
            principled_node.inputs[2].default_value = roug
            principled_node.inputs[3].default_value = ior
            principled_node.inputs[0].default_value = (.1, .1, .1, 1)
        
        
            for value in g_config[key]:
                mesh_name = str(value).split('/')[-1]
                if mesh_name == '_NML37753545_AA_021_FR_BMPR_Styling220218_Without_LIC_1052497_09':
                    h = len(mesh_name) + 1
                    temp = min(63, h)
                    print(f'Name: {mesh_name} to new name: {mesh_name[:min(63, h)]} h:{h}')
                    pass
                # print(f'Material: {key}, Meshe: {mesh}')
                try:
                    h = len(mesh_name) + 1
                    # print(f'\n\n\n Changed name from {mesh_name} to {mesh_name[:min(63, h)]}, h: {h}\n\n\n')
                    mesh_name = mesh_name[:min(63, h)]
                    mesh = bpy.data.objects[mesh_name]
                    mesh.active_material = mat
                    if mesh_name in alembic_meshes:
                        alembic_meshes.remove(mesh_name)
                except:
                    try:
                        parent_mesh_name = str(value).split('/')[-2]
                        h = len(parent_mesh_name)
                        parent_mesh_name = parent_mesh_name[:min(63, h)]
                        mesh = bpy.data.objects[parent_mesh_name]
                        mesh.active_material = mat
                        if mesh_name in alembic_meshes:
                            alembic_meshes.remove(mesh_name)    
                        # print(f'Name changed from {mesh_name} to {parent_mesh_name}. Material changed.')
                    except:
                        print(f"Mesh: {mesh_name} or {parent_mesh_name} doesn't exsist on scene")
            
        print('Finished easy part')
            
        for ob in bpy.data.objects:
            pattern = '[a-zA-Z0-9_]+'
            _name = f'{ob.name.split(".")[0]}{pattern}'
            if ob.type == 'MESH' and ob.name in alembic_meshes:
                for key in g_config:
                    for value in g_config[key]:
                        if re.findall(_name, value):
                            try:
                                mat = bpy.data.materials[key]
                                mesh = bpy.data.objects[ob.name]
                                mesh.active_material = mat    
                                if ob.name in alembic_meshes:
                                    alembic_meshes.remove(ob.name)
                            except:
                                print('Something went wrong')
                            break
                        
        print(alembic_meshes)
        with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\Test_meshes.txt', 'w+') as dt:
            for n in alembic_meshes:
                dt.write(f'{n}\n')
        
        
        
        # metaVariant = g_config['metaVariantSets']
        # preset = metaVariant["Preset"]
        # int_variants = preset["variants"]
        # for key, value in int_variants.items():
        #     usdVariants = value["usdVariants"]
        #     for key, value in usdVariants.items():
        #         tempPath = str(key).split('/')[0]
        #         temp = str(value["variantSet"])
        #         if tempPath == 'CHASSIS':
        #             mesh = bpy.data.objects[temp]
        #             mesh.active_material = mat_chassis
        #         if tempPath == 'EXTERIOR':
        #             mesh = bpy.data.objects[temp]
        #             mesh.active_material = mat_exterior
        #         if tempPath == 'INTERIOR':
        #             mesh = bpy.data.objects[temp]
        #             mesh.active_material = mat_interior


def create_and_parent(whole_data: str):
    memo = {}
    pattern = f'(def Xform [ "A-Za-z_]+)'
    loc_pattern = f'double3 xformOp:translate = [()-? 0-9.,e]+'
    rot_pattern = f'float3 xformOp:rotateXYZ = [()-? 0-9.,e]+'
    buf = whole_data.splitlines()
    for n in buf:
        temp = re.findall(pattern, n)
        loc_temp = re.findall(loc_pattern, n)
        rot_temp = re.findall(rot_pattern, n)
        if temp:
            indent = n.index(temp[0])
            temp_name = temp[0].strip().split('"')[-2]
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
            memo[indent] = temp_name
        if loc_temp:
            str_vector = loc_temp[0][:-1].split('(')[-1]
            # print(f"str_vector :{str_vector}")
            # print(f'VECTOR           : {str_vector}')
            x,y,z = str(str_vector).split(',')
            # print(f'X: {x}, y: {y}, z: {z}')
            temp_obj.location = (float(x), -float(z), float(y))
        if rot_temp:
            # print(f"Rot :{rot_temp[0]}")
            str_vector = rot_temp[0][:-1].split('(')[-1]
            # print(f'VECTOR           : {str_vector}')
            # print(f"str_vector :{str_vector}")
            x,y,z = str(str_vector).split(',')
            # print(f'X: {x}, y: {y}, z: {z}')
            temp_obj.rotation_euler = (float(x), -float(z), float(y))
    return memo


def create_rig():
    pattern = f'(def Xform [ "A-Za-z_]+)'
    # loc_pattern = f'double3 xformOp:translate = [() -0-9.,)]+'
    # rot_pattern = f'float3 xformOp:rotateXYZ = [() -0-9.,)]+'
    with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\RigData3.usda', 'r') as data:
        whole_data = data.read()
        idx = whole_data.index('def Xform "RIG_Main"') -1 
        last_bracket_idx = whole_data.rindex('}')
        out = re.findall(pattern, whole_data[idx:last_bracket_idx])
        i_name = str(out[0][:-1]).strip().split('"')[-1]
        if not i_name:
            i_name  = str(out[0][:-1]).strip().split('"')[-2]
        create_and_parent(whole_data[idx: last_bracket_idx])
        
    # print("BBBBBBBBBBB")
        
        

