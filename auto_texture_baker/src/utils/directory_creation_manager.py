"""
This module handles creating directory for saving output files
"""

import os
import bpy

def create_save_directory(save_dir):
    """
    Create directory for saving output results if not exist
    """

    try:
        abs_save_dir = bpy.path.abspath(save_dir)
        os.makedirs(abs_save_dir, exist_ok = True)

    # pylint: disable=W0718
    except Exception as e:
        return False, e

    return True, ""
