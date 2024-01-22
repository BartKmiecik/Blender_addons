#----------------------------------------------------------
# File __init__.py
#----------------------------------------------------------
#
# The user interface is created in the "right" panel in the 3D View
# This panel is normally closed, so it must be opened (+) to be seen.
#
 
#    Addon info
bl_info = {
  "name": "Multifile",
  'author': 'Based on work by Thomas Larsson',
  "location": "View3D &gt; UI panel &gt; Add meshes",
   "category": "3D View"
  }

# To support reload properly, try to access a package var, 
# if it's there, reload everything
if "bpy" in locals():
  import imp
  imp.reload(mycube)
  imp.reload(mysphere)
  imp.reload(mycylinder)
  print("Reloaded multifiles")
else:
  import mycube, mysphere, mycylinder
  print("Imported multifiles")

import bpy
from bpy.props import *

#
#   class AddMeshPanel(bpy.types.Panel):
#
class AddMeshPanel(bpy.types.Panel):
  bl_label = "Add meshes"
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"

  def draw(self, context):
    self.layout.operator("multifile.add", text="Add cube").mesh = "cube"
    self.layout.operator("multifile.add", text="Add cylinder").mesh = "cylinder"
    self.layout.operator("multifile.add", text="Add sphere").mesh = "sphere"

#
#   class OBJECT_OT_AddButton(bpy.types.Operator):
#
class OBJECT_OT_AddButton(bpy.types.Operator):
  bl_idname = "multifile.add"
  bl_label = "Add"
  mesh = bpy.props.StringProperty()

  def execute(self, context):
    if self.mesh == "cube":
      mycube.makeMesh(-8)
      print ("Added a cube")
    elif self.mesh == "cylinder":
      mycylinder.makeMesh(-5)
      print ("Added a cylinder")
    elif self.mesh == "sphere":
      mysphere.makeMesh(-2)
      print ("Added a sphere")
    return{'FINISHED'}    

#
#    Registration
#

def register():
  print ("Registering ", __name__)
  bpy.utils.register_module(__name__)

def unregister():
  print ("Unregistering ", __name__)
  bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
  register()