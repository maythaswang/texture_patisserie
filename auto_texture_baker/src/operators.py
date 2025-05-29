"""
This module contains operators and utility functions for baking materials
"""
import bpy
import auto_texture_baker.src.baking_system as baking_system
import auto_texture_baker.src.state_manager as state_manager
import auto_texture_baker.src.data_models as data_models
import auto_texture_baker.src.utils as utils


# pylint: disable=C0103
class MATERIAL_OT_bake_textures(bpy.types.Operator):
    """
    Blender Operator for baking texture
    """

    bl_idname = "autobake.bake_texture"
    bl_label = "Auto bake textures"
    bl_description = "Auto bake textures based on boxes checked"
    bl_options = {"REGISTER"}

    def execute(self, context) -> None:
        """
        Handle baking based on given settings.
        
        Parameters: 
        context (bpy_types.Context): Blender python context
        """

        # Load settings
        settings = context.scene.pg_bake_settings
        cfg = data_models.BakeCfg(settings)
        selected = bpy.context.selected_objects

        # Pre Bake Routine 
        err_msg = self._pre_bake_routine(cfg, selected)
        if not err_msg is None: 
            self.report({'ERROR'}, err_msg)
            return {"CANCELLED"}

        # Load Render Configurations 
        render_state_manager = state_manager.RenderStateManager(context,cfg)
        render_state_manager.set_bake_render_state()

        # We will probably be handling more shaders in the future but this one will be the 
        # defualt for now
        principled_bsdf_baker = baking_system.PrincipledBSDFBaker(context,cfg,selected)
        if cfg.bake_separately:
            principled_bsdf_baker.separate_bake()
        else:
            principled_bsdf_baker.batch_bake()

        # Restore Render state 
        render_state_manager.restore_initial_render_state()

        # Baking success
        self.report({'INFO'}, "Baking Complete!")
        return {"FINISHED"}

    def _bakeable_test(self, selected): 
        """
        Test whether the current setup can be used for baking textures.

        selected(list[Any]): Selected meshes for baking
        """

        # Verify that at least one object is selected
        if(not selected or len(selected) == 0):
            return "No object selected"
        
        # Verify that all selected objects are bakable
        for obj in selected:
            obj_valid, err_msg = utils.is_bakeable_obj(obj)
            if not obj_valid:
                return err_msg
        
        return None

    def _prepare_save_dir(self, save_to_disk, output_path) -> str:
        """
        Create save directory if the users wishes to export the baked texture 
        to an external directory.

        Parameters:
        save_to_disk(bool)  : Status whether the user wants to export the texture
        output_path(string) : Output path of the texture 

        Returns:
        str: Error message if encounter errors, otherwise None 
        """

        if not save_to_disk:
            return None 
        
        status, err_msg = utils.create_save_directory(output_path)

        # Cancel if failed to create or find save directory.
        if not status: 
            return "Failed to find or create save directory: " + err_msg

    def _pre_bake_routine(self, cfg, selected): 
        """
        Run all required tests before baking 
        
        Parameters: 
        cfg(auto_texture_baker.src.data_models.bake_cfg.BakeCfg): Bake configs
        selected(list[Any])                                     : List of selected mesh to bake
        """
        
        err_msg = self._bakeable_test(selected)
        if not err_msg is None: 
            return err_msg
        
        err_msg = self._prepare_save_dir(cfg.save_to_disk, cfg.output_path)
        if not err_msg is None: 
            return err_msg
        
        return None
