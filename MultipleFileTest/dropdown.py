from bpy.types import Operator
from bpy.props import EnumProperty
from . import utility

class DropdownOperator(Operator):
    bl_idname = 'test.dropdown'
    bl_label = 'Select EIM'

    eim_list = utility.read_all_emis()
    temp_enum = []
    for i in range(len(eim_list)):
        temp_enum.append((eim_list[i], eim_list[i], eim_list[i]))
        # print(f'EIM: {i}, {eim_list[i]}, {eim_list[i]}')
    

    my_enum: EnumProperty(
        name= '',
        description='Select option',
        items = temp_enum
    )

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "my_enum")

    def execute(self, context):
        option = self.my_enum
        print(f'EIM SELECTED: {option}')
        variant = utility.use_dll(eim = option)
        utility.select_variant(variant=variant)
        return {'FINISHED'}