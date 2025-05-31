"""
This module manage setting up material connections
"""
from typing import Any
from collections import deque
import bpy

import texture_patisserie.src.material_system as material_system
import texture_patisserie.src.utils as utils


class MaterialEditor: 
    """
    Handles common action regarding creating, deleting, duplicating materials. 
    """

    def __init__(self, bpy_context) -> None: 
        """
        Initialize MaterialEditor Object

        Parameters: 
        bpy_context (bpy_types.Context): Blender python context
        """

        self.material_stack = deque()
        self.bpy_context = bpy_context

    def duplicate_material(self, obj) -> list[Any]:
        """
        Duplicate materials needed to be baked and store the orignal materials 
        inside the internal material_stack
        
        Parameters: 
        obj(bpy.types.Material) : Object that will have their material duplicated for baking purposes.
                                 *for some reason this is also material type lol 
        Returns: 
        list[bpy.types.Material]: List of duplicated materials.
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
            print(type(obj))
            dupe_mat.name = f"BAKE_{material.name}"
            self.material_stack.append((mat_id, material, dupe_mat))

            # Prepare to modify metallic connection
            metallic_connection = material_system.MetallicConnection(dupe_mat) # DEBUG
            metallic_connection.prepare_metallic_values()

            duplicate_materials.append((dupe_mat, metallic_connection))

            # Link Material
            self._link_material(obj, mat_id, dupe_mat)

        return duplicate_materials

    def add_texture_to_nodes(self, duplicate_materials, bake_image) -> None:
        """
        Add texture nodes to all materials in the object

        Parameters:
        duplicate_materials(list[bpy.types.Material])   : List of duplicated materials.
        bake_image                                      : Image texture that will be use for baking
        """

        for material, _ in duplicate_materials:
            self._create_texture_node(material, bake_image)

    def restore_material(self, obj) -> None:
        """
        Restore the original material to the slot

        Parameters:
        obj(bpy.types.Material): mesh 
        """

        for _ in range(len(obj.material_slots)):
            # Restore original material
            original_id, original_mat, dupe_mat = self.material_stack.pop()
            self._link_material(obj, original_id, original_mat)
            bpy.data.materials.remove(dupe_mat)

    def _create_texture_node(self, material, bake_image) -> None:
        """
        Create texture nodes in the material and hook up the image texture
        with material and bake_image and set them active

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


    def _link_material(self,obj, mat_id, material) -> None:
        """
        Link material to object

        Parameters: 
        obj(bpy.types.Material)         : mesh
        mat_id(int)                     : material slot id
        material(bpy.types.Material)    : material that will be linked
        """
        obj.data.materials[mat_id] = material
        obj.material_slots[mat_id].material = material  
