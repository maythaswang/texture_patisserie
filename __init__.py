"""
TEXTURE PATISSERIE - BLENDER ADDON
"""    

bl_info = {
    "name": "Texture Patisserie",
    "author": "maythas_w maythas.wangcharoenwong@gmail.com",
    "version": (0,0,2),
    "blender": (2,8,0),
    "description" : "Automatically bakes selected object's material into texture",
    "category" : "Material",
}

# IMPORTS
# pylint: disable=C0413
import bpy
from .src.property_group.bake_settings import PG_bake_settings
from .src.operators import MATERIAL_OT_bake_textures
from .src.ui import PROPERTIES_PT_bake_panel

classes = (PG_bake_settings, PROPERTIES_PT_bake_panel, MATERIAL_OT_bake_textures)

def register():
    """
    Registers all blender classes
    """

    for cls in classes: 
        bpy.utils.register_class(cls)
 
    # Setup props
    bpy.types.Scene.pg_bake_settings = bpy.props.PointerProperty(type=PG_bake_settings)

def unregister():
    """
    Unregsiter all blender classes 
    """

    # Cleanup props
    del bpy.types.Scene.pg_bake_settings

    for cls in classes: 
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
