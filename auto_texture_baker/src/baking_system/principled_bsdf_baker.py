"""
This module serves as the core logic for baking texture that uses single 
Principled BSDF. 
"""

import bpy

class PrincipledBSDFBaker:
    """
    Serves as the core logic for baking texture that uses single Principled BSDF
    as the main shader.
    """

    def __init__(self):
        """
        Initialize PrincipledBSDFBaker
        """

        pass

    def batch_bake(self):
        
        # Stores textures and materials for later use
        batch_textures = {}
        obj_materials = []

        # for bake_name, (bake_type_enabled, bake_type, pass_filter, color_space) in cfg.texture_passes.items():
        #     if not bake_type_enabled:
        #         continue 
            
            # bake_image= material_system.create_texture_single(BATCH_BAKE_NAME, bake_name, cfg.bake_width, cfg.bake_height, color_space)
            # batch_texture.update({bake_name: bake_image})






    def separate_bake(self):
        pass
