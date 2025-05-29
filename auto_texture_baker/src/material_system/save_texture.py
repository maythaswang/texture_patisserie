"""
This module contains functions for saving texture files  
"""
import os
import bpy

FILE_TYPE_EXT = {
    "BMP": ".bmp",
    "JPEG": ".jpg",
    "PNG": ".png",
    "TIFF": ".tiff"
}

def save_texture_to_disk(cfg, bake_type, obj_name, file_type, texture):
    """
    Save texture to the specified path provided cfg, bake_type, obj_name, file_type, texture

    Parameters: 
    cfg(auto_texture_baker.src.data_models.bake_cfg.BakeCfg):   Bake settings 
    bake_type(String)                                       :   Type of baking (albedo, normals, etc...)
    file_type(String)                                       :   Output file type
    texture(UNKNOWN)                                        :   Image texture
    """

    # Verify if the texture is exists
    if not texture:
        return

    # Create file path 
    file_path = os.path.join(cfg.output_path, f"{obj_name}_{bake_type}{FILE_TYPE_EXT[file_type]}")
    print(FILE_TYPE_EXT[file_type])
    texture.filepath_raw = file_path
    texture.save()

def create_save_directory(save_dir):
    """
    Create directory for saving textures if not exist
    """

    try:
        abs_save_dir = bpy.path.abspath(save_dir)
        os.makedirs(abs_save_dir, exist_ok = True)
    except Exception as e:
        return False, e

    return True, ""
