import maya.cmds as cmd

'''

Functions defined in this module:

    checkPerFaceMaterialsInAnyInstance(shape)
    getPerFaceMaterialAssignment(transf, shape)
    reassignPerFaceMaterialsToInstances(transform, shape, all_shape_instances)

Entry points (called from Shelf buttons):

    reassignMaterials()

'''


###############################################################################
#
#   Get transform and shape from a single object selection considering
#   instanced nodes (shape is common, transforms are different)
#
#   Returns a list with three elements: transform and shape and 
#   instances_array (in this order)
#
#   NOTE: This function is not currently used. Just ignore it.
#   Nothing to see here, move along...
#
###############################################################################
def getInstancedNodeFromSelection():
    # Get all possible paths for the (potentially) instanced node
    shape_paths = cmd.ls(selection=True, dag=True, leaf=True, allPaths=True, long=True)
    if not shape_paths:
        return
    #print("Shape_paths: ", shape_paths)
    transform = cmd.ls(selection=True)
    #print("Transforms: ", transform)

    if len(transform) == 1:
        transform = transform[0]
    else:
        cmd.error("Only ONE node must be selected")
        return

    #print("trans: ", transform)
    shape = [s for s in shape_paths if transform in s]
    if not shape or len(shape) > 1:
        cmd.error("Only ONE shape must be selected")
        return
    shape = shape[0]
    #print("shape: ", shape)

    #WARNING: when selecting nodes higher in hierarchy, the transform may not be the direct parent of the shape (may be a higher group)
    # TO-DO: fix!

    return [transform, shape, shape_paths]


###############################################################################
#
#   Check if there is more than one shadingEngine connected to a shape
#   in any of the instances of this shape
#
#   Returns True if there are several SEs, otherwise False
#
###############################################################################
def checkPerFaceMaterialsInAnyInstance(shape):
    if not shape:
        cmd.warning("No shape selected")
        return

    # Shading engines connected to the shape node
    sgs = cmd.listConnections(shape, type='shadingEngine')
    return sgs and len(sgs) > 1


###############################################################################
#
#    Returns a map of faces with shadingEngine as key
#
###############################################################################
def getPerFaceMaterialAssignment(transf, shape):
    if not shape:
        cmd.warning("No shape selected")
        return

    mat2face = {}
    # Shading engines connected to the shape node
    sgs = cmd.listConnections(shape, type='shadingEngine')
    #print(sgs)
    if sgs:
        for sg in sgs:
            faces = []
            members = cmd.sets(sg, q=True)
            if members:
                for item in members:
                    # WARNING: delimit node name (with string-start, "|", or ".") to avoid wrongly identify nodes with names that are a superset of the one we are searching
                    if ("|"+transf+"|") in item or item.startswith(transf+"|") or ("|"+transf+".") in item or item.startswith(transf+"."):
                         faces.append(item)
            if faces:
                mat2face[sg] = faces
    return mat2face


###############################################################################
#
#    Reassign per-face materials to every other instance of the shape
#
###############################################################################
def reassignPerFaceMaterialsToInstances(transform, shape, all_shape_instances):
    mat2face = getPerFaceMaterialAssignment(transform, shape)
    if not mat2face:
        # No material, assign default one
        print("No material. Assigning default SG")
        cmd.sets(transform, e=True, forceElement="initialShadingGroup")
        mat2face = getPerFaceMaterialAssignment(transform, shape)
    # For each instane of the shape...
    for s in all_shape_instances:
        if not ("|"+transform+"|") in s and not s.startswith(transform+"|"):  # ...except the original (selected) one, of course
            if len(mat2face) == 1:
                # Per object material assignment (or some faces with no material)
                sg = mat2face.keys()[0]
                cmd.sets(s, e=True, forceElement=sg)
            else:
                for sg in mat2face:
                    for f in mat2face[sg]:
                        new_faces = f.replace(transform, s)
                        cmd.sets(new_faces, e=True, forceElement=sg)


###############################################################################
#
#    Reassign per-face materials to every other instance of the shape
#
###############################################################################
def reassignMaterials():
    transforms = cmd.ls(selection=True)
    for t in transforms:
        shape = cmd.listRelatives(t, shapes=True, fullPath=True)
        all_shape_instances = cmd.ls(shape, allPaths=True)
        reassignPerFaceMaterialsToInstances(t, shape, all_shape_instances)


        import maya.cmds as cmds


###############################################################################
#
#    Create a new shader (and shading group) of type shaderType and with
#    name nodeName
#
#    Returns shader name and SG name
#
###############################################################################
def createShader(shaderType, nodeName):
    shaderName = cmds.shadingNode(shaderType, asShader=True, name=nodeName)
    sgName = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=(shaderName + "SG"))
    cmds.connectAttr(shaderName + ".outColor", sgName + ".surfaceShader")
    return (shaderName, sgName)

###############################################################################
#
#    Create a new shader of type newShaderType, apply it to all elements where
#    existingShader is currently applied, then copy attributes from 
#    existingShader to the new shader (currently only .baseColor)
#    The node name of the new shader will be the original one with suffix
#    appended to it
#
#    This code was originally written to convert aiStandardSurface to aiToon
#    so this is the only cased that has been tested
#
#    NOTE: The original shaders are kept. If you want to remove them, use
#    Edit > Delete Unused Nodes in the Hypershade menu
#
###############################################################################
def convertShader(existingShader, newShaderType, suffix):
    shader_node = cmds.ls(existingShader)
    if ( shader_node ):
        shader_node = shader_node[0]
    
    node_type = cmds.nodeType(shader_node)
    if node_type != "aiStandardSurface":
        cmds.error("WRONG node type: %s - should be aiStandardSurface"%node_type)
        return

    SGs = cmds.listConnections(shader_node, type="shadingEngine")
    if len(SGs) > 1:
        cmds.error("The material is applied to more than one Shading Group")
        return

    # Query geometry with original shaders applied    
    geo = cmds.listConnections(SGs, type="mesh")

    new_node_name = shader_node + suffix
    created_nodes = createShader(newShaderType, new_node_name)
    new_node_name = created_nodes[0]
    new_SG_name = created_nodes[1]

    # Adding geometry to new SG
    cmds.select(geo)
    cmds.sets( e=True, forceElement=new_SG_name)

    # Transfer shader attributes from aiStandardSurface to aiToon
    # Add all attributes and correspondences you need. Only base color is
    # copied in this example
    
    cmds.setAttr(new_node_name + ".baseColorR", cmds.getAttr(shader_node+".baseColorR"))
    cmds.setAttr(new_node_name + ".baseColorG", cmds.getAttr(shader_node+".baseColorG"))
    cmds.setAttr(new_node_name + ".baseColorB", cmds.getAttr(shader_node+".baseColorB"))


###############################################################################
#
#    Replace all aiStandarSurfaces materials in the scene to aiToon, keeping
#    the original baseColor
#
###############################################################################
def convertAllAiStandardSurfaceToAiToon():
    SGs = cmds.ls(type="aiStandardSurface")
    for sg in SGs:
        convertShader(sg, "aiToon", "Toon")
