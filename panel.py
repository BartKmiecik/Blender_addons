import glob, sys, time, math, random, asyncio, bpy, os
from bpy.props import EnumProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
# import test_package
# import logging
# pkg_dir = "D:\\BlenderAddons\\Maker\\testpackage\\utilit_material" 
# sys.path.append(pkg_dir)
# print(f'AAAAAAAAAAAA path: {sys.path}')


class TEST_OT_test_op(Operator):
    bl_idname = 'test.test_op'
    bl_label = 'Test'
    bl_description = 'Test'
    bl_options = {'REGISTER', 'UNDO'}

    hided_obj = []
    action: EnumProperty(
        items=[
            ('ADD_CUBE', 'add cube', 'add cube'),
            ('REMOVE_CUBE', 'remove object', 'remove object'),
            ('CHANGE_MATERIAL', 'change material', 'change material'),
            ('HIDE_CUBE', 'hide object', 'hide object'),
            ("RANDOM_MOVE", 'move object', 'move object'),
            ("DIFF_MATERIAL", 'diff mat', 'diff mat'),
            ("ABC_IMPORT", 'abc import', 'abc import')
    ]
)

    def execute(self, context):
        if self.action == 'ADD_CUBE':
            self.add_cube(context=context)
        elif self.action == 'REMOVE_CUBE':
            _obj = bpy.context.selected_objects
            self.remove_object(context=context, obj_to_remove=_obj)
        elif self.action == 'HIDE_CUBE':
            print(f'Hide object BEFORE: {self.hided_obj}')
            _obj = bpy.context.selected_objects
            self.hide_object(self, context, _obj)
            print(f'Hide object AFTER: {self.hided_obj}')
        elif self.action == 'CHANGE_MATERIAL':
            _obj = bpy.context.selected_objects
            self.change_material(context, _obj)
        elif self.action == 'RANDOM_MOVE':
            _obj = bpy.context.selected_objects
            self.randomMove(context, _obj)
        elif self.action == 'DIFF_MATERIAL':
            _obj = bpy.context.object
            self.diffMate(context, _obj)
        elif self.action == 'ABC_IMPORT':
            self.abc_import_synconus(context)
        return {'FINISHED'}
 
    @staticmethod
    def remove_object(context, obj_to_remove):
        if obj_to_remove == None:
            obj_to_remove = bpy.context.selected_objects
        if obj_to_remove != None:
            bpy.ops.object.delete()
 
    @staticmethod
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
 
    @staticmethod
    def change_material(context, cube):
        if cube is None:
            cube = bpy.context.selected_objects
        if cube is not None:
            new_mat = bpy.data.materials.new(name="Material")
            new_mat.use_nodes = True
            bsdf = new_mat.node_tree.nodes["Principled BSDF"]
            color_ramp = new_mat.node_tree.nodes.new("ShaderNodeValToRGB")
            r, g, b = random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)
            color_ramp.color_ramp.elements[0].color = (r, g, b, 1)
            new_mat.node_tree.links.new(bsdf.inputs['Base Color'], color_ramp.outputs['Color'])

            for obj in cube:
                obj.data.materials[0] = new_mat
        
    @staticmethod
    def hide_object(self, context, cube):
        if cube is None or cube == []:
            # print(cube)
            # print('BBBBBBBBBBB not cube')
            cube = bpy.context.selected_objects
            # print(cube)
        if cube is not None:
            # print('CCCCCCCCCCCCCC not cube')
            # print(cube)
            # print(f'Obje name: {cube[0].hide_viewport}')
            hide = True
            if cube == []:
                # print(f'Empty cube: {cube} and hide obj: {self.hided_obj}')
                cube = self.hided_obj
                # print(f'Cube: {cube} and hide obj: {self.hided_obj}')
                print(f'Hided cube: {cube}')
                hide = False
            vis = hide
            if vis:
                # print(f'Adding cube: {cube} to hide object')
                self.hided_obj.append(cube)
                # print(f'Hide object: {self.hided_obj}')
            # print(f'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA {vis}')
            bpy.context.object.hide_viewport = vis
            if vis:
                self.hided_obj.remove(cube)
            # vis = bpy.context.object.visible_in_viewport_get
            # print(f'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA {vis}')
        return cube
    
    @staticmethod
    def randomMove(context, cube):
        if cube is None or cube == []:
            cube = bpy.context.selected_objects
        if cube is not None:
            x = random.randint(-10, 10)
            y = random.randint(-10, 10)
            z = random.randint(-10, 10)
            cube[0].location = (x, y, z)
    
    @staticmethod
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
    
    @staticmethod
    def abc_import_synconus(context):
        # print('Start')
        abc_list = list(glob.glob("D:\\alembicCar\\*"))
        # print('Globbed')
        print(abc_list[0])
        # print('First')
        # bpy.ops.wm.alembic_import(filepath=abc_list[0], relative_path=True, as_background_job=True)
        # obj = bpy.ops.wm.alembic_import(filepath=abc_list[0], relative_path=True, as_background_job=False)
        # temp_name = os.path.basename(abc_list[0])
        # print(f'Temp name: {temp_name}')
        # print(f'Object: {obj}')
        # print(f'Objec name: {obj.name}')
        t_start = time.time()
        for n in abc_list:
            # print(f'Importing: {n}')
            
            t = bpy.ops.wm.alembic_import(filepath=n, relative_path=True, as_background_job=False)
            try:
                tem_name = os.path.basename(n)
                obj = bpy.context.object
                obj.name = tem_name
            except:
                print('Missing mesh')
        t_end = time.time()

        print(f'Total importing time: {t_end - t_start}')
        


