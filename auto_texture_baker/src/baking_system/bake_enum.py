"""
Enum for bake mode
"""

# NOTE: This is currently unused for now
import enum 
class BakeMode(enum.Enum):
    BAKE_BATCH = 0
    BAKE_SEPARATE_OBJ = 1 
    BAKE_SEPARATE_MAT = 2
