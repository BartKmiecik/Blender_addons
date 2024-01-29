from bpy.types import Operator
from bpy.props import EnumProperty
from . import utility_variants


class DropdowCarpaints(Operator):
    bl_idname = 'test.dropdown_carpaint'
    bl_label = 'Select Carpaint'
    
    eim_list = utility_variants.read_all_carpaints()
    temp_enum = []
    for i in range(len(eim_list)):
        temp_enum.append((eim_list[i], eim_list[i], eim_list[i]))  

    carpaints: EnumProperty(
        name= '',
        description='Select carpaint',
        items = temp_enum
    )

    selected_carpaint = '---'
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "carpaints")

    def execute(self, context):
        self.__class__.selected_carpaint = self.carpaints
        self.report({'INFO'}, str(self.__class__.selected_carpaint))
        print(f'Carpaint SELECTED: {self.selected_carpaint}')
        utility_variants.change_car_paint(car_paint=self.selected_carpaint)
        return {'FINISHED'}