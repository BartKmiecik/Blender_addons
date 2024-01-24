from bpy.types import Operator
from bpy.props import EnumProperty
from . import utility


class DropdownInteriorTrim(Operator):
    bl_idname = 'test.dropdown_interior_trim'
    bl_label = 'Select Carpaint'
    
    eim_list = utility.read_all_interior_trim()
    temp_enum = []
    for i in range(len(eim_list)):
        temp_enum.append((eim_list[i], eim_list[i], eim_list[i]))  

    interior_trims: EnumProperty(
        name= '',
        description='Select carpaint',
        items = temp_enum
    )

    selected_interior_trim = '---'
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "interior_trims")

    def execute(self, context):
        self.__class__.selected_interior_trim = self.interior_trims
        self.report({'INFO'}, str(self.__class__.selected_interior_trim))
        print(f'Interior SELECTED: {self.selected_interior_trim}')
        variant = utility.use_dll(interior = self.selected_interior_trim)
        utility.select_variant(variant=variant)
        return {'FINISHED'}