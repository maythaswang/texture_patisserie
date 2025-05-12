"""
This module contains functions for saving texture files  
"""
import os

FILE_TYPE_EXT = {
    "BMP": ".bmp",
    "JPEG": ".jpg",
    "PNG": ".png",
    "TIFF": ".tiff"
}

def save_texture_to_disk(cfg, bake_type, obj_name, file_type, texture):
    """Save texture to the specified path"""
    if not texture:
        return

    file_path = os.path.join(cfg.output_path, f"{obj_name}_{bake_type}{FILE_TYPE_EXT[file_type]}")
    print(FILE_TYPE_EXT[file_type])
    texture.filepath_raw = file_path
    texture.save()

def create_save_directory(save_dir):
    """Create directory if not exist"""
    try:
        os.makedirs(save_dir, exist_ok = True)
    except Exception as e:
        return False, e

    return True, ""
