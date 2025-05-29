"""
Enum for bake mode
"""

import enum 
class BakeMode(enum.Enum):
    BAKE_BATCH = 0
    BAKE_SEPARATE_OBJ = 1 
    BAKE_SEPARATE_MAT = 2