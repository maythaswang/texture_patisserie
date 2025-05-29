"""
This module contains operators and utility functions for baking materials
"""
import bpy

from .data_models import bake_cfg
from .material_system import texture_generator,save_texture,metalness_manager, material_editor
from .utils import validator
import auto_texture_baker.src.state_manager as state_manager

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
        cfg = bake_cfg.BakeCfg(settings)
        print(type(cfg))

        # Verify that at least 1 object is selected
        selected = bpy.context.selected_objects
        if(not selected or len(selected) == 0):
            self.report({"ERROR"}, "No object selected")
            return {"CANCELLED"}
        
        # Validate All Objects
        for obj in selected:
            obj_valid, err_msg = validator.is_bakeable_obj(obj)
            if not obj_valid:
                self.report({"ERROR"}, err_msg)
                return {"CANCELLED"}

        # Save to disk prep
        status = True
        if cfg.save_to_disk:
            status, err = save_texture.create_save_directory(cfg.output_path)
            print(status)

        # Cancel if failed to create or find save directory.
        if not status: 
            self.report({"ERROR"}, "Failed to find or create save directory")
            return {"CANCELLED"} 

        # Load Render Configurations 
        render_state_manager = state_manager.RenderStateManager(context,cfg)
        render_state_manager.set_bake_render_state()
        
        # WARNING, BANDAID SOLUTIONNNNNNn
        BATCH_BAKE_NAME = "batch_bake"

        ### BAKE BATCH VARIANT
        batch_texture = {}
        obj_materials = []
        if not cfg.bake_separately:

            # Pre-Generate textures if we bake batch.
            for bake_name, (bake_type_enabled, bake_type, pass_filter, color_space) in cfg.texture_passes.items():
                if not bake_type_enabled:
                    continue 
                
                bake_image = self._generate_texture(BATCH_BAKE_NAME, cfg, bake_name, color_space)
                batch_texture.update({bake_name: bake_image})

            # Pre-Duplicate materials so we don't need to dupe k times. (where k is the number of bake types)
            for obj in selected:
                # Duplicate materials so if something went wrong we can revert without doing any damage to the real material.
                duplicate_materials = self._duplicate_materials(obj)
                obj_materials.append(duplicate_materials)



            for bake_name, (bake_type_enabled, bake_type, pass_filter, color_space) in cfg.texture_passes.items():
                # Ignore disabled passes
                if not bake_type_enabled:
                    continue

                for i, obj in enumerate(selected):

                    duplicate_materials = obj_materials[i] 

                    # WARNING: bandage solution for now... I'll fix this later.
                    bake_image = batch_texture.get(bake_name)
                    # Add bake_image to material nodes
                    self._add_texture_to_nodes(duplicate_materials,bake_image)

                    # Edit Metallic links
                    for _, metallic_connection in duplicate_materials:
                        if bake_name == "metallic": 
                            metallic_connection.prepare_bake_metallic()
                        else:
                            metallic_connection.prepare_bake_others()
                            
                # Baking routine
                try:
                    if bake_type_enabled:
                        context.scene.render.film_transparent = True
                        # bpy.data.scenes["Scene"].render.bake.use_clear = False
                        bpy.data.scenes["Scene"].render.bake.target = "IMAGE_TEXTURES"
                        context.scene.render.bake.use_clear = True
                        bpy.data.scenes["Scene"].update_render_engine()
                        print(bpy.data.scenes["Scene"].render.bake.use_clear)
                        bpy.ops.object.bake(type=bake_type,pass_filter=pass_filter, use_split_materials=False, use_clear=True, target="IMAGE_TEXTURES", height=cfg.bake_height, width = cfg.bake_width, save_mode="INTERNAL")

                        # WARNING: Again, another bandage solution
                        if cfg.save_to_disk and cfg.bake_separately:
                            save_texture.save_texture_to_disk(cfg, bake_name, BATCH_BAKE_NAME, cfg.file_type, bake_image)
                except Exception as e:
                    self.report({'ERROR'}, f"{e}")

            ## TODO: USING A STACK DOESN"T WORK FOR THIS SO LET's DO IT THE OTHER WAY (right now did the most stupid hacky way just to get by)
            # Restoring material
            for obj in selected[::-1]:
                self._restore_material(obj) # JUST REVERSE THE THING FOR NOW LOL

        ### STANDARD 
        else:
            # Iterate through the list of selected objects 
            for obj in selected:
                # Validate Object
                obj_valid, err_msg = validator.is_bakeable_obj(obj)
                if not obj_valid:
                    self.report({"ERROR"}, err_msg)
                    break

                # Duplicate materials so if something went wrong we can revert without doing any damage to the real material.
                duplicate_materials = self._duplicate_materials(obj)
                
                for bake_name, (bake_type_enabled, bake_type, pass_filter, color_space) in cfg.texture_passes.items():
                    # Ignore disabled passes
                    if not bake_type_enabled:
                        continue

                    # Edit Metallic links
                    for _, metallic_connection in duplicate_materials:
                        if bake_name == "metallic": 
                            metallic_connection.prepare_bake_metallic()
                        else:
                            metallic_connection.prepare_bake_others()

                    # WARNING: bandage solution for now... I'll fix this later.
                    if cfg.bake_separately:
                        bake_image = self._generate_texture(obj.name, cfg, bake_name, color_space)
                    else: 
                        bake_image = batch_texture.get(bake_name)

                    # Add bake_image to material nodes
                    self._add_texture_to_nodes(duplicate_materials,bake_image)


                    # Baking routine
                    try:
                        if bake_type_enabled:
                            bpy.ops.object.bake(type=bake_type,pass_filter=pass_filter, use_split_materials=False)
                            # WARNING: Again, another bandage solution
                            if cfg.save_to_disk and cfg.bake_separately:
                                save_texture.save_texture_to_disk(cfg, bake_name, obj.name, cfg.file_type, bake_image)
                    except Exception as e:
                        self.report({'ERROR'}, f"{e}")

                # Restoring material
                self._restore_material(obj)

        # Restore Render state 
        render_state_manager.restore_initial_render_state()

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

            # Prepare to modify metallic connection
            metallic_connection = metalness_manager.MetallicConnection(dupe_mat) # DEBUG
            metallic_connection.prepare_metallic_values()

            duplicate_materials.append((dupe_mat, metallic_connection))

            # Link Material
            material_editor.link_material(obj, mat_id, dupe_mat)
            self.report({'INFO'}, f"Duplicating material {material.name}")

        return duplicate_materials

    def _generate_texture(self, name, cfg, bake_name, color_space):  
        """Generate new texture to store the baked material"""       
        # Putting this here will bake multiple mats to same texture
        bake_image= texture_generator.create_texture_single(name, bake_name, cfg.bake_width, cfg.bake_height, color_space)

        # for material, _ in duplicate_materials:
            # texture_generator.create_texture_node(material, bake_image)

        return bake_image
    
    def _add_texture_to_nodes(self, duplicate_materials, bake_image):
        for material, _ in duplicate_materials:
            texture_generator.create_texture_node(material, bake_image)

    def _restore_material(self, obj):
        """Restore the original material to the slot"""
        for _ in range(len(obj.material_slots)):
            # Restore original material
            original_id, original_mat, dupe_mat = self.material_stack.pop()
            material_editor.link_material(obj, original_id, original_mat)
            bpy.data.materials.remove(dupe_mat)
