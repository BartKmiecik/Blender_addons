import glob, sys, time, math, random, asyncio, bpy, os
from ctypes import *
import json, ctypes

object_to_hide = []
car_meshes = {}


def remove_object(context, obj_to_remove):
    if obj_to_remove == None:
        obj_to_remove = bpy.context.selected_objects
    if obj_to_remove != None:
        bpy.ops.object.delete()


def add_cube(context):
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
        print(cube)
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


async def abc_import_assync(context):
    abc_list = list(glob.glob("D:\\alembicCar\\*"))
    for n in abc_list:
        # print(f'Importing: {n}')
        batch = asyncio.gather(bpy.ops.wm.alembic_import(filepath=n, relative_path=True, as_background_job=True))
        resu = await batch
        try:
            tem_name = os.path.basename(n)
            obj = bpy.context.object
            obj.name = tem_name
        except:
            print('Missing mesh')


def get_all():
    t_start = time.time()
    car_meshes.clear()
    for ob in bpy.data.objects:
        _name = ob.name
        # print(f'NAAAAAAAAAAAAAAAAAAAME: {_name}')
        # print (ob.name)
        # print(f'Obj: {ob.name} is vis: {not bpy.data.objects[ob.name].hide_viewport}')
        car_meshes[_name] = not bpy.data.objects[_name].hide_viewport
    t_end = time.time()
    print(f'Select all objects in scene: {t_end - t_start}, objects: {len(car_meshes)}')


def get_random_car_part(self):
    avaliable_list = []
    for key, value in self.car_meshes.items():
        if value:
            avaliable_list.append(key)
    
    rand_int = random.randint(0, len(avaliable_list)-1)
    rand_obj = avaliable_list[rand_int]
    self.car_meshes[rand_obj] = False
    return rand_obj


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
    print(f'Unhide random one/third: {t_end - t_start}')    


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


def use_dll(eim = "GLVALG2Z34ZUA-----"):
    with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\ConfigJson2.json', 'r') as config:
        t_config = config.read()
        g_config = json.loads(t_config)
        h_config = json.dumps(g_config).encode("utf-8")
        with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\Selections.json', 'r') as selection:
            t_sel = selection.read()
            g_selection = json.loads(t_sel)
            g_selection["Preset"] = eim
            h_selection = json.dumps(g_selection).encode("utf-8")
            mydll = cdll.LoadLibrary('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\OutputCalculator.dll')
            mydll.CalculateOutput.argtypes = [c_char_p, c_char_p]
            mydll.CalculateOutput.restype = c_char_p
            result = mydll.CalculateOutput(c_char_p(h_config), c_char_p(h_selection))
            t_result = result.decode("utf-8")
            # print(f'Parts selected by dll: {t_result}')
            with open('D:\BlenderAddons\Blender_addons\Images\Test.txt', 'w+') as dt:
                dt.write(str(t_result))
    return t_result


def select_variant(variant):
    if len(car_meshes) == 0:
        get_all()
    t_start = time.time()
    t1 = json.loads(str(variant))
    for n in t1:
        part = n["Variant"]
        state = n["State"]
        if state == 'on':
            state = True
            bpy.data.objects[part].hide_viewport = not state
        elif state == 'off':
            state = False
            bpy.data.objects[part].hide_viewport = not state
        t_end = time.time()
    print(f'Select variant, took: {t_end - t_start} sec')


def assigne_mat(self):
    with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\ConfigJson.json', 'r') as config:
        t_config = config.read()
        g_config = json.loads(t_config)
        metaVariant = g_config['metaVariantSets']
        interior = metaVariant["Interior"]
        int_variants = interior["variants"]
        a_variants = int_variants["A"]
        var_set = a_variants["usdVariants"]
        # print(f'A variant: {a_variants["usdVariants"]}')
        for key, value in var_set.items():
            print(f'Matvariants config KEY       : {value["variant"]} \n')
            
            
def read_all_emis():
    eim_list = []
    with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\ConfigJson.json', 'r') as config:
        t_config = config.read()
        g_config = json.loads(t_config)
        metaVariant = g_config['metaVariantSets']
        preset = metaVariant["Preset"]
        int_variants = preset["variants"]
        for key, value in int_variants.items():
            print(f'Matvariants config KEY       : {key} \n')
            eim_list.append(key)
    return eim_list

            
def read_all_carpaints():
    eim_list = []
    with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\ConfigJson.json', 'r') as config:
        t_config = config.read()
        g_config = json.loads(t_config)
        metaVariant = g_config['metaVariantSets']
        preset = metaVariant["Paint"]
        int_variants = preset["variants"]
        for key, value in int_variants.items():
            print(f'Matvariants config KEY       : {key} \n')
            eim_list.append(key)
    return eim_list