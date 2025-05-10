"""
This module contains operators and utility functions for baking materials
"""
import bpy

from .config import bake_config
from .texture_system import texture_generator
from .utils import validator

from collections import deque

class MATERIAL_OT_bake_textures(bpy.types.Operator):
    bl_idname = "autobake.bake_texture"
    bl_label = "Auto bake textures"
    bl_description = "Auto bake textures based on boxes checked"
    bl_options = {"REGISTER"}

    # Material stack for restoring popped out materials
    material_stack = deque()

    def execute(self, context):

        # Load settings
        settings = context.scene.pg_bake_settings
        bake_configs = bake_config.BakeConfig(settings)
        has_valid_mesh = False

        # Verify that at least 1 object is selected
        selected = bpy.context.selected_objects
        if(not selected or len(selected) == 0):
            self.report({"ERROR"}, "No object selected")
            return {"CANCELLED"}

        # Iterate through the list of selected objects 
        for obj in selected:
            # Validate Object
            obj_valid, err_msg = validator.is_bakeable_obj(obj)
            if not obj_valid:
                self.report({"ERROR"}, err_msg)
                continue

            for bake_name, (bake_type_enabled, bake_type, pass_filter) in bake_configs.texture_passes.items():
                # Ignore disabled passes
                if not bake_type_enabled:
                    continue

                # Duplicate material
                self._duplicate_material(obj, bake_name)

                # Baking routine
                try:
                    if bake_type_enabled:
                        bpy.ops.object.bake(type=bake_type,pass_filter=pass_filter, use_split_materials=False) 

                except Exception as e:
                    self.report({'ERROR'}, f"{e}")

                # Restoring material
                self._restore_material(obj)

            has_valid_mesh = True
    
        # No material was baked
        if not has_valid_mesh:
            self.report({'ERROR'}, "No valid mesh")
            return {"CANCELLED"}

        # Baking success
        self.report({'INFO'}, "Baking Complete!")
        return {"FINISHED"}


    # Right now we duplicate material for every texture type we bake
    # TODO: Fix this by separating and duplicate only once
    def _duplicate_material(self, obj, bake_name):
        """Duplicate material for writing systems"""
        bake_image= texture_generator.create_texture_single(obj.name, bake_name)
        for mat_id, slot in enumerate(obj.material_slots):
            material = slot.material
            mat_valid, err_msg = validator.is_bakeable_mat(material)
            if not mat_valid: 
                self.report({"ERROR"}, err_msg)
                continue
                
            # Duplicate material
            dupe_mat = material.copy()                
            dupe_mat.name = f"{material.name}_BAKE" # Might change suffix to resolution or something
            self.material_stack.append((mat_id, material, dupe_mat))

            texture_generator.link_material(obj, mat_id, dupe_mat)
            texture_generator.create_texture_node(dupe_mat, bake_image)

            self.report({'INFO'}, f"Baking material {material.name}, {bake_name}")

    def _restore_material(self, obj):
        """Restore the original material to the slot"""
        for mat_id, slot in enumerate(obj.material_slots):
            # Restore original material 
            original_id, original_mat, dupe_mat = self.material_stack.pop()
            texture_generator.link_material(obj, original_id, original_mat)
            bpy.data.materials.remove(dupe_mat)
