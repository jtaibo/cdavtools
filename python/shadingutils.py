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
