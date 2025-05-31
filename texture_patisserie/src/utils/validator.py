"""
This module provide functions for validating whether an object, mesh, material is usable
"""

def is_bakeable_obj(obj) -> tuple[bool, str]: 
    """
    Validate whether the current object can be baked

    Parameter: 
    obj(bpy.types.Material) : Object that will have their material duplicated for baking purposes.

    Returns: 
    tuple[bool, str]: Success Status and Error message
    """
    
    # VALIDATE OBJECT IS BEING SELECTED
    if not obj or obj.type != "MESH":
        return False, "Invalid object selected"

    # VALIDATE MATERIAL EXISTENCE
    if not obj.data.materials:
        return False, "Object has no material"

    # VALIDATE UV EXISTENCE
    if not obj.data.uv_layers:
        return False, "Object has no UV map"

    return True, ""

def is_bakeable_mat(material):
    """
    Validate whether the current material can be baked

    Parameter: 
    material(bpy.types.Material) : Object that will have their material duplicated for baking purposes.

    Returns: 
    tuple[bool, str]: Success Status and Error message
    """

    if not material.use_nodes: 
        return False, "Material doesn't have any nodes."

    nodes = material.node_tree.nodes
    if not nodes:
        return False, "Material has no node tree"

    return True, ""
