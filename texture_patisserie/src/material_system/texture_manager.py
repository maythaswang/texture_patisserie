"""
This module handle texture related operations such as creating, saving textures
"""

import os 
import bpy
import texture_patisserie.src.utils as utils

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
        cfg(texture_patisserie.src.data_models.bake_cfg.BakeCfg):   Bake settings 
        bake_type(String)                                       :   Type of baking (albedo, normals, etc...)
        file_type(String)                                       :   Output file type
        texture(bpy.types.Image)                                :   Image texture
        """
        # print(FILE_TYPE_EXT[file_type]) #DEBUG

        # Verify if the texture is exists
        if not texture:
            return

        # Create file path 
        texture_name = utils.build_texture_name(cfg, bake_type, obj_name)
        output_path = cfg.output_path

        if cfg.create_subdirectory: 
            subdir_name = utils.build_dir_name(cfg, obj_name)
            output_path = os.path.join(cfg.output_path, subdir_name)

            # Create subdirectory
            status, err = utils.create_save_directory(output_path)
            if not status:
                print(err)   

        # Save filepath
        file_path = os.path.join(output_path, f"{texture_name}{FILE_TYPE_EXT[file_type]}")
        if not cfg.overwrite_previous_save:
            counter = 1
            while(os.path.exists(file_path)):
                file_path = os.path.join(output_path, f"{texture_name}{cfg.output_name_separator}{counter}{FILE_TYPE_EXT[file_type]}")
                counter+= 1
        

        texture.filepath_raw = file_path
        texture.save()



    def create_texture_single(self, cfg, name, bake_type, width, height, color_space):
        """
        Generate new texture and define a new name for baking materials

        Parameters: 
        name(string)        : texture name
        bake_type(string)   : texture name suffix
        width(int)          : texture width
        height(int)         : texture height
        color_space(string) : color space of the texture such as 'sRGB'
        """

        # Define Texture name    
        # texture_name = f"tmp_{name}_{bake_type}"
        texture_name = utils.build_texture_name(cfg, bake_type, name)

        # Create Texture
        non_color = not "albedo" == bake_type
        use_alpha = cfg.use_alpha and bake_type == "albedo"
        bake_image = bpy.data.images.new(texture_name, width=width, height=height, alpha = use_alpha, is_data=non_color)
        bake_image.colorspace_settings.name = color_space

        # Configure Image texture 
        bake_image.file_format = cfg.file_type

        return bake_image   
