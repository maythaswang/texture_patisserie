"""
This module manages loading, storing, and restoring render settings inbetween bakes
"""

class RenderStateManager:
    """
    Handles managing setting render state according to user input
    """

    def __init__(self, bpy_context, render_cfg):
        """
        Initialize Render State Manager

        Parameters: 
        bpy_context(bpy_types.Context)                                  : Blender python context
        render_cfg(texture_patisserie.src.data_models.bake_cfg.BakeCfg) : Bake and Render Configs
        """

        self.bpy_context = bpy_context
        self.render_cfg = render_cfg
        self.render_state = self._store_render_state()

    ###--------------------------- PUBLIC ---------------------------###

    def set_bake_render_state(self) -> None:
        """
        Set render state for baking
        """

        self.bpy_context.scene.render.engine                        = "CYCLES"
        self.bpy_context.scene.cycles.samples                       = self.render_cfg.render_samples
        self.bpy_context.scene.cycles.device                        = self.render_cfg.render_device
        self.bpy_context.scene.render.image_settings.file_format    = self.render_cfg.file_type
        self.bpy_context.scene.render.bake.margin                   = self.render_cfg.texture_margin
     
    def restore_initial_render_state(self) -> None: 
        """
        Restore render state to default
        """

        self.bpy_context.scene.render.engine                        = self.render_state["engine"]
        self.bpy_context.scene.cycles.samples                       = self.render_state["samples"]
        self.bpy_context.scene.cycles.device                        = self.render_state["device"]
        self.bpy_context.scene.render.image_settings.file_format    = self.render_state["file_type"] 
        self.bpy_context.scene.render.bake.margin                   = self.render_state["texture_margin"]

    ###-------------------------- PRIVATE --------------------------###

    def _store_render_state(self) -> None:
        """
        Store previous render state
        """

        render_state = {
            "engine":           self.bpy_context.scene.render.engine,
            "samples":          self.bpy_context.scene.cycles.samples,
            "device":           self.bpy_context.scene.cycles.device,
            "file_type":        self.bpy_context.scene.render.image_settings.file_format,
            "texture_margin":   self.bpy_context.scene.render.bake.margin
        }

        return render_state
