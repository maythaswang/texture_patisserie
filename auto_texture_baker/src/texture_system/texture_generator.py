"""
This module handles generating texture and texture nodes for baking
"""
import bpy

# Set material to material slot at mat_id
# TODO: Move this to another module
def link_material(obj, mat_id, material) -> None:
    """Link material to object"""
    obj.data.materials[mat_id] = material
    obj.material_slots[mat_id].material = material

def create_texture_single(name, bake_type, width, height, color_space):
    """Generate new texture for baking all mats of same obj"""
    bake_image = bpy.data.images.new(f"tmp_{name}_{bake_type}", width=width, height=height)
    bake_image.colorspace_settings.name = color_space
    return bake_image

def create_texture_node(material, bake_image):
    """Create texture nodes in the material and hook up the image texture"""
    nodes = material.node_tree.nodes
    tex_image_node = nodes.new(type='ShaderNodeTexImage')
    tex_image_node.image = bake_image
    tex_image_node.select = True
    nodes.active = tex_image_node
