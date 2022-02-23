import re
import os
import math
import maya.cmds as cmd
import maya.OpenMaya as om


###############################################################################
#   Bounding Box
###############################################################################
class BoundingBox():

    def __init__(self, node):
        self.bbox = cmd.exactWorldBoundingBox(node)

    def get(self):
        return self.bbox

    def width(self):
        return self.bbox[3] - self.bbox[0]

    def height(self):
       return self.bbox[4] - self.bbox[1]

    def depth(self):
       return self.bbox[5] - self.bbox[2]

    def center(self):
        return [ (self.bbox[0] + self.bbox[3]) / 2., (self.bbox[1] + self.bbox[4]) / 2., (self.bbox[2] + self.bbox[5]) / 2. ]

    def maxDim(self):
        return max( self.width(), self.height(), self.depth() )

    def diameter(self):
        return math.sqrt(self.width()*self.width() + self.height()*self.height() + self.depth()*self.depth())

    def radius(self):
        return self.diameter()/2.

###############################################################################
#   Create a wireframe cube to show bounding box (debug information)
#   Parameter is a 6-value array such as returned by
#       bbox = cmd.exactWorldBoundingBox( scene_objects )
#   Returns the box node
###############################################################################
def createDebugBoundingBox(bbox, name="bbox", hidden=False):
    bb_w = bbox[3] - bbox[0]
    bb_h = bbox[4] - bbox[1]
    bb_d = bbox[5] - bbox[2]
    dbg_bbox = cmd.polyCube(width=bb_w, height=bb_h, depth=bb_d, name=name)
    cmd.xform(dbg_bbox, translation=[bbox[0]+bb_w/2, bbox[1]+bb_h/2, bbox[2]+bb_d/2])
    print("dbg_bbox=", dbg_bbox)
    # Display as template
    cmd.setAttr(dbg_bbox[0] + ".template", 1)
    # Hide the bbox
    if hidden:
        cmd.setAttr(dbg_bbox[0] + ".visibility", 0)
    return dbg_bbox


###############################################################################
#
#   Selections
#
###############################################################################

###############################################################################
#   Return the current selection, so it can be saved to restore it later
#   Returns an MSelectionList
###############################################################################
def getSelection():
    sel = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(sel)
    return sel

###############################################################################
#   Set the current selection (from a previously saved one)
###############################################################################
def setSelection(sel):
    om.MGlobal.setActiveSelectionList(sel)

###############################################################################
#   Check if a node name is unique in the scene
###############################################################################
def isNameUnique(n):
    query = cmd.ls(n)
    if len(query) > 1:
        return False
    else:
        return True


###############################################################################
#
#   Instances
#
###############################################################################

###############################################################################
#   Get the instances in the scene
###############################################################################
def getInstances():
    instances = []
    iterDag = om.MItDag(om.MItDag.kBreadthFirst)
    while not iterDag.isDone():
        instanced = om.MItDag.isInstanced(iterDag)
        if instanced:
            instances.append(iterDag.fullPathName())
        iterDag.next()
    return instances

###############################################################################
#   Uninstance selected objects
###############################################################################
def uninstance(instances):
    while len(instances):
        parent = cmd.listRelatives(instances[0], parent=True)[0]
        cmd.duplicate(parent, renameChildren=True)
        cmd.delete(parent)
        instances = getInstances()

###############################################################################
#   Remove all the instances in the scene
###############################################################################
def uninstanceAll():
    uninstance( getInstances() )

###############################################################################
#   Select all the instances in the scene
###############################################################################
def selectInstances():
    cmd.select( getInstances() )


###############################################################################
#
#   Importing and referencing
#
###############################################################################

###############################################################################
#   Importing a file
###############################################################################
def importFile(file_path, group_name):
    the_file = cmd.file(file_path, i=True, namespace=group_name+"NS", groupReference=True, groupName=group_name)
    return the_file

###############################################################################
#   Create a reference to a file
###############################################################################
def referenceFile(file_path, group_name):
    the_file = cmd.file(file_path, reference=True, groupReference=True, groupLocator=True, lockReference=True, groupName=group_name)
    return the_file


