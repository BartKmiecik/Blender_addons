import bpy
from . import dropdown_eim, dropdown_carpaints, dropdown_interior_trim

class Side_Panel(bpy.types.Panel):
    bl_label = "Katana Panel"
    bl_idname = "PT_TestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Katana'
    
    def draw(self, context):
        layout = self.layout
        # layout.row().label(text="Spawn Cube", icon='CUBE')
        # layout.row().operator('test.test_op', text='Add Cube').action = 'ADD_CUBE'
        # layout.row().operator('test.test_op', text='Remove Cube').action = 'REMOVE_CUBE'
        # layout.row().operator('test.test_op', text='Move').action = 'RANDOM_MOVE'        
        layout.row().operator('test.test_op', text='Import sync alembics').action = 'ABC_IMPORT'
        layout.row().operator('test.test_op', text='Random material').action = 'DIFF_MATERIAL'   
        layout.row().operator('test.test_op', text='Get all').action = 'GET_ALL'
        # layout.row().operator('test.test_op', text='Import async alembics (NOT WORKING YET)').action = 'ABC_ASIMPORT'
        layout.row().operator('test.test_op', text='Hide random').action = 'HIDE_RANDOM'
        layout.row().operator('test.test_op', text='Unhide all').action = 'UNHIDE_RANDOM'
        # layout.row().operator('test.test_op', text='Use Dll').action = 'USE_DLL'
        layout.row().operator('test.test_op', text='Select Variant').action = 'SELECT_VARIANT'
        layout.row().operator('test.test_op', text='Fake Materials').action = 'FAKE_MATERIALS'
        layout.row().operator('test.test_op', text='Save scene').action = 'SAVE_SCENE'
        layout.row().label(text=f'EIM: {str(dropdown_eim.DropdownEIM.selected_eim)}')
        layout.row().operator('test.dropdown_eim', text='Select EIM')
        layout.row().label(text=f'Carpaint: {str(dropdown_carpaints.DropdowCarpaints.selected_carpaint)}')
        layout.row().operator('test.dropdown_carpaint', text='Select Carpaint')
        layout.row().label(text=f'Interior Trim: {str(dropdown_interior_trim.DropdownInteriorTrim.selected_interior_trim)}')
        layout.row().operator('test.dropdown_interior_trim', text='Select Interior Trim')


class Test_Panel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_select"
    bl_label = "Select"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="My Select Panel")

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Selection Tools")
        box.operator("object.select_all").action = 'TOGGLE'
        row = box.row()
        row.operator("object.select_all").action = 'INVERT'
        row.operator("object.select_random")