"""
Enum for bake mode
"""

# NOTE: This is currently unused for now
import enum 
class BakeGroupingOptions(enum.Enum):
    BAKE_BATCH = 0
    BAKE_SEPARATE_OBJ = 1 
    BAKE_SEPARATE_MAT = 2
 
def get_grouping_options_from_string(mode_str: str) -> BakeGroupingOptions:
    """
    Get BakeGroupingOptions from string
    """

    mode_str = mode_str.strip().lower()
    mode_map = {
        "bake_batch": BakeGroupingOptions.BAKE_BATCH,
        "bake_separate_obj": BakeGroupingOptions.BAKE_SEPARATE_OBJ,
        "bake_separate_mat": BakeGroupingOptions.BAKE_SEPARATE_MAT
    }
    
    if mode_str in mode_map:
        return mode_map[mode_str]
    else:
        return -1