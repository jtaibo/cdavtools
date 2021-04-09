import maya.cmds as cmd

'''
Functions defined in this module:

    getInstancedNodeFromSelection()
    checkPerFaceMaterialsInAnyInstance(shape)
    getPerFaceMaterialAssignment(transf, shape)

'''


###############################################################################
#
#   Get transform and shape from a single object selection considering
#   instanced nodes (shape is common, transforms are different)
#
#   Returns a list with two elements: transform and shape (in this order)
#
def getInstancedNodeFromSelection():
    # Get all possible paths for the (potentially) instanced node
    shape_paths = cmd.ls(selection=True, dag=True, leaf=True, allPaths=True, long=True)
    if not shape_paths:
        return
    #print("shape_paths: ", shape_paths)
    transform = cmd.ls(selection=True)
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

    return [transform, shape]


###############################################################################
#
#   Check if there is more than one shadingEngine connected to a shape
#   in any of the instances of this shape
#
#   Returns True if there are several SEs, otherwise False
#
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
            #print(members)
            for item in members:
                if transf in item:
                     faces.append(item)
            if faces:
                mat2face[sg] = faces
    return mat2face