###############################################################################
#
# Scene cleanup
#
###############################################################################

###############################################################################
#   Delete channels and construction history for the group
###############################################################################
def deleteChannelsAndHistory(group_name):
    cmd.delete(group_name, constructionHistory=True, channels=True, all=True)

###############################################################################
#   Delete channels and construction history for all the scene
###############################################################################
def deleteChannelsAndHistoryForAll():
    cmd.delete(constructionHistory=True, channels=True, all=True)


###############################################################################
#   Delete empty groups
###############################################################################
def deleteEmptyGroups():
    done = False
    while not done:
        empty_groups = checkEmptyGroups(False)
        if not empty_groups:
            done = True
        else:
            for g in empty_groups:
                # Check if group exists or use capture exceptions in delete()
                # because in case of references, the group may already have been deleted
                if cmd.objExists(g):
                    cmd.delete(g)

###############################################################################
#   Rename non-unique-name nodes
###############################################################################
def renameNonUniqueNodes():
    nodes = cmd.ls(shortNames=True)
    for n in nodes:
        if '|' in n:
            # Non-unique names have full path
            short_name = n.rpartition('|')[-1]
            if not isNameUnique(short_name):
                cmd.rename(n, short_name + "#")

##################################################
#
# Cleanup modeling asset for production
#
#	- Delete history
#	- Delete channels
#   - Delete empty groups
#	- Import references
#   - Unlock references?
#	- Convert instances to objects
#	- Freeze transformations
#
##################################################
def cleanupModelingAssetForProduction():
    # import and unlock? references
    deleteChannelsAndHistoryForAll()
    renameNonUniqueNodes()
    deleteEmptyGroups()
    uninstanceAll()
    # freeze transformations

###############################################################################
#   Check for copy-pasted nodes
###############################################################################
def checkCopyPastedNodes(ui=True):
    nodes = cmd.ls()
    copypasted_nodes = []
    for n in nodes:
        if "pasted__" in n:
            copypasted_nodes.append(n)
    if ui:
        if copypasted_nodes:
            cmd.warning( str(len(copypasted_nodes)), "copy-pasted nodes detected:", copypasted_nodes )
        else:
            cmd.warning("NO copy-pasted nodes. Nice!")
    return copypasted_nodes

###############################################################################
#   Check for non-unique node names
###############################################################################
def checkNonUniqueNodeNames(ui=True):
    nodes = cmd.ls(shortNames=True)
    non_unique_names = []
    for n in nodes:
        if '|' in n:
            non_unique_names.append(n)
    if ui:
        if non_unique_names:
            cmd.warning( str(len(non_unique_names)), "non-unique node names detected:", non_unique_names )
        else:
            cmd.warning("NO duplicated node names. Nice!")
    return non_unique_names

###############################################################################
#   Check for illegal characters in node names
###############################################################################
def checkIllegalNodeNames(ui=True):
    nodes = cmd.ls(shortNames=True)
    illegal_node_names = []
    regex = re.compile('[^A-Za-z0-9_|]')
    for n in nodes:
        if regex.search(n) :
            illegal_node_names.append(n)
    if ui:
        if illegal_node_names:
            cmd.warning( str(len(illegal_node_names)), "illegal node names detected:", illegal_node_names )
        else:
            cmd.warning("NO illegal node names. Nice!")
    return illegal_node_names

