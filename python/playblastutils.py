import maya.cmds as cmd


'''

Functions defined in this module:

Entry points (called from Shelf buttons):

    configureHardwareRenderHQ()

'''


###############################################################################
#
#   Configure hardware render for high quality
#
#   This script configures the Viewport 2.0 hardware render options for
#   high quality visualization (especially showing wireframe)
#   This is meant to be used for generating high quality playblasts for
#   3D animatics or model presentations for a demo reel
#
def configureHardwareRenderHQ():
    cmd.setAttr("hardwareRenderingGlobals.enableTextureMaxRes", 0)  # Clamp texture resolution
    cmd.setAttr("hardwareRenderingGlobals.motionBlurEnable", 1)
    cmd.setAttr("hardwareRenderingGlobals.motionBlurSampleCount", 16)   # Motion blur sample count
    cmd.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)   # SSAO
    cmd.setAttr("hardwareRenderingGlobals.lineAAEnable", 1) # Smooth wireframe  
    cmd.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)    # Multisampling anti-aliasing
    cmd.setAttr("hardwareRenderingGlobals.aasc", 16)    # Sample count (AA)
