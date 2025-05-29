bl_info = {
    "name": "Auto Texture Baker",
    "author": "maythas_w maythas.wangcharoenwong@gmail.com",
    "version": (0,0,1),
    "blender": (2,8,0),
    "description" : "Automatically bakes selected object's material into texture",
    "category" : "Material",
}

# IMPORTS
import bpy
from .src.property_group.bake_settings import PG_bake_settings
from .src.ui import PROPERTIES_PT_bake_panel
from .src.operators import MATERIAL_OT_bake_textures

classes = (PG_bake_settings, PROPERTIES_PT_bake_panel, MATERIAL_OT_bake_textures)

def register():
    for cls in classes: 
        bpy.utils.register_class(cls)
 
    # Setup props
    bpy.types.Scene.pg_bake_settings = bpy.props.PointerProperty(type=PG_bake_settings)

def unregister():
    # Cleanup props
    del bpy.types.Scene.pg_bake_settings

    for cls in classes: 
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