###############################################################################
#   Check for empty groups
###############################################################################
def checkEmptyGroups(ui=True):
    # Save the original selection in the scene
    orig_sel = getSelection()

    cmd.select(allDagObjects=True, hierarchy=True)
    objs = cmd.ls(selection=True, long=True)    # ***** CHECK!

    empty_groups = []

    for obj in objs:
        if cmd.nodeType(obj) == "transform":
            # Check empty groups
            children = cmd.listRelatives(obj, fullPath=True)
            if not children :
                empty_groups.append(obj)
            else:
                # Consider an empty group if the children are not in the listed scene
                # (shape nodes that are not shown in the Outliner, but reachable through Hypergraph/connections with all their history)
                empty_with_children = True
                for ch in children:
                    if ch in objs:
                        empty_with_children = False
                if empty_with_children:
                    empty_groups.append(obj)

    if ui:
        if empty_groups :
            print( "Empty groups: ", empty_groups )
            cmd.warning( str(len(empty_groups)) + " empty groups" )
            cmd.select(empty_groups)
        else:
            cmd.warning( "No empty groups. Nice!" )

    # Restore the original selection in the scene
    # unless there are empty groups and UI is enabled, in which case they are selected
    if not ui or not empty_groups:
        setSelection(orig_sel)

    return empty_groups

###############################################################################
#   List UUIDs for nodes in the scene
###############################################################################
def UUIDCheck():
    #geometry = cmd.ls(geometry=True)
    #transforms = cmd.listRelatives(geometry, p=True, path=True)
    #cmd.select(transforms, r=True)

    # If empty selection, select all geometry, otherwise use the current selection
    selection = cmd.ls(sl=True)
    if not selection:
        cmd.SelectAllGeometry()

    names = cmd.ls(sl=True, long=True)
    uuids = cmd.ls(sl=True, uuid=True)

    #if len(names) != len(uuids):
    #    print("Something is wrong...")
    #    exit(-1)

    for i in range(len(names)):
        print(names[i], uuids[i])

###############################################################################
#
#   References
#
###############################################################################

###############################################################################
#   Returns a list of reference nodes in the scene
###############################################################################
def getReferences():
    return cmd.ls(type="reference")

###############################################################################
#   Returns a list of the broken references in the scene
###############################################################################
def checkBrokenReferences():
    references_to_ignore = [ "sharedReferenceNode" ]    # The sharedReferenceNode appears when unloading a reference
    refs = getReferences()
    broken_refs = []
    for r in refs:
        try:
            path = cmd.referenceQuery(r, filename=True, withoutCopyNumber=True)
            if not os.path.isfile(path):
                print("Reference %s cannot be reached at path %s"%(r, path))
                broken_refs.append(r)
        except:
            if r not in references_to_ignore:
                broken_refs.append(r)
    return broken_refs

###############################################################################
#   Writes a report of broken references (meant to be used from Maya UI)
###############################################################################
def checkBrokenReferencesUI():
    broken_refs = checkBrokenReferences()
    if ( broken_refs ):
        cmd.error("ERROR - Broken references! : %s"%broken_refs)
    else:
        cmd.warning("Everything OK")


###############################################################################
#   Count the Maya projects (directories containing workspace.mel) are in the
#   "filename" path
###############################################################################
def countMayaProjectsInPath(filename):
    count = 0
    path = ""
    clean_filename = filename.replace("\\", "/")
    dirs = clean_filename.split("/")
    for dir in dirs:
        path += dir + "/"
        if os.path.isfile(path + "workspace.mel"):
            count += 1
    return count


###############################################################################
#   Returns a list of scenes in directory, complying with the extensions
###############################################################################
def selectScenesInDirectory(path, extensions=["mb", "ma"]):
    scenes_list = []
    for root, dirs, files in os.walk( path ):
        for file in files:
            for ext in extensions:
                if file.endswith("."+ext):
                    scenes_list.append(root + "/" + file)
                    break
    return scenes_list

###############################################################################
#   Returns the path of the project containing the scene supplied as argument
###############################################################################
def getProjectPath(scene_path):

    scene_path = os.path.abspath(scene_path)
    # If path is valid
    if os.path.exists(scene_path):
        if os.path.isfile(scene_path):
            # Process parent directory
            return getProjectPath(os.path.dirname(scene_path))
        else:
            if os.path.isfile(scene_path + "/" + "workspace.mel"):
                return scene_path
            else:
                return getProjectPath(os.path.dirname(scene_path))
    else:
        print("ERROR. Invalid path: %s"%scene_path)
        return nil
