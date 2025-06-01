# Texture Patisserie - Blender Add-on

[//]: # (Shields basic info setup)
[shield-release-date]:https://img.shields.io/badge/release_date-2025.06.01-blue
[shield-current-blender-version]:https://img.shields.io/badge/blender_version-4.4.0-red

[//]: # (Shields status setup)
[shield-compatible]:https://img.shields.io/badge/compatible-green
[shield-incompatible]:https://img.shields.io/badge/incompatible-red
[shield-active]:https://img.shields.io/badge/active-green
[shield-disabled]:https://img.shields.io/badge/disabled-red

[//]: # (Shields version setup)
[shield-version-0.0.1]:https://img.shields.io/badge/version-0.0.1-blue
[shield-version-0.0.2]:https://img.shields.io/badge/version-0.0.2-important

[//]: # (Alt texts)
[compatible]:compatible
[incompatible]:incompatible
[active]:active
[disabled]:disabled
[v0.0.1]:v0.0.1
[v0.0.2]:v0.0.2

![v0.0.2][shield-version-0.0.2] ![2025.06.01][shield-release-date] ![4.4.0][shield-current-blender-version]

A Blender Add-on for streamlining the process of baking and exporting materials to PBR textures in a few clicks.

※This add-on is still being maintained, I will be adding more features whenever I am free or in need of some specific functionalities! :)

<p align="center">
    <img src="images/bake_screen.png" width="480">
</p>

## Version Compatibility
This addon works for blender version 4.4.0 and should be backward compatible. 
However, I haven't checked other for other versions yet since this add-on was initially created for personal use only. 


|Blender version| Add-on Version | Status| 
| ---- | --- | ---- |
|4.4.0 | ![v0.0.2][shield-version-0.0.2] | ![compatible][shield-compatible] |

## Supported Features 

|Name                                          | Description | Version | Status| 
|---|---|---|---|
| PBR texture baking                           | Bake materials into metallic, roughness, albedo, normal maps (more coming soon)                 | ![v0.0.1][shield-version-0.0.1] | ![active][shield-active]    | 
| Principled BSDF baking                       | Bake materials that uses Principled BSDF.                                                       | ![v0.0.2][shield-version-0.0.2] | ![active][shield-active]    |
| Single shader material baking                | Bake materials with only one shader node.                                                       | ![v0.0.2][shield-version-0.0.2] | ![active][shield-active]    | 
| Texture Export                               | Saves texture to defined directory when write to device.                                        | ![v0.0.2][shield-version-0.0.2] | ![active][shield-active]    |
| Batch baking                                 | Baking multiple objects into one texture image for creating texture atlas                       | ![v0.0.2][shield-version-0.0.2] | ![active][shield-active]    | 
| Separate object baking                       | Baking multiple objects into each of their own texture image                                    | ![v0.0.2][shield-version-0.0.2] | ![active][shield-active]    |
| Separate material baking                     | Baking multiple objects and each of their material separately into their own texture image      | ![v0.0.1][shield-version-0.0.1] | ![][shield-disabled]  | 
| Texture Output configurations                | Supports selecting render device, samples, resolution, filetype, alpha channel, texture margins | ![v0.0.2][shield-version-0.0.2] | ![active][shield-active]    |   
| Modifiable naming convention and Presets     | User adjustable naming conventions based on the provided presets.                               | ![v0.0.2][shield-version-0.0.2] | ![active][shield-active]    |
| Batch naming convention                      | Allow overriding default object name for batches                                                | ![v0.0.2][shield-version-0.0.2] | ![active][shield-active]    |
| Versioning naming convention                 | Use user specified suffixes when duplicated textures are saved to device                        | ![v0.0.2][shield-version-0.0.2] | ![active][shield-active]    |
| Output directory creation                    | Create subdirectories for both batch and separate baking mode if used                           | ![v0.0.2][shield-version-0.0.2] | ![active][shield-active]    |
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



In case anyone wants to go through the code. Most files are documented with docstrings, I did try to be as detailed as possible but there are still some disrepancy in conventions between some files so please do we aware of that.

### Future plans (No promises)
- Normals swizzle based on engine
- High to Low-poly baking
- Bake Queue and presets
- Channel Packing

## License 
This project is distributed under [GPL-v3.0](LICENSE)
