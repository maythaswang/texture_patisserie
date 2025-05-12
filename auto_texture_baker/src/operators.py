"""
This module contains operators and utility functions for baking materials
"""
import bpy

from .bake_configs import bake_config
from .material_system import texture_generator,save_texture,metalness_manager, material_editor
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
        cfg = bake_config.BakeConfig(settings)
        has_valid_mesh = False

        # Verify that at least 1 object is selected
        selected = bpy.context.selected_objects
        if(not selected or len(selected) == 0):
            self.report({"ERROR"}, "No object selected")
            return {"CANCELLED"}

        status = True
        if cfg.save_to_disk:
            status, err = save_texture.create_save_directory(cfg.output_path)
            print(status)

        # Load Render Configurations 
        render_state = self._store_render_state(context)
        self._set_render_state(context,cfg)


        if not status: 
            self.report({"ERROR"}, "Failed to find or create save directory")
            return {"CANCELLED"} 

        # Iterate through the list of selected objects 
        for obj in selected:
            # Validate Object
            obj_valid, err_msg = validator.is_bakeable_obj(obj)
            if not obj_valid:
                self.report({"ERROR"}, err_msg)
                continue

            duplicate_materials = self._duplicate_materials(obj)
            
            # Prepare to modify metallic connection
            metallic_connection = metalness_manager.MetallicConnection(duplicate_materials[0]) # DEBUG
            metallic_connection.prepare_metallic_values()

            for bake_name, (bake_type_enabled, bake_type, pass_filter, color_space) in cfg.texture_passes.items():
                # Ignore disabled passes
                if not bake_type_enabled:
                    continue

                # Edit Metallic links
                if bake_name == "metallic": 
                    metallic_connection.prepare_bake_metallic()
                else:
                    metallic_connection.prepare_bake_others()


                bake_image = self._generate_texture(obj, cfg, duplicate_materials, bake_name, color_space)

                # Baking routine
                try:
                    if bake_type_enabled:
                        bpy.ops.object.bake(type=bake_type,pass_filter=pass_filter, use_split_materials=False)

                        if cfg.save_to_disk:
                            save_texture.save_texture_to_disk(cfg, bake_name, obj.name, cfg.file_type, bake_image)
                except Exception as e:
                    self.report({'ERROR'}, f"{e}")

            # Restoring material
            self._restore_material(obj)
            has_valid_mesh = True
        
        # Restore Render state 
        self._restore_render_state(context,render_state)

        # No material was baked
        if not has_valid_mesh:
            self.report({'ERROR'}, "No valid mesh")
            return {"CANCELLED"}

        # Baking success
        self.report({'INFO'}, "Baking Complete!")
        return {"FINISHED"}

    def _duplicate_materials(self, obj):
        """Duplicate material to be baked"""
        duplicate_materials = []
        for mat_id, slot in enumerate(obj.material_slots):
            # Material Validation
            material = slot.material
            mat_valid, err_msg = validator.is_bakeable_mat(material)
            if not mat_valid: 
                self.report({"ERROR"}, err_msg)
                continue

            # Duplicate material
            dupe_mat = material.copy()
            dupe_mat.name = f"BAKE_{material.name}"
            self.material_stack.append((mat_id, material, dupe_mat))
            duplicate_materials.append((dupe_mat))

            # Link Material
            material_editor.link_material(obj, mat_id, dupe_mat)
            self.report({'INFO'}, f"Duplicating material {material.name}")

        return duplicate_materials

    def _generate_texture(self, obj, cfg, duplicate_materials, bake_name, color_space):  
        """Generate new texture to store the baked material"""       
        # Putting this here will bake multiple mats to same texture
        bake_image= texture_generator.create_texture_single(obj.name, bake_name, cfg.bake_width, cfg.bake_height, color_space)

        for material in duplicate_materials:
            texture_generator.create_texture_node(material, bake_image)
            self.report({'INFO'}, f"Generating texture {material.name}, {bake_name}")

        return bake_image

    def _restore_material(self, obj):
        """Restore the original material to the slot"""
        for _ in range(len(obj.material_slots)):
            # Restore original material
            original_id, original_mat, dupe_mat = self.material_stack.pop()
            material_editor.link_material(obj, original_id, original_mat)
            bpy.data.materials.remove(dupe_mat)

    def _set_render_state(self, context, cfg):
        """Set render state for baking"""
        context.scene.render.engine = "CYCLES"
        context.scene.cycles.samples = cfg.render_samples
        context.scene.cycles.device = cfg.render_device
        context.scene.render.image_settings.file_format = cfg.file_type

        
    def _store_render_state(self, context):
        """Store previous render state"""
        render_state = {
            "engine": context.scene.render.engine,
            "samples": context.scene.cycles.samples,
            "device": context.scene.cycles.device,
            "file_type": context.scene.render.image_settings.file_format
        }
        return render_state
    
    def _restore_render_state(self,context,render_state): 
        """Restore render state to default"""
        context.scene.render.engine = render_state["engine"]
        context.scene.cycles.samples = render_state["samples"]
        context.scene.cycles.device = render_state["device"]
        context.scene.render.image_settings.file_format = render_state["file_type"] 
