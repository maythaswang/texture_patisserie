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
        layout.operator("autobake.bake_texture", text="Bake Selected Maps")

        ### Bake settings 
        layout.label(text="Bake Settings")

        row = layout.row() 
        row.prop(scene.pg_bake_settings, "bake_separately", text="Bake Separately")

        layout.separator(type="LINE")

        ### Output Textures ###
        layout.label(text="Textures to bake")

        row = layout.row()
        row.prop(scene.pg_bake_settings , "albedo")
        row.prop(scene.pg_bake_settings , "roughness")
        row.prop(scene.pg_bake_settings , "metallic")
        row.prop(scene.pg_bake_settings , "normal")

        layout.separator(type="LINE")

        ### Output Settings ###
        layout.label(text="Output Settings")

        # Render Device
        layout.prop(scene.pg_bake_settings, "render_device", text="Render device")

        # Render Samples
        row = layout.row()
        row.label(text="Render Samples")
        row.prop(scene.pg_bake_settings, "render_samples", text="")

        # Texture resolution
        row = layout.row()
        row.label(text="Texture Resolution")
        row.prop(scene.pg_bake_settings, "bake_width", text="width")
        row.prop(scene.pg_bake_settings, "bake_height", text="height")
        
        # Save Settings
        row = layout.row()
        row.prop(scene.pg_bake_settings, "file_type", text="File Type")
        row = layout.row()
        row.prop(scene.pg_bake_settings, "save_to_disk" , text="Save to disk")
        row.prop(scene.pg_bake_settings, "output_path", text="")
