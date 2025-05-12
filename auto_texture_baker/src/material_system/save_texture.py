"""
This module contains functions for saving texture files  
"""
import os

def save_texture_to_disk(cfg, bake_type, obj_name, texture):
    """Save texture to the specified path"""
    if not texture:
        return

    file_path = os.path.join(cfg.output_path, f"{obj_name}_{bake_type}.png")

    print(texture.name)
    texture.filepath_raw = file_path
    texture.file_format = 'PNG'
    texture.update()
    texture.save()

def create_save_directory(save_dir):
    """Create directory if not exist"""
    try:
        os.makedirs(save_dir, exist_ok = True)
    except Exception as e:
        return False, e

    return True, ""
