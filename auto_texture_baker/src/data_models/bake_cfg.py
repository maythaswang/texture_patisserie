"""
This module contains class for storing all baking configurations
"""

import auto_texture_baker.src.bake_enums as bake_enums

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

        # self.bake_separately = settings.bake_separately
        self.bake_grouping_options = bake_enums.get_grouping_options_from_string(settings.bake_grouping_options)

        self.bake_width = settings.bake_width
        self.bake_height = settings.bake_height
        self.save_to_disk = settings.save_to_disk
        self.output_path = settings.output_path
        self.render_samples = settings.render_samples
        self.render_device = settings.render_device
        self.file_type = settings.file_type

        self.texture_passes = self._load_texture_settings(settings)

        # Naming Convention
        self.naming_convention = settings.naming_convention

        self.output_name_text1 = settings.output_name_text1
        self.output_name_text2 = settings.output_name_text2 
        self.output_name_separator = settings.output_name_separator

        # Override batch name
        self.batch_name_override = settings.batch_name_override
        self.batch_name = settings.batch_name

        # Override texture names 
        self.texture_type_name_override = settings.texture_type_name_override
        self.output_albedo_name = settings.output_albedo_name
        self.output_roughness_name = settings.output_roughness_name
        self.output_metallic_name = settings.output_metallic_name
        self.output_normal_name = settings.output_normal_name

        # Versioning 
        self.overwrite_previous_save = settings.overwrite_previous_save
        self.file_versioning_suffix = settings.file_versioning_suffix
    
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
