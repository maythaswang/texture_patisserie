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

    bake_width: bpy.props.IntProperty(name="bake_width", default=1024, description="Output texture width", min=4)
    bake_height: bpy.props.IntProperty(name="bake_height", default=1024, description="Output texture height", min=4)
    save_to_disk: bpy.props.BoolProperty(name="save_to_disk", default=False)
    output_path: bpy.props.StringProperty(name="output_path",subtype="DIR_PATH", default= "//baked_textures/")

    render_samples: bpy.props.IntProperty(name="render_samples", default=10, description="Render samples", min=1)

    file_type_items = [
        ('PNG', "PNG", "Portable Network Graphics (PNG)"),
        ('JPEG', "JPEG", "Joint Photographic Experts Group (JPEG)"),
        ('TIFF', "TIFF", "Tagged Image File Format (TIFF)"),
        ('BMP', "BMP", "Bitmap Image Format (BMP)"),
        ('EXR', "EXR", "OpenEXR Image Format (EXR)")
    ]

    file_type: bpy.props.EnumProperty(
        name="File Type", 
        description="Choose the file type for saving the texture",
        items=file_type_items, 
        default='PNG'
    )