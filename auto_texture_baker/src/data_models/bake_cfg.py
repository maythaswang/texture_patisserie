"""
This module contains class for storing all baking configurations
"""

class BakeCfg:
    """
    Loads user's configuration for baking textures from blender's property group 
    into a more accessible way.
    """

    def __init__(self,settings) -> None:
        """
        Initialize BakeCfg with settings 

        Parameters:
        settings (auto_texture_baker.src.bake_settings.PG_bake_settings): Blender custom property group.
        """

        self.bake_separately = settings.bake_separately

        self.bake_width = settings.bake_width
        self.bake_height = settings.bake_height
        self.save_to_disk = settings.save_to_disk
        self.output_path = settings.output_path
        self.render_samples = settings.render_samples
        self.render_device = settings.render_device
        self.file_type = settings.file_type

        self.texture_passes = self._load_texture_settings(settings)

    ###--------------------------- PUBLIC ---------------------------###

    #
    #
    #

    ###-------------------------- PRIVATE --------------------------###

    def _load_texture_settings(self, settings) -> None:
        """
        Load settings for baking regarding which baking passes to use.

        Parameters:
        settings (auto_texture_baker.src.bake_settings.PG_bake_settings): Blender custom property group.
        """

        texture_passes = {
            "albedo":    (settings.albedo, "DIFFUSE", {"COLOR"}, "sRGB"),
            "roughness": (settings.roughness, "ROUGHNESS", {"NONE"}, "Non-Color"),
            "metallic":  (settings.metallic, "EMIT", {"NONE"}, "Non-Color"),
            "normal":    (settings.normal, "NORMAL", {"NONE"}, "Non-Color"),
        }
        return texture_passes
