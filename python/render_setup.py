import mtoa.aovs
import maya.cmds as cmd


################################################################################
#
#    NOTE: As I have not found Arnold python AOV API anywhere, the best 
#    reference I have, besides random Google search examples, is the python
#    code located in 
#
#    /Program Files/Autodesk/Arnold/maya2020/scripts/mtoa/aovs.py
#


aov_dict = {}
component_aovs = [ "diffuse", "specular" ]
denoised_aovs = [ "diffuse", "specular" ] # TO-DO (NOTE: include only "color" AOVs, not other information)


################################################################################
#
#
def updateAOVDict():
    global aov_dict
    aovs = mtoa.aovs.AOVInterface().getAOVNodes(names=True)
    aov_dict = dict(aovs)


################################################################################
#
#
def addCryptomatteAOVs():
    crypto_aovs = ["crypto_asset", "crypto_material", "crypto_object"]
    for a in crypto_aovs:
        if a not in aov_dict:
            mtoa.aovs.AOVInterface().addAOV(a, aovShader="cryptomatte" )


################################################################################
#
#
def addStandardAOV( aov_name ):
    if aov_name not in aov_dict:
        mtoa.aovs.AOVInterface().addAOV(aov_name)


################################################################################
#
#
def addMotionVectorsAOV():
    aov_name = "motionvector"
    if aov_name not in aov_dict:
        addStandardAOV(aov_name)
    # Enable motion blur with "instantaneous shutter" option
    cmd.setAttr("defaultArnoldRenderOptions.motion_blur_enable", 1)
    cmd.setAttr("defaultArnoldRenderOptions.ignoreMotionBlur", 1)


################################################################################
#
#
def configureDenoising():
    cmd.setAttr("defaultArnoldRenderOptions.denoiseBeauty", 0)    # Disable OptiX denoiser (just in case...)
    cmd.setAttr("defaultArnoldRenderOptions.outputVarianceAOVs", 1)    # Enable Arnold Denoiser AOVs

    # Update current AOVs dictionary
    updateAOVDict()

    # Add drivers for denoising additional (non-beauty) AOVs
    # More information in
    #    https://arnoldsupport.com/2021/03/22/mtoa-denoising-aovs-with-the-arnold-denoiser/   
    for aov in denoised_aovs:
        if aov in aov_dict:
            node = aov_dict[aov]
            conns = cmd.listConnections(node + ".outputs")
            if len(conns) <= 2 :    # Detect whether the variance filter has already been added because outputs have 4 connections instead of 2
                print("Configuring denoising for AOV %s (node %s)"%(aov, node))
                # Add new output driver
                cmd.connectAttr("defaultArnoldDriver.message", node + ".outputs[1].driver")
                # Add new AOV filter and set type to "variance"
                variance_filter = cmd.createNode("aiAOVFilter")
                cmd.setAttr(variance_filter + ".ai_translator", "variance", type="string")
                # NOTE: Maybe the same variance_filter node could be used for all the AOVs
                cmd.connectAttr(variance_filter + ".message", node + ".outputs[1].filter")

    # NOTE: All these AOVs should be passed to noice as "light group AOVs" in denoising script (outside Maya)


################################################################################
#
#
def configureAOVs():
    addCryptomatteAOVs()
    addStandardAOV("Z")
    addMotionVectorsAOV()
    for n in component_aovs:
        addStandardAOV(n)
    configureDenoising()


################################################################################
#
#
def setRenderCameras():
    cams = cmd.ls(cameras=True)
    non_render_cams = ["topShape", "frontShape", "sideShape", "perspShape"]
    for c in cams:
        if c in non_render_cams:
            cmd.setAttr(c + ".renderable", 0)
        else:
            # TO-DO: Decide which cameras to render
            # TO-DO: Define camera naming convention for render!!!
            # TEMPORARY: all non-default cameras are enabled to render
            cmd.setAttr(c + ".renderable", 1)

    
################################################################################
#
#    Check documentation for renderGlobals node in
#    https://help.autodesk.com/view/MAYAUL/2020/ENU/?guid=__Nodes_renderGlobals_html
#
def setRenderOutput():
    # Directory and naming
    cmd.setAttr("defaultRenderGlobals.imageFilePrefix", "<Scene>/<Scene>", type="string")

    # Merge AOVs (one EXR file instead of separated files)
    cmd.setAttr("defaultArnoldDriver.mergeAOVs", 1)    # NOTE: This is required by arnold denoiser (noice)

    cmd.setAttr("defaultRenderGlobals.outFormatControl", 0)    # default
    cmd.setAttr("defaultRenderGlobals.animation", 1)           # animation (vs. single frame)
    cmd.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)   # Frame number precedes the output type extension in file name
    cmd.setAttr("defaultRenderGlobals.extensionPadding", 4)    # Frame # padding
    cmd.setAttr("defaultRenderGlobals.periodInExt", 1)         # Period character between the filename and the file extension
    
    # Image Size options are defined in a separate node connected to renderGlobals.resolution attribute
    resolution = cmd.listConnections("defaultRenderGlobals.resolution")[0]
    cmd.setAttr(resolution + ".width", 1920)
    cmd.setAttr(resolution + ".height", 1080)


################################################################################
#
#    Scene render configuration
#
def configureRender():
    # Populate AOV dictionary
    updateAOVDict()
    configureAOVs()
    setRenderCameras()
    setRenderOutput()


################################################################################
#
#
if __name__ == "__main__":
    pass
