# Texture Patisserie - Blender Add-on

A Blender Add-on for streamlining the process of baking and exporting materials to PBR textures in a few clicks.

<p align="center">
    <img src="images/bake_screen.png" width="480">
</p>


## Installation 

## Supported Features 

|Name| Description | Version | Status| 
|---|---|---|---|
| PBR texture baking | Bake materials into metallic, roughness, albedo, normal maps (more coming soon) | 0.0.1 | Active | 
| Principled BSDF baking | Bake materials that uses Principled BSDF. | 0.0.2  |   |
| Single shader material baking | Bake materials with only one shader node.  |  0.0.2 |   | 
| Texture Export | Saves texture to defined directory when write to device. | 0.0.2 | |
| Batch baking | Baking multiple objects into one texture image for creating texture atlas | 0.0.2 | | 
| Separate object baking | Baking multiple objects into each of their own texture image | 0.0.2 | |
| Separate material baking | Baking multiple objects and each of their material separately into their own texture image | 0.0.1 | Inactive | 
| Texture Output configurations | Supports selecting render device, samples, resolution, filetype, alpha channel, texture margins | 0.0.2 | Active |   
| Modifiable naming convention and Presets | User adjustable naming conventions based on the provided presets. | 0.0.2 | Active |
| Batch naming convention | Allow overriding default object name for batches | 0.0.2 | |
| Versioning naming convention | Use user specified suffixes when duplicated textures are saved to device | 0.0.2 ||
| Output directory creation | Create subdirectories for both batch and separate baking mode if used | 0.0.2 | |
-------

## Demos

### Future plans
- Hi-poly -> low-poly baking
- Normals swizzle
- Channel Packing 
- Bake Queue and presets

### Known Issues 
- Export format issue
- The nodes going into different output cannot be the same otherwise there will be issues when rewrangling internally


※This add-on is still being maintained, I will be adding more features whenever I am free or in need of some specific functionalities!