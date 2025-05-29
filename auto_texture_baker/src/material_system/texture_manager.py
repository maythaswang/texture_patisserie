"""
This module handle texture related operations such as creating, saving textures
"""

import os 
import bpy

FILE_TYPE_EXT = {
    "BMP": ".bmp",
    "JPEG": ".jpg",
    "PNG": ".png",
    "TIFF": ".tiff"
}

class TextureManager: 
    """
    Manages texture related operations such as creating, saving textures
    """

    def __init__(self, save_dir): 
        self.save_dir = save_dir

    def save_texture_to_disk(self, cfg, bake_type, obj_name, file_type, texture):
        """
        Save texture to the specified path provided cfg, bake_type, obj_name, file_type, texture

        Parameters: 
        cfg(auto_texture_baker.src.data_models.bake_cfg.BakeCfg):   Bake settings 
        bake_type(String)                                       :   Type of baking (albedo, normals, etc...)
        file_type(String)                                       :   Output file type
        texture(bpy.types.Image)                                :   Image texture
        """

        print(type(texture))
        # Verify if the texture is exists
        if not texture:
            return

        # Create file path 
        file_path = os.path.join(cfg.output_path, f"{obj_name}_{bake_type}{FILE_TYPE_EXT[file_type]}")
        print(FILE_TYPE_EXT[file_type])
        texture.filepath_raw = file_path
        texture.save()



    def create_texture_single(self, name, bake_type, width, height, color_space):
        """
        Generate new texture and define a new name for baking materials
        """

        # Define Texture name    
        texture_name = f"tmp_{name}_{bake_type}"

        # Create Texture
        bake_image = bpy.data.images.new(texture_name, width=width, height=height)
        bake_image.colorspace_settings.name = color_space

        # Configure Image texture 
        # TODO: Fix this, the output does not reflect this value at all.
        bake_image.alpha_mode = 'STRAIGHT'
        bake_image.file_format = 'PNG'

        return bake_image
