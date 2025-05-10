"""
This module contains operators and utility functions for baking materials
"""
import bpy
from . import validator


from collections import deque

### TODO: THIS IS SUCH A MESS, THE AMOUNT OF CLEANING UP WILL BE MASSIVE


class MATERIAL_OT_bake_textures(bpy.types.Operator):
    bl_idname = "autobake.bake_texture"
    bl_label = "Auto bake textures"
    bl_description = "Auto bake textures based on boxes checked"
    bl_options = {"REGISTER"}

    # Material stack for restoring popped out materials
    material_stack = deque()

    def _load_bake_settings(self, context):
        """Load settings for baking"""
        settings = context.scene.pg_bake_settings
        texture_settings = {
            "albedo":    (settings.albedo, "DIFFUSE", {"COLOR"}),
            "roughness": (settings.roughness, "ROUGHNESS", {"NONE"}),
            "normal":    (settings.normal, "NORMAL", {"NONE"}),
            "metallic":  (settings.metallic, "EMIT", {"NONE"}),
        }
        return texture_settings
    
    # def _load_save_settings(self, context): 
    #     settings = context.scene.pg_bake_save_settings
    #     save_settings = {
    #         "bake_width":    bpy.props.IntProperty(name="bake_width", default=1024, description="Output texture width")
    #         "bake_height":   bpy.props.IntProperty(name="bake_height", default=1024, description="Output texture height")
    #         "save_to_disk":  bpy.props.BoolProperty(name="save_to_disk", default=False)
    #         "output_path":   bpy.props.StringProperty(name="output_path",subtype="DIR_PATH", default= "./baked"
    #     }
    #     return save_settings

    def execute(self, context):

        # Load settings
        texture_settings = self._load_bake_settings(context)

        has_valid_mesh = False

        # Verify that at least 1 object is selected
        selected = bpy.context.selected_objects
        if(not selected or len(selected) == 0):
            self.report({"ERROR"}, "No object selected")
            return {"CANCELLED"}

        ### TODO: CLEAN THIS UP LATER THIS IS JUST A PROTOTYPE

        TMP_BATCH_ON = True

        ### Variant where we bake all 3 materials on the same map
        if(TMP_BATCH_ON):
            # Iterate through the list of selected objects 
            for obj in selected:
                # Validate Object
                obj_valid, err_msg = validator.is_bakeable_obj(obj)
                if not obj_valid:
                    self.report({"ERROR"}, err_msg)
                    continue

                for bake_name, (bake_type_enabled, bake_type, pass_filter) in texture_settings.items():

                    bake_image= create_texture_single(obj.name, bake_name)
                    for mat_id, slot in enumerate(obj.material_slots):
                        material = slot.material
                        mat_valid, err_msg = validator.is_bakeable_mat(material)
                        if not mat_valid: 
                            self.report({"ERROR"}, err_msg)
                            continue
                        
                        # Duplicate material
                        dupe_mat = material.copy()                
                        dupe_mat.name = f"{material.name}_BAKE" # Might change suffix to resolution or something
                        self.material_stack.append((mat_id, material, dupe_mat))

                        link_material(obj, mat_id, dupe_mat)
                        create_texture_node(dupe_mat, bake_image)

                    # Baking routine
                    try:
                        if bake_type_enabled:
                            bpy.ops.object.bake(type=bake_type,pass_filter=pass_filter, use_split_materials=False) 

                    except Exception as e:
                        self.report({'ERROR'}, f"{e}")

                    for mat_id, slot in enumerate(obj.material_slots):
                        # Restore original material 
                        original_id, original_mat, dupe_mat = self.material_stack.pop()
                        link_material(obj, original_id, original_mat)
                        bpy.data.materials.remove(dupe_mat)


                self.report({'INFO'}, f"Baking material {material.name}")
                has_valid_mesh = True

        ### OLD VERSION WHERE BATCHING IS NOT CONSIDERED <also this method is kinda hacky and terrible>
        else:
            # Iterate through the list of selected objects 
            for obj in selected:
                # Validate Object
                obj_valid, err_msg = validator.is_bakeable_obj(obj)
                if not obj_valid:
                    self.report({"ERROR"}, err_msg)
                    continue

                for mat_id, slot in enumerate(obj.material_slots):
                # for mat_id, material in enumerate(obj.data.materials):
                    material = slot.material
                    mat_valid, err_msg = validator.is_bakeable_mat(material)
                    if not mat_valid: 
                        self.report({"ERROR"}, err_msg)
                        continue
                    
                    # Duplicate material
                    dupe_mat = material.copy()                
                    dupe_mat.name = f"{material.name}_BAKE" # Might change suffix to resolution or something
                    self.material_stack.append((mat_id, material))

                    # Baking routine
                    try:
                        link_material(obj, mat_id, dupe_mat)
                        obj.active_material_index = mat_id
                        bake_textures(dupe_mat, texture_settings, obj, True)
                        # bake_textures(material, bake_settings, obj)

                    except Exception as e:
                        self.report({'ERROR'}, f"{e}")

                    # Restore original material 
                    original_id, original_mat = self.material_stack.pop()
                    link_material(obj, original_id, original_mat)
                    bpy.data.materials.remove(dupe_mat)

                    self.report({'INFO'}, f"Baking material {material.name}")
                    has_valid_mesh = True

        # No material was baked
        if not has_valid_mesh:
            self.report({'ERROR'}, "No valid mesh")
            return {"CANCELLED"}

        # Baking success
        self.report({'INFO'}, "Baking Complete!")
        return {"FINISHED"}

# Set material to material slot at mat_id
def link_material(obj, mat_id, material) -> None: 
    """Link material to object"""
    obj.data.materials[mat_id] = material
    obj.material_slots[mat_id].material = material

### MIXED VERSION
def create_texture_single(name, bake_type):
    """Generate new texture for baking all mats of same obj"""
    # Generate textures
    width, height = 1024, 1024  # Texture size (can be customized)
    bake_image = bpy.data.images.new(f"tmp_{name}_{bake_type}", width=width, height=height)
    return bake_image

def create_texture_node(material, bake_image):
    """Create texture nodes in the material and hook up the image texture"""
    nodes = material.node_tree.nodes
    tex_image_node = nodes.new(type='ShaderNodeTexImage')
    tex_image_node.image = bake_image
    tex_image_node.select = True
    nodes.active = tex_image_node

### SEPARATE VERSION

def create_texture(material, bake_type) -> None:
    """Generate new texture for baking"""

    # Generate textures
    width, height = 1024, 1024  # Texture size (can be customized)
    bake_image = bpy.data.images.new(f"tmp_{material.name}_{bake_type}", width=width, height=height)

    # Create texture node 
    nodes = material.node_tree.nodes
    tex_image_node = nodes.new(type='ShaderNodeTexImage')
    tex_image_node.image = bake_image
    tex_image_node.select = True
    nodes.active = tex_image_node


def bake_textures(material, bake_settings, obj, split_tex) -> None:
    """Bake textures"""

    # Ensure only this object is selected and active
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    for bake_name, (bake_type_enabled, bake_type, pass_filter) in bake_settings.items():
        if bake_type_enabled:
            create_texture(material, bake_name) 
            print(material.name)
            bpy.ops.object.bake(type=bake_type,pass_filter=pass_filter, use_split_materials=split_tex) # I think this one might be running in batches? 
