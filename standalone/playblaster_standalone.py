#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#

import os
import sys
import re
#import glob
import maya.standalone
import maya.cmds as cmd


###############################################################################
#   Configure a decent visual quality if the GPU allows it
#   (disable if something breaks)
#
def configureHardwareRender():
    cmd.setAttr("hardwareRenderingGlobals.enableTextureMaxRes", 0)  # Clamp texture resolution
    cmd.setAttr("hardwareRenderingGlobals.motionBlurEnable", 1)
    cmd.setAttr("hardwareRenderingGlobals.motionBlurSampleCount", 16)   # Motion blur sample count
    cmd.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)   # SSAO
    cmd.setAttr("hardwareRenderingGlobals.lineAAEnable", 1) # Smooth wireframe  
    cmd.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)    # Multisampling anti-aliasing
    cmd.setAttr("hardwareRenderingGlobals.aasc", 16)    # Sample count (AA)


###############################################################################
#   Playblast for a scene
#
def do_playblast(filename, playblast_path):
    print("Opening scene :", filename)
    opened_file = cmd.file(filename, o=True, f=True)

    configureHardwareRender()

    # Check/select camera and create the playblast

    #cmd.lookThru( "modelPanel1", "cam_turntableShape1" )
    #cmd.setFocus( "modelPanel1" )
    # LookThrou and setFocus don't work in headless standalone mode. The trick is to set the playblast camera as the only renderable one
    #cameras = cmd.ls(type="camera")
    #for cam in cameras :
        #print("Camera %s renderable: %s"%(cam, cmd.getAttr(cam+".rnd")))
        #cmd.setAttr(cam + ".rnd", 0)
    #cmd.setAttr("cam_turntable1.rnd", 1)

    cmd.playblast(filename=playblast_path, forceOverwrite=True, viewer=False, format="qt", compression="H.264", width=1920, height=1080, quality=100, percent=100)


print("Starting Maya")
maya.standalone.initialize("Python")
#cmds.loadPlugin("Mayatomr") # Load all plugins you might need

#filename="D:\\Google Drive\\Almacen\\CDAV\\Materiales&Iluminacion\\maya_projects\\MEI\\02_prod\\scenes\\test_playblast_v01.mb"

# TO-DO: Integrate with CDAV-UDC Pipeline Management System
proj_path = "X:/ProyAnim/Universidade da Coruña/alstroemeria - Documentos/ALS"

# Set project (DON'T FORGET TO SET PROJECT! EVER!)
cmd.workspace(proj_path + "/02_prod", openWorkspace=True)

###############################################################################
# TO-DO: Selection of scenes to playblast

scenes_list = []
proj_id = "ALS"
path = proj_path + "/02_prod/scenes/"

stage_dir = "00_layout"
stage = "layout"

sequence_dirs = [ d for d in os.listdir(path) if re.match(r'sq\d*', d) ]
for seq in sequence_dirs:
    shot_dirs = [ s for s in os.listdir(path+"/"+seq) if re.match(r'sh\d*', s) ]
    for shot in shot_dirs:
        layout_shot_files = [ f for f in os.listdir(path+"/"+seq+"/"+shot+"/"+stage_dir) if re.match(proj_id + "_" + stage + r'_sq\d*_sh\d*_tk\d*\.mb', f) ]
        if layout_shot_files:
            scene_path = path+"/"+seq+"/"+shot+"/"+stage_dir + "/" + layout_shot_files[-1]  # Get last element (more recent take)
            scenes_list.append(scene_path)

###############################################################################

for scene in scenes_list:
    output_file = os.path.splitext(os.path.basename(scene))[0]

    output_path = "X:/tmp/test_playblast/" + output_file
    print("Generating playblast for scene %s in %s..."%(scene, output_file))
    do_playblast(scene, output_path)


print("Done")
