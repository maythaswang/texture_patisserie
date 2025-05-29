"""
Bake Plugin UI 
"""
import bpy

#pylint: disable=C0103
class PROPERTIES_PT_bake_panel(bpy.types.Panel):
    """
    Panel for selecting nodes to bake
    """

    bl_idname = "MATERIAL_PT_bake_textures"
    bl_label = "Auto Texture Baker"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"

    def draw(self, context):
        """
        Draw the UI panel every frame using the provided context
        context(bpy_types.Context): blender python's context
        """

        ### Setup ### 
        layout = self.layout
        scene = context.scene
        pg = scene.pg_bake_settings
        

        layout.operator("autobake.bake_texture", text="Bake Selected Maps")

        ### Bake settings 
        layout.label(text="Bake Settings")

        row = layout.row()
        layout.label(text="Bake Grouping Options")
        layout.prop(pg, "bake_grouping_options", text="")

        layout.separator(type="LINE")

        ### Output Textures ###
        layout.label(text="Textures to bake")

        row = layout.row()
        row.prop(pg , "albedo")
        row.prop(pg , "roughness")
        row.prop(pg , "metallic")
        row.prop(pg , "normal")

        layout.separator(type="LINE")

        ### Output Settings ###
        layout.label(text="Output Settings")

        # Render Device
        layout.prop(pg, "render_device", text="Device")

        # Render Samples
        row = layout.row()
        row.label(text="Render Samples")
        row.prop(pg, "render_samples", text="")

        # Texture resolution
        row = layout.row()
        row.label(text="Resolution")
        row.prop(pg, "bake_width", text="width")
        row.prop(pg, "bake_height", text="height")
        
        # Save Settings
        row = layout.row()
        row.prop(pg, "file_type", text="File Type")
        row = layout.row()
        row.prop(pg, "save_to_disk" , text="Save to disk")
        row.prop(pg, "output_path", text="")

        layout.separator(type="LINE")

        # Naming conventions
        layout.label(text="Naming Convention")
        layout.prop(pg, "naming_convention", text="Format")
        layout.prop(pg, "output_name_text1", text="Text1")
        layout.prop(pg, "output_name_text2", text="Text2")
        layout.prop(pg, "output_name_separator", text="Separator")

        layout.prop(pg, "batch_name_override", text="Override batch name")
        if pg.batch_name_override:
            layout.prop(pg, "batch_name", text="Batch name")

        layout.prop(pg, "texture_type_name_override", text="Texture type name override")
        if pg.texture_type_name_override:
            layout.prop(pg, "output_albedo_name", text="Albedo")
            layout.prop(pg, "output_roughness_name", text="Roughness")
            layout.prop(pg, "output_metallic_name", text="Metallic")
            layout.prop(pg, "output_normal_name", text="Normal")

        layout.separator(type="LINE")

        # Versioning
        layout.label(text="Versioning")
        layout.prop(pg, "overwrite_previous_save", text="Overwrite previous save")
        if not pg.overwrite_previous_save:
            layout.label(text= "File versioning suffix [eg: duplicate_V0,1,2..n ]:")
            layout.prop(pg, "file_versioning_suffix", text="")