# TEXTURE OVEN - Blender Extension


# Currently supports 
- Principled BSDF
  - Metallic
  - Roughness
  - Albedo
  - Normal
- Single Object Multi Texture 
- Multiple Object Separately
- Multiple Object in one UV
- Texture Export

# Will implement
- Multires
- MultiUV 
- Channel Packing 
- Formatting (prefix, suffix, name overriding)
- Directory Creation
- Bake Queue

# Issues 
- Export format issue
- Currently there is an issue where the bake result will never set itself to clear bg
- The nodes going into different output cannot be the same otherwise there will be issues when rewrangling internally