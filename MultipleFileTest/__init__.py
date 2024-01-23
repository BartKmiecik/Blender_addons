from bpy.utils import register_class, unregister_class
from . import ui_panel, view_model

bl_info = {
	'name': 'Katana',
	'description': 'Various katana tools',
	'author': 'BK',
	'version': (0, 0, 1),
	'blender': (2, 83, 0),
	'support': 'COMMUNITY',
	'category': '3D View'
}


CLASSES_TO_REGISTER = ['view_model.ViewModelOperator', 'ui_panel.Side_Panel']

def register():
    for n in CLASSES_TO_REGISTER:
        register_class(eval(n))


def unregister():
    for n in CLASSES_TO_REGISTER:
        unregister_class(eval(n))


if __name__ == "__main__":
	register()
