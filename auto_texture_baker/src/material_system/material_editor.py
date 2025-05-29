"""
This module manage setting up material connections
"""
from typing import Any
from collections import deque
import bpy

import auto_texture_baker.src.material_system as material_system
import auto_texture_baker.src.utils as utils


class MaterialEditor: 
    """
    Handles common action regarding creating, deleting, duplicating materials. 
    
    Attributes:
    material_stack(deque): Stack for handling storing original material for restoration.

    """

    def __init__(self, bpy_context) -> None: 
        """
        Initialize MaterialEditor Object
        """

        self.material_stack = deque()
        self.bpy_context = bpy_context

    def duplicate_material(self, obj) -> list[Any]:
        """
        Duplicate materials needed to be baked and store the orignal materials 
        inside the internal material_stack
        
        Parameters: 
        obj


        Returns: 
        """


        duplicate_materials = []
        for mat_id, slot in enumerate(obj.material_slots):
            # Material Validation
            material = slot.material
            mat_valid, err_msg = utils.validator.is_bakeable_mat(material)
            if not mat_valid: 
                print(err_msg)
                continue

            # Duplicate material
            dupe_mat = material.copy()
            dupe_mat.name = f"BAKE_{material.name}"
            self.material_stack.append((mat_id, material, dupe_mat))

            # Prepare to modify metallic connection
            metallic_connection = material_system.MetallicConnection(dupe_mat) # DEBUG
            metallic_connection.prepare_metallic_values()

            duplicate_materials.append((dupe_mat, metallic_connection))

            # Link Material
            self._link_material(obj, mat_id, dupe_mat)
            # self.report({'INFO'}, f"Duplicating material {material.name}")

        return duplicate_materials

    def add_texture_to_nodes(self, duplicate_materials, bake_image):
        """
        Add texture to nodes
        """
        for material, _ in duplicate_materials:
            material_system.create_texture_node(material, bake_image)

    def restore_material(self, obj):
        """Restore the original material to the slot"""
        for _ in range(len(obj.material_slots)):
            # Restore original material
            original_id, original_mat, dupe_mat = self.material_stack.pop()
            self._link_material(obj, original_id, original_mat)
            bpy.data.materials.remove(dupe_mat)

    def _link_material(self,obj, mat_id, material) -> None:
        """Link material to object"""
        obj.data.materials[mat_id] = material
        obj.material_slots[mat_id].material = material  
