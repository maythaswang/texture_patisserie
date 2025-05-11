import bpy
import os

def save_texture_to_disk(cfg, bake_type, obj_name, texture):
    if not texture:
        # self.report({'WARNING'}, f"{obj_name}: No image found to save for {bake_name}")
        return

    # save_dir = bpy.path.abspath("//bakes")
    # os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(cfg.output_path, f"{obj_name}_{bake_type}.png")

    print(texture.name)
    texture.filepath_raw = file_path
    texture.file_format = 'PNG'
    texture.update()
    texture.save()
    # self.report({'INFO'}, f"Saved {bake_type} to {file_path}")

def create_save_directory(save_dir):
    """Create directory if not exist"""
    try:
        os.makedirs(save_dir, exist_ok = True)
    except Exception as e:
        return False, e

    return True, ""
