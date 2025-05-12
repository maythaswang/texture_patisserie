"""
This module contains utility functions for loading bake settings
"""
import bpy

class BakeConfig:
    def __init__(self,settings):
        self.bake_width = settings.bake_width
        self.bake_height = settings.bake_height
        self.save_to_disk = settings.save_to_disk
        self.output_path = settings.output_path

        self.texture_passes = self._load_texture_settings(settings)

    def _load_texture_settings(self, settings):
        """Load settings for baking"""
        texture_passes = {
            "albedo":    (settings.albedo, "DIFFUSE", {"COLOR"}, "sRGB"),
            "roughness": (settings.roughness, "ROUGHNESS", {"NONE"}, "Non-Color"),
            "normal":    (settings.normal, "NORMAL", {"NONE"}, "Non-Color"),
            "metallic":  (settings.metallic, "EMIT", {"NONE"}, "Non-Color"),
        }
        return texture_passes