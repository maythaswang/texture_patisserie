"""
This module contains utility functions for loading bake settings
"""
import bpy

class BakeConfig:
    def __init__(self,settings):
        bake_width = settings.bake_width
        bake_height = settings.bake_height
        save_to_disk = settings.save_to_disk
        output_path = settings.output_path