"""
This module serves as the core logic for baking texture that uses single 
Principled BSDF. 
"""
import bpy
import auto_texture_baker.src.material_system as material_system

class PrincipledBSDFBaker:
    """
    Serves as the core logic for baking texture that uses single Principled BSDF
    as the main shader.
    """

    def __init__(self, context, cfg, selected) -> None:
        """
        Initialize PrincipledBSDFBaker with context, cfg, selected 

        Parameters:
        context (bpy_types.Context)                                 : Blender python context
        cfg (auto_texture_baker.src.data_models.bake_cfg.BakeCfg)   : Bake configs
        selected (list[Any])                                        : Selected meshes
        """

        self.cfg = cfg
        self.selected = selected
        self.blender_context = context
        self.material_editor = material_system.MaterialEditor(context)
        self.texture_manager = material_system.TextureManager(cfg.output_path)

    def batch_bake(self) -> str:
        """
        Bake models in batches into one single texture per bake pass, this can be 
        used to create texture atlas

        Returns: 
        str: String of error message if the program encounters an error, otherwise None
        """

        # WARNING, BANDAID SOLUTIONNNNNNn
        BATCH_BAKE_NAME = "batch_bake"       

        # Stores textures and materials for later use
        batch_textures = {}
        obj_materials = []
        cfg = self.cfg

        # Pre-Generate textures for each bake type
        for bake_name, (bake_type_enabled, bake_type, pass_filter, color_space) in cfg.texture_passes.items():
            if not bake_type_enabled:
                continue 
            
            bake_image= self.texture_manager.create_texture_single(cfg,BATCH_BAKE_NAME, bake_name, cfg.bake_width, cfg.bake_height, color_space)
            batch_textures.update({bake_name: bake_image})

        # Pre-Duplicate materials so we don't need to dupe k times. (where k is the number of bake types)
        for obj in self.selected:
            # Duplicate materials so if something went wrong we can revert without doing any damage to the real material.
            duplicate_materials = self.material_editor.duplicate_material(obj)
            obj_materials.append(duplicate_materials)

        cfg = self.cfg
        for bake_name, (bake_type_enabled, bake_type, pass_filter, color_space) in cfg.texture_passes.items():
        # Ignore disabled passes
            if not bake_type_enabled:
                continue

            for i, obj in enumerate(self.selected):
                duplicate_materials = obj_materials[i] 

                # WARNING: bandage solution for now... I'll fix this later.
                bake_image = batch_textures.get(bake_name)
                # Add bake_image to material nodes
                self.material_editor.add_texture_to_nodes(duplicate_materials,bake_image)

                self._rewrangle_metallic_nodes(bake_name, duplicate_materials)
   
            # Baking routine
            err_msg = self._bake_routine(bake_type, pass_filter, cfg.bake_height, cfg.bake_width)
            if not err_msg is None:
                return err_msg

            if cfg.save_to_disk:
                self._save_texture(bake_name, obj.name, bake_image)

        ## TODO: Fix this lol...
        # USING A STACK DOESN"T WORK FOR THIS SO LET's DO IT THE OTHER WAY (right now did the most stupid hacky way just to get by)
        
        # Restoring material
        for obj in self.selected[::-1]:
            self.material_editor.restore_material(obj) # JUST REVERSE THE THING FOR NOW LOL

    def separate_bake(self) -> str:
        """
        Bake textures separately for each mesh
        
        Returns: 
        str: String of error message if the program encounters an error, otherwise None
        """

        cfg = self.cfg
        # Iterate through the list of selected objects 
        for obj in self.selected:

            # Duplicate materials so if something went wrong we can revert without doing any damage to the real material.
            duplicate_materials = self.material_editor.duplicate_material(obj)
            
            for bake_name, (bake_type_enabled, bake_type, pass_filter, color_space) in cfg.texture_passes.items():
                # Ignore disabled passes
                if not bake_type_enabled:
                    continue

                # Edit Metallic links
                self._rewrangle_metallic_nodes(bake_name,duplicate_materials)
                bake_image = self.texture_manager.create_texture_single(cfg, obj.name, bake_name, cfg.bake_width, cfg.bake_height, color_space)

                # Add bake_image to material nodes (each obj have same bake_image for all materials)
                self.material_editor.add_texture_to_nodes(duplicate_materials, bake_image)
                
                # Baking routine
                err_msg = self._bake_routine(bake_type, pass_filter, cfg.bake_height, cfg.bake_width)
                if not err_msg is None:
                    return err_msg
                
                if cfg.save_to_disk:
                    self._save_texture(bake_name ,obj.name ,bake_image)

            # Restoring material
            self.material_editor.restore_material(obj)

        return None

    def _bake_routine(self, bake_type, pass_filter, bake_height, bake_width) -> str: 
        """
        Main baking routine with settings based on bake_type, pass_filter, bake_height, bake_width

        Parameters: 
        bake_type(string)   : Bake type specified from blender's baking option such as 'DIFFUSE' 
        pass_filter(set)    : Pass filter such as 'COLOR', 'DIRECT', 'NONE'
        bake_height(float)  : Height of the output texture 
        bake_width(float)   : Width of the output texture

        Returns: 
        str: String of error message if the program encounters an error, otherwise None
        """

        try:
            self.blender_context.scene.render.film_transparent = True
            self.blender_context.scene.render.bake.use_clear = True
            bpy.data.scenes["Scene"].render.bake.target = "IMAGE_TEXTURES"
            bpy.data.scenes["Scene"].update_render_engine()

            bpy.ops.object.bake(type=bake_type,pass_filter=pass_filter, use_split_materials=False, use_clear=True, target="IMAGE_TEXTURES", height=bake_height, width = bake_width, save_mode="INTERNAL")

        #pylint: disable=W0718
        except Exception as e:
            return e
        
        return None

    def _save_texture(self, bake_name, output_filename, image_texture ):
        """
        Save the output texture to the device

        Parameters: 
        bake_name(string)               : Bake name name such as 'albedo', 'roughness'...
        output_filename(string)         : Filename that will be the used in the output file
        image_texture(bpy.types.Image)  : Image textures that will be saved. 
        """

        cfg = self.cfg
        self.texture_manager.save_texture_to_disk(cfg, bake_name, output_filename, cfg.file_type, image_texture)


    def _rewrangle_metallic_nodes(self, bake_name, duplicate_materials) -> None:
        """
        Rewrangle metallic nodes for baking purposes

        Parameters: 
        bake_name(string)                               : Bake name name such as 'albedo', 'roughness'...
        duplicate_materials(list[bpy.types.Material])   : List of duplicated materials that requires rewrangling
        """

        for _, metallic_connection in duplicate_materials:
            if bake_name == "metallic": 
                metallic_connection.prepare_bake_metallic()
            else:
                metallic_connection.prepare_bake_others()
