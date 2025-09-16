# ==============================================================================
# content           = Init Module Setup ( User )
# version           = V.1.0
# date              = 11/07/2025
# dependencies      = Python
# license 			= WTFP License
# author            = Faris Nabil Arsyad
#                   - faris@lmn.co.id
#                   - trr.faris@gmail.com
# ==============================================================================

# ==============================================================================
# MODULES
import bpy

bl_info = {
    "name": "Startup LMN",
    "category": "Object",
    "blender": (4, 5, 0),
    "version": (1, 0, 0),
    "author": "Faris Nabil Arsyad",
    "description": "LMN Startup Addon",
}


def register():
    from ProjectA.Blender.Api.pipeline import BlenderHostLMN

    host_LMN = BlenderHostLMN()
    host_LMN.install()
    # bpy.ops.preferences.addon_enable(module="startup_lmn")


def unregister():
    pass
