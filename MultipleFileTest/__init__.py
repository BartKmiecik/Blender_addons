import asyncio, bpy
from bpy.props import EnumProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from . import utility

bl_info = {
	'name': 'Katana',
	'description': 'Various katana tools',
	'author': 'BK',
	'version': (0, 0, 1),
	'blender': (2, 83, 0),
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
    bl_label = "Katana Panel"
    bl_idname = "PT_TestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Katana'
    
    def draw(self, context):
        layout = self.layout
        layout.row().label(text="Spawn Cube", icon='CUBE')
        layout.row().operator('test.test_op', text='Add Cube').action = 'ADD_CUBE'
        layout.row().operator('test.test_op', text='Remove Cube').action = 'REMOVE_CUBE'
        layout.row().operator('test.test_op', text='Move').action = 'RANDOM_MOVE'        
        layout.row().operator('test.test_op', text='Random material').action = 'DIFF_MATERIAL'        
        layout.row().operator('test.test_op', text='Import sync alembics').action = 'ABC_IMPORT'
        layout.row().operator('test.test_op', text='Import async alembics (NOT WORKING YET)').action = 'ABC_ASIMPORT'
        layout.row().operator('test.test_op', text='Get all').action = 'GET_ALL'
        layout.row().operator('test.test_op', text='Hide random').action = 'HIDE_RANDOM'
        layout.row().operator('test.test_op', text='Unhide all').action = 'UNHIDE_RANDOM'
        layout.row().operator('test.test_op', text='Save scene').action = 'SAVE_SCENE'


CLASSES_TO_REGISTER = ['TEST_OT_test_op', 'Test_Panel']

def register():
    for n in CLASSES_TO_REGISTER:
        register_class(eval(n))


def unregister():
    for n in CLASSES_TO_REGISTER:
        unregister_class(eval(n))


if __name__ == "__main__":
	register()
