import bpy, json, random, ctypes, time
from ctypes import *

car_meshes = {}
curent_car_paint = 'GAT'
curent_interior_trim = 'A'
curent_eim = 'GLVALG2Z34ZUA-----'


def get_all():
    t_start = time.time()
    car_meshes.clear()
    for ob in bpy.data.objects:
        _name = ob.name
        car_meshes[_name] = not bpy.data.objects[_name].hide_viewport
    t_end = time.time()
    print(f'Select all objects in scene: {t_end - t_start}, objects: {len(car_meshes)}')
    return car_meshes


def use_dll(interior = curent_interior_trim, carpaint = curent_car_paint, eim = curent_eim):
    global curent_interior_trim, curent_car_paint, curent_eim
    curent_interior_trim = interior
    curent_car_paint = carpaint
    curent_eim = eim
    with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\ConfigJson.json', 'r') as config:
        t_config = config.read()
        g_config = json.loads(t_config)
        h_config = json.dumps(g_config).encode("utf-8")
        with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\Selections.json', 'r') as selection:
            t_sel = selection.read()
            g_selection = json.loads(t_sel)
            g_selection["Preset"] = eim
            g_selection["Paint"] = carpaint
            g_selection["Interior"] = interior
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
        elif state == 'off':
            state = False
        try:
            if type(state) == bool:
                bpy.data.objects[part].hide_viewport = not state
        except:
            print(f"Mesh: {part}, doesn't exist in scene")
        t_end = time.time()
        
    print(f'Select variant, took: {t_end - t_start} sec')


def change_car_paint(car_paint = 'GAT'):
    try:
        mat_exterior = bpy.data.materials[car_paint]        
    except:
        mat_exterior = bpy.data.materials.new(name=car_paint)
        mat_exterior.use_nodes = True
        r = random.random()
        g = random.random()
        b = random.random()
        m = random.random()
        roug = random.random()
        ior = random.random() * random.randint(1, 3)
        principled_node = mat_exterior.node_tree.nodes.get('Principled BSDF')
        principled_node.inputs[0].default_value = (r, g, b, 1)
        principled_node.inputs[1].default_value = m
        principled_node.inputs[2].default_value = roug
        principled_node.inputs[3].default_value = ior

    with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\ConfigJson.json', 'r') as config:
        t_config = config.read()
        g_config = json.loads(t_config)
        metaVariant = g_config['metaVariantSets']
        preset = metaVariant["Preset"]
        int_variants = preset["variants"]
        for key, value in int_variants.items():
            usdVariants = value["usdVariants"]
            for key, value in usdVariants.items():
                tempPath = str(key).split('/')[0]
                temp = str(value["variantSet"])
                if tempPath == 'EXTERIOR':
                    try:
                        mesh = bpy.data.objects[temp]
                        mesh.active_material = mat_exterior
                    except:
                        print(f"Mesh: {temp} doesn't exsist on scene")

def change_interior_trim(interior_trim = 'A'):
    result = use_dll(interior=interior_trim)
    result = json.loads(result)
    for i in result:
        temp_path = str(i["Path"]).split('/')
        if temp_path[0] == "Materials" and temp_path[1] != 'Colors':
            mat_name = i["State"]
            mesh_name = i["Variant"]
            try:
                mat_interior = bpy.data.materials[mat_name]        
            except:
                mat_interior = bpy.data.materials.new(name=mat_name)
                mat_interior.use_nodes = True
                r = random.random()
                g = random.random()
                b = random.random()
                m = random.random()
                roug = random.random()
                ior = random.random() * random.randint(1, 3)
                principled_node = mat_interior.node_tree.nodes.get('Principled BSDF')
                principled_node.inputs[0].default_value = (r, g, b, 1)
                principled_node.inputs[1].default_value = m
                principled_node.inputs[2].default_value = roug
                principled_node.inputs[3].default_value = ior
                try:
                    mesh = bpy.data.objects[mesh_name]
                    mesh.active_material = mat_interior
                except:
                    print(f"Mesh: {mesh_name} doesn't exist in scene")
                        
            
def read_all_emis():
    eim_list = []
    with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\ConfigJson.json', 'r') as config:
        t_config = config.read()
        g_config = json.loads(t_config)
        metaVariant = g_config['metaVariantSets']
        preset = metaVariant["Preset"]
        int_variants = preset["variants"]
        for key, value in int_variants.items():
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
            eim_list.append(key)
    return eim_list


def read_all_interior_trim():
    eim_list = []
    with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\ConfigJson.json', 'r') as config:
        t_config = config.read()
        g_config = json.loads(t_config)
        metaVariant = g_config['metaVariantSets']
        preset = metaVariant["Interior"]
        int_variants = preset["variants"]
        for key, value in int_variants.items():
            eim_list.append(key)
    return eim_list

