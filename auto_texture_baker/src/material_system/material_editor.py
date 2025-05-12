"""
This module manage setting up material connections
"""

def link_material(obj, mat_id, material) -> None:
    """Link material to object"""
    obj.data.materials[mat_id] = material
    obj.material_slots[mat_id].material = material
