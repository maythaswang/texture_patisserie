"""
Property Group for storing bake settings
"""

import bpy

class PG_bake_settings(bpy.types.PropertyGroup):
    """Property Group for bake settings"""

    albedo: bpy.props.BoolProperty(name="Albedo", default = True)
    roughness: bpy.props.BoolProperty(name="Roughness", default = True)
    metallic: bpy.props.BoolProperty(name="Metallic", default = True)
    normal: bpy.props.BoolProperty(name="Normal", default = True)