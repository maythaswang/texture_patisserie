"""
Property Group for storing bake settings
"""

import bpy

class PG_bake_settings(bpy.types.PropertyGroup):
    """Property Group for bake settings"""

    albedo: bpy.props.BoolProperty(name="albedo", default = True)
    roughness: bpy.props.BoolProperty(name="roughness", default = True)
    metallic: bpy.props.BoolProperty(name="metallic", default = True)
    normal: bpy.props.BoolProperty(name="normal", default = True)

    bake_width: bpy.props.IntProperty(name="bake_width", default=1024, description="Output texture width")
    bake_height: bpy.props.IntProperty(name="bake_height", default=1024, description="Output texture height")
    save_to_disk: bpy.props.BoolProperty(name="save_to_disk", default=False)
    output_path: bpy.props.StringProperty(name="output_path",subtype="DIR_PATH", default= "//baked_textures/")