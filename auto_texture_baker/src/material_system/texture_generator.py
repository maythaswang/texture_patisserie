"""
This module handles generating texture and texture nodes for baking
"""
import bpy

def create_texture_single(name, bake_type, width, height, color_space):
    """
    Generate new texture and define a new name for baking materials
    """

    # Define Texture name    
    texture_name = f"tmp_{name}_{bake_type}"

    # Create Texture
    bake_image = bpy.data.images.new(texture_name, width=width, height=height)
    bake_image.colorspace_settings.name = color_space

    # Configure Image texture 
    # TODO: Fix this, the output does not reflect this value at all.
    bake_image.alpha_mode = 'STRAIGHT'
    bake_image.file_format = 'PNG'

    return bake_image

def create_texture_node(material, bake_image):
    """
    Create texture nodes in the material and hook up the image texture
    with material and bake_image

    Parameters: 
    material(bpy.types.Material):   Material where the texture node will be created
    bake_image(bpy.types.Image):    Image where the result is baked to 
    """

    # Create nodes 
    nodes = material.node_tree.nodes
    tex_image_node = nodes.new(type='ShaderNodeTexImage')

    # Assign image to the texture node
    tex_image_node.image = bake_image

    # Select as active node
    tex_image_node.select = True
    nodes.active = tex_image_node
