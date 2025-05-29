"""
This module manage setting up material connections
"""
from typing import Any
from . import *
from ..utils import *

class MaterialEditor: 
    """
    Handles common action regarding creating, deleting, duplicating materials. 
    
    Attributes:

    """

    def __init__(self): 
        """
        Initialize MaterialEditor Object
        """

    def duplicate_material(self, obj) -> list[Any]:
        """Duplicate materials to be baked"""
        duplicate_materials = []
        for mat_id, slot in enumerate(obj.material_slots):
            # Material Validation
            material = slot.material
            mat_valid, err_msg = validator.is_bakeable_mat(material)
            if not mat_valid: 
                # self.report({"ERROR"}, err_msg)
                continue

            # Duplicate material
            dupe_mat = material.copy()
            dupe_mat.name = f"BAKE_{material.name}"
            self.material_stack.append((mat_id, material, dupe_mat))

            # Prepare to modify metallic connection
            metallic_connection = MetallicConnection(dupe_mat) # DEBUG
            metallic_connection.prepare_metallic_values()

            duplicate_materials.append((dupe_mat, metallic_connection))

            # Link Material
            self._link_material(obj, mat_id, dupe_mat)
            # self.report({'INFO'}, f"Duplicating material {material.name}")

        return duplicate_materials


    def _link_material(self,obj, mat_id, material) -> None:
        """Link material to object"""
        obj.data.materials[mat_id] = material
        obj.material_slots[mat_id].material = material  

def link_material(obj, mat_id, material) -> None:
    """Link material to object"""
    obj.data.materials[mat_id] = material
    obj.material_slots[mat_id].material = material  