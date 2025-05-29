"""
Build texture and directory names based on user input
"""

def build_texture_name(cfg, bake_pass, main_name): 
    """
    Build texture name based on the configuration provided
    """

    texture_name = ""
    word_position = ["","","",""]

    name = main_name
    text1 = cfg.output_name_text1
    text2 = cfg.output_name_text2
    separator = cfg.output_name_separator

    bake_type = bake_pass


    if not cfg.bake_separately:
        if cfg.batch_name_override:
            name = cfg.batch_name
        else:
            name = main_name

    if cfg.texture_type_name_override: 
        match bake_pass:
            case 'albedo': 
                bake_type = cfg.output_albedo_name
            case 'albedo': 
                bake_type = cfg.output_albedo_name
            case 'metallic': 
                bake_type = cfg.output_metallic_name
            case 'normal': 
                bake_type = cfg.output_normal_name

    match cfg.naming_convention: 
        case "name_type_text1_text2":
            word_position = [name, bake_type, text1, text2]
        case "text1_name_type_text2":
            word_position = [text1, name, bake_type, text2]
        case "text1_text2_name_type":
            word_position = [text1, text2, name, bake_type]
        case "text1_type_name_text2":
            word_position = [text1, bake_type, name, text2]

    word_position = [word for word in word_position if word != ""]
    texture_name = separator.join(word_position)

    return texture_name
