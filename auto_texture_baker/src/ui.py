"""
Bake Plugin UI 
"""
import bpy

class PROPERTIES_PT_bake_panel(bpy.types.Panel):
    """Panel for selecting nodes to bake"""

    bl_idname = "MATERIAL_PT_bake_textures"
    bl_label = "Auto Texture Baker"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.operator("autobake.bake_texture", text="Bake Selected Maps")
        layout.label(text="Select Texture to bake!")

        row = layout.row()
        row.prop(scene.pg_bake_settings , "albedo")
        row.prop(scene.pg_bake_settings , "roughness")
        row.prop(scene.pg_bake_settings , "metallic")
        row.prop(scene.pg_bake_settings , "normal")

        layout.label(text="Texture Resolution")
        row = layout.row()
        row.prop(scene.pg_bake_settings, "bake_width" )
        row.prop(scene.pg_bake_settings, "bake_height" )
        
        
        layout.label(text="Output Location")
        row = layout.row()
        row.prop(scene.pg_bake_settings, "save_to_disk" , text="Save to disk")
        row = layout.row()
        row.prop(scene.pg_bake_settings, "output_path", text="")

        layout.label(text="Render Settings")
        layout.prop(scene.pg_bake_settings, "render_samples", text="Render Samples")
