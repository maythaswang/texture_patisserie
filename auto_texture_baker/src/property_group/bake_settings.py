"""
Property Group for storing bake settings
"""

import bpy

# pylint: disable=C0103
class PG_bake_settings(bpy.types.PropertyGroup):
    """
    Property Group for bake settings
    """
    
    albedo: bpy.props.BoolProperty(name="albedo", default = True)
    roughness: bpy.props.BoolProperty(name="roughness", default = True)
    metallic: bpy.props.BoolProperty(name="metallic", default = True)
    normal: bpy.props.BoolProperty(name="normal", default = True)

    # Batching options

    bake_grouping_options_items= [
        ("bake_batch", "Bake Batch", "Bake multiple objects into the same texture"),
        ("bake_separate_obj", "Bake Separate Object", "Bake each objects separately into different textures"),
    ]
    
    bake_grouping_options: bpy.props.EnumProperty(
        name="Bake Grouping Options",
        description="Choose the options based on how you prefer the output textures are grouped",
        items = bake_grouping_options_items,
        default="bake_batch"
    )

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

    # Naming conventions
    naming_convention_items = [
        ('name_type_text1_text2', 'Name, Type, Text1, Text2', 'Choose the preferred naming convention'),
        ('text1_name_type_text2', 'Text1, Name, Type, Text2', 'Choose the preferred naming convention'),
        ('text1_text2_name_type', 'Text1, Text2, Name, Type', 'Choose the preferred naming convention'),
        ('text1_type_name_text2', 'Text1, Type, Name, Text2', 'Choose the preferred naming convention'),
    ]

    naming_convention: bpy.props.EnumProperty(
        name="Naming Convention",
        description="Choose the preferred naming convention for the output texture",
        items=naming_convention_items, 
        default="name_type_text1_text2"
    )

    output_name_text1: bpy.props.StringProperty(name="output_name_text1", default="")
    output_name_text2: bpy.props.StringProperty(name="output_name_text2", default="")
    output_name_separator: bpy.props.StringProperty(name="output_name_separator", default="_")
    batch_name_override: bpy.props.BoolProperty(name="batch_name_override", default = False)
    batch_name: bpy.props.StringProperty(name="batch_name", default="batch")

    # Override texture names 
    texture_type_name_override: bpy.props.BoolProperty(name="texture_type_name_override", default=False)
    output_albedo_name:     bpy.props.StringProperty(name="output_albedo_name", default = "albedo")
    output_roughness_name:  bpy.props.StringProperty(name="output_roughness_name", default= "roughness")
    output_metallic_name:   bpy.props.StringProperty(name="output_metallic_name", default = "metallic")
    output_normal_name:     bpy.props.StringProperty(name="output_normal_name", default = "normal")
