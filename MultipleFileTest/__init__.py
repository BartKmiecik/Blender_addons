import glob, sys, time, math, random, asyncio, bpy, os
from bpy.props import EnumProperty
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy.utils import register_class, unregister_class
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from . import utility
# import test_package
# import logging
# pkg_dir = "D:\\BlenderAddons\\Maker\\testpackage\\utilit_material" 
# sys.path.append(pkg_dir)
# print(f'AAAAAAAAAAAA path: {sys.path}')

bl_info = {
	'name': 'BARTOS',
	'description': 'Various tools for handle geodata',
	'author': 'BARTOS',
	'license': 'GPL',
	'deps': '',
	'version': (2, 2, 8),
	'blender': (2, 83, 0),
	'location': 'View3D > Tools > BARTOS',
	'warning': '',
	'wiki_url': 'https://github.com/BARTOS/BlenderGIS/wiki',
	'tracker_url': 'https://github.com/BARTOS/BlenderGIS/issues',
	'link': '',
	'support': 'COMMUNITY',
	'category': '3D View'
}

class TEST_OT_test_op(Operator, AddObjectHelper):
    bl_idname = 'test.test_op'
    bl_label = 'Test'
    bl_description = 'Test'
    bl_options = {'REGISTER', 'UNDO'}


    object_to_hide = []
    car_meshes = {}
    action: EnumProperty(
        items=[
            ('ADD_CUBE', 'add cube', 'add cube'),
            ('REMOVE_CUBE', 'remove object', 'remove object'),
            ("RANDOM_MOVE", 'move object', 'move object'),
            ("DIFF_MATERIAL", 'diff mat', 'diff mat'),
            ("ABC_IMPORT", 'abc import', 'abc import'),
            ("ABC_ASIMPORT", 'abc asimport', 'abc asimport'),
            ("GET_ALL", 'get all', 'get all'),
            ("HIDE_RANDOM", 'hide random', 'hide random'),
            ("UNHIDE_RANDOM", 'unhide random', 'unhide random'),
            ("SAVE_SCENE", 'save scene', 'save scene'),
    ]
)

    def execute(self, context):
        if self.action == 'ADD_CUBE':
            self.add_cube(context=context)
        elif self.action == 'REMOVE_CUBE':
            _obj = bpy.context.selected_objects
            self.remove_object(context=context, obj_to_remove=_obj)
        elif self.action == 'RANDOM_MOVE':
            _obj = bpy.context.selected_objects
            self.randomMove(context, _obj)
        elif self.action == 'DIFF_MATERIAL':
            _obj = bpy.context.object
            self.diffMate(context, _obj)
        elif self.action == 'ABC_IMPORT':
            self.abc_import_synconus(self, context)
        elif self.action == 'ABC_ASIMPORT':
            asyncio.run(self.abc_import_assync(context))
        elif self.action == 'GET_ALL':
            self.get_all(self)
        elif self.action == 'HIDE_RANDOM':
            self.hide_random_third_of_car(self, context)
        elif self.action == 'UNHIDE_RANDOM':
            self.unhide_random_third_of_car(self, context)
        elif self.action == 'SAVE_SCENE':
            self.save_scene(context)
        return {'FINISHED'}
 
    @staticmethod
    def remove_object(context, obj_to_remove):
        utility.remove_object(context, obj_to_remove)
 
    @staticmethod
    def add_cube(context):
        utility.add_cube(context)
 
    
    @staticmethod
    def randomMove(context, cube):
        utility.randomMove(context, cube)
    
    @staticmethod
    def diffMate(context, cube):
        utility.diffMate(context, cube)
    
    @staticmethod
    def abc_import_synconus(self, context):
        utility.abc_import_synconus(self, context)

    @staticmethod
    async def abc_import_assync(context):
        utility.abc_import_assync(context)
    

    def get_all(self,context):
        utility.get_all(self, context)

    def get_random_car_part(self):
        rand_obj = utility.get_random_car_part(self)
        return rand_obj

    @staticmethod
    def hide_random_third_of_car(self, context):
        utility.hide_random_third_of_car(self, context)
        
    @staticmethod
    def unhide_random_third_of_car(self, context):
        utility.unhide_random_third_of_car(self, context)
        

    @staticmethod
    def save_scene(context, filepath = 'D:\BlenderAddons\Scenes\Test'):
        utility.save_scene(context, filepath)
        


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
        row.operator('test.test_op', text='Move').action = 'RANDOM_MOVE'
        row = layout.row()
        row.operator('test.test_op', text='Random material').action = 'DIFF_MATERIAL'
        row = layout.row()
        row.operator('test.test_op', text='Import sync alembics').action = 'ABC_IMPORT'
        row = layout.row()
        row.operator('test.test_op', text='Import async alembics (NOT WORKING YET)').action = 'ABC_ASIMPORT'
        row = layout.row()
        row.operator('test.test_op', text='Get all').action = 'GET_ALL'
        row = layout.row()
        row.operator('test.test_op', text='Hide random').action = 'HIDE_RANDOM'
        row = layout.row()
        row.operator('test.test_op', text='Unhide all').action = 'UNHIDE_RANDOM'
        row = layout.row()
        row.operator('test.test_op', text='Save scene').action = 'SAVE_SCENE'

# def add_object_manual_map():
#    url_manual_prefix = "https://docs.blender.org/manual/en/latest/BARTOS"
#    url_manual_mapping = (
#        ("bpy.ops.mesh.add_object", "scene_layout/object/BARTOS/types.html"),
#    )
#    return url_manual_prefix, url_manual_mapping

def register():
    register_class(TEST_OT_test_op)
    register_class(Test_Panel)
    # bpy.utils.register_manual_map(add_object_manual_map)


def unregister():
    unregister_class(TEST_OT_test_op)
    register_class(Test_Panel)
    # bpy.utils.register_manual_map(add_object_manual_map)


# register()


if __name__ == "__main__":
	register()