class Test_Panel(bpy.types.Panel):
    bl_label = "Test Panel"
    bl_idname = "PT_TestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NewTestTab'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.label(text="Spawn Cube", icon='CUBE')
        row = layout.row()
        row.operator('test.test_op', text='Add Cube').action = 'ADD_CUBE'
        row = layout.row()
        row.operator('test.test_op', text='Remove Cube').action = 'REMOVE_CUBE'
        row = layout.row()
        row.operator('test.test_op', text='Hide Cube').action = 'HIDE_CUBE'
        row = layout.row()
        row.operator('test.test_op', text='Change Material').action = 'CHANGE_MATERIAL'
        row = layout.row()
        row.operator('test.test_op', text='Move').action = 'RANDOM_MOVE'
        row = layout.row()
        row.operator('test.test_op', text='Diff Mat').action = 'DIFF_MATERIAL'
        row = layout.row()
        row.operator('test.test_op', text='Import alembics').action = 'ABC_IMPORT'


def register():
    register_class(TEST_OT_test_op)
    register_class(Test_Panel)


def unregister():
    unregister_class(TEST_OT_test_op)
    register_class(Test_Panel)

# if __name__ == "__main__":
#     print('Register Main')
#     register()


# def change_material():
#     cube = bpy.context.selected_objects
#     new_mat = bpy.data.materials.new(name="Material")
#     new_mat.use_nodes = True
#     bsdf = new_mat.node_tree.nodes["Principled BSDF"]
#     color_ramp = new_mat.node_tree.nodes.new("ShaderNodeValToRGB")
#     r, g, b = random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)
#     color_ramp.color_ramp.elements[0].color = (r, g, b, 1)
#     new_mat.node_tree.links.new(bsdf.inputs['Base Color'], color_ramp.outputs['Color'])

#     for obj in cube:
#         # obj.data.materials.append(new_mat)
#         obj.data.materials[0] = new_mat
#         # obj.active_material_index = len(cube.data.materials) - 1
        

# def create_cube():
#     cube = bpy.ops.mesh.primitive_cube_add(size=4, location=(0, 0, 0))
#     new_mat = bpy.data.materials.new(name="Material")
#     new_mat.use_nodes = True
#     bsdf = new_mat.node_tree.nodes["Principled BSDF"]
#     color_ramp = new_mat.node_tree.nodes.new("ShaderNodeValToRGB")
#     color_ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1)
#     new_mat.node_tree.links.new(bsdf.inputs['Base Color'], color_ramp.outputs['Color'])

#     cube = bpy.context.selected_objects
#     for obj in cube:
#         obj.data.materials.append(new_mat)


# print('Register Main')
register()

# create_cube()
# change_material()

