from bpy.types import Operator
from bpy.props import EnumProperty
from . import utility


class DropdownEIM(Operator):
    bl_idname = 'test.dropdown_eim'
    bl_label = 'Select EIM'
    
    eim_list = utility.read_all_emis()
    temp_enum = []
    for i in range(len(eim_list)):
        temp_enum.append((eim_list[i], eim_list[i], eim_list[i]))  

    car_eims: EnumProperty(
        name= '',
        description='Select EIM',
        items = temp_enum
    )

    selected_eim = '---'
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "car_eims")

    def execute(self, context):
        self.__class__.selected_eim = self.car_eims
        self.report({'INFO'}, str(self.__class__.selected_eim))
        print(f'EIM SELECTED: {self.selected_eim}')
        variant = utility.use_dll(eim = self.selected_eim)
        utility.select_variant(variant=variant)
        return {'FINISHED'}