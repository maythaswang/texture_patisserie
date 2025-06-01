# Texture Patisserie - Blender Add-on

A Blender Add-on for streamlining the process of baking and exporting materials to PBR textures in a few clicks.

<p align="center">
    <img src="images/bake_screen.png" width="480">
</p>

## Version Compatibility
This addon works for blender version 4.4.0 and should be backward compatible. 
However, I haven't checked other for other versions yet since this add-on was initially created for personal use only. 

|Blender version| Add-on Version | Status| 
| ---- | --- | ---- |
|4.4.0 | 0.0.2 | Compatible |

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
## Installation and Usage
Simply download the latest release (will be up soon)

Afterwards, open blender and go to `Edit > Preferences > Add-ons`. Click the dropdown icon and select `Install from disk` then select the zip file containing the add-on.

<p align="center">
    <img src="images/install_process.png" width="480">
</p>

After the installation is complete, you can find the addon under `Properties Panel > Render > Texture Patisserie` and you are now ready to go!

## Demos

## Known Issues 
- Export format doesn't conform fully to the specified format.
- The nodes going into different output cannot be the same otherwise there will be issues when rewrangling internally. Right now consider making 

## Notes

※This add-on is still being maintained, I will be adding more features whenever I am free or in need of some specific functionalities!

### Future plans (No promises)
- Normals swizzle based on engine
- High to Low-poly baking
- Bake Queue and presets
- Channel Packing 