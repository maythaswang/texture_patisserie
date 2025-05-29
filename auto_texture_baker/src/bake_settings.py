"""
Property Group for storing bake settings
"""

import bpy

class PG_bake_settings(bpy.types.PropertyGroup):
    """
    Property Group for bake settings
    """

    albedo: bpy.props.BoolProperty(name="albedo", default = True)
    roughness: bpy.props.BoolProperty(name="roughness", default = True)
    metallic: bpy.props.BoolProperty(name="metallic", default = True)
    normal: bpy.props.BoolProperty(name="normal", default = True)

    bake_separately: bpy.props.BoolProperty(name="bake_separately", default=False)

    bake_width: bpy.props.IntProperty(name="bake_width", default=1024, description="Output texture width", min=4)
    bake_height: bpy.props.IntProperty(name="bake_height", default=1024, description="Output texture height", min=4)
    save_to_disk: bpy.props.BoolProperty(name="save_to_disk", default=False)
    output_path: bpy.props.StringProperty(name="output_path",subtype="DIR_PATH", default= "//baked_textures/")

    render_samples: bpy.props.IntProperty(name="render_samples", default=10, description="Render samples", min=1)
    render_device_items = [
        ("CPU","CPU","Use CPU for baking"),
        ("GPU","GPU","Use GPU for baking")
    ]

    render_device: bpy.props.EnumProperty(
        name="Rendering Device",
        description="Device to use for rendering",
        items=render_device_items,
        default="CPU"
    )

    file_type_items = [
        ("PNG", "PNG",  "Output image in PNG format"),
        ("JPEG", "JPEG", "Output image in JPEG format)"),
        ("TIFF", "TIFF", "Output image in TIFF format"),
        ("BMP", "BMP",  "Output image in BMP format"),
    ]

    file_type: bpy.props.EnumProperty(
        name="File Type", 
        description="Choose the file type for saving the texture",
        items=file_type_items, 
        default="PNG"
    )
