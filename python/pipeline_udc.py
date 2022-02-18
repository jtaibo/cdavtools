import glob
import os

topDirs= {
    "trans": "00_transDep",
    "dev": "01_dev",
    "pre&prod": "02_prod",
    "post": "03_post"
    }

# Asset types and directories
assetTypeAbbr = [ "ch", "pr", "st", "cm", "lg", "fx" ]
assetTypeDirs = [ "00_characters", "01_props", "02_sets", "03_cameras" ]    # WARNING: Missing 99 library
# Library elements follow the criteria above, prefixed with "lb"
assetTypeAbbrLibrary = [ "lb" + x for x in assetTypeAbbr ]
#assetTypeDirsLibrary = [ x[0:3] + "lb" + x[3:] for x in assetTypeDirs ]
assetTypeDirsLibrary = [ "00_lbcharacters", "01_lbprops", "02_lbsets", "03_lbcameras", "04_lblights", "05_lbfx" ]

# Pipeline stages or departments
dptDirs = [ "00_modeling", "01_rigging", "02_cloth", "03_hair", "04_shading", "05_lighting", "06_fx" ]
dptTasks = [ ["modlp", "modhp", "modsc", "modbs"], ["anim", "layout", "rig"], ["cloth"], ["hair"], ["shd"], ["lkdv", "lgt"], ["fx"] ]

imgPlanePos = [ "imgPlaneFr", "imgPlaneBk", "imgPlaneLf", "imgPlaneRg", "imgPlaneTp", "imgPlaneBt" ]

taskRenamingSuggestions = {
   "light": "lgt",
   "lighting": "lgt",
   "lights": "lgt",
   "lookdev": "lkdv",
   "mod": "modhp",
   "mlp": "modlp",
   "mhp": "modhp",
   "msc": "modsc",
   "bls": "modbs"
   }

prodDirs = ["00_layout", "01_animation", "02_cache", "03_fx", "04_lighting", "05_rendering"]
prodTasks = [ ["layout"], ["ablk", "abrd", "aref"], ["cache"], ["fx"], ["light"], ["render"] ]

scene_extensions = ["mb"]

# Files to ignore when analyzing
files_to_ignore = ["desktop.ini"]
directories_to_ignore = [".mayaSwatches"]


###############################################################################
#
#    Check whether this path is a valid project according to our pipeline
#
###############################################################################
def isThisPathAProject(path, proj_dir):
    if not os.path.isfile( path + "/" + proj_dir + "/02_prod/workspace.mel" ):
        return False
    if len(proj_dir) > 5:
        print(path, proj_dir, " too long")
        return False
    if not proj_dir.isupper():
        print(path, proj_dir, " not capitalized")
        return False
    return True


###############################################################################
#
#    Return a list of all projects in the path
#
#    The returned list contains 2-element lists with the ID and the path for each project
#    The list is sorted by project ID
#
###############################################################################
def getProjectsInPath(path):
    print("Searching projects in " + path)
    projects = []
    for root, dirs, files in os.walk( path ):
        for dir in dirs:
            if isThisPathAProject(root, dir) :
                projects.append( [dir, root + "/" + dir] )
    projects.sort()
    return projects


###############################################################################
#
#    Class Asset
#
###############################################################################
class Asset:

    # Constructor
    def __init__(self, project, assetType, assetID, inLibrary=False):
        self.project = project
        self.assetType = assetType
        self.assetID = assetID
        self.inLibrary = inLibrary

    def getID(self):
        return self.assetID
        
    def getType(self):
        return self.assetType

    # Get asset directory
    def getDirectory(self):
        return self.project.projID + "_" + assetTypeAbbr[self.assetType] + "_" + self.assetID

    # Print asset information
    def printInfo(self):
        print(self.getDirectory())

    # Get absolute path for all published versions
    def getPublishedVersionsPaths(self, dptType, dptTask):
        #print("getPublishedVersionsPaths", dptType, dptTask, dptDirs[dptType], dptTasks[dptType][dptTask])
        #pattern = self.project.projPath + "/maya_" + self.project.projID + "/assets/" + assetTypeDirs[self.assetType] + "/" + self.project.projID + "_" + assetTypeAbbr[self.assetType] + "_" + self.assetID + "/" + dptDirs[dptType] + "/" + self.project.projID + "_" + assetTypeAbbr[self.assetType] + "_" + dptTasks[dptType] + "_" + self.assetID + "_v??.mb"
        if self.inLibrary:
            pattern = self.project.projPath + "/02_prod/assets/99_library/" + self.project.projID + "_" + assetTypeAbbr[self.assetType] + "_" + self.assetID + "/" + dptDirs[dptType] + "/" + self.project.projID + "_" + assetTypeAbbr[self.assetType] + "_" + dptTasks[dptType][dptTask] + "_" + self.assetID + "_v??.mb"
        else:
            pattern = self.project.projPath + "/02_prod/assets/" + assetTypeDirs[self.assetType] + "/" + self.project.projID + "_" + assetTypeAbbr[self.assetType] + "_" + self.assetID + "/" + dptDirs[dptType] + "/" + self.project.projID + "_" + assetTypeAbbr[self.assetType] + "_" + dptTasks[dptType][dptTask] + "_" + self.assetID + "_v??.mb"
        files = glob.glob(pattern)
        return files

    # Get absolute path for last published version
    def getLastPublishedVersionPath(self, dptType, dptTask):
        files = self.getPublishedVersionsPaths(dptType,dptTask)
        if files:
            # TO-DO: sort alphabetically?
            return files[-1]    # last element
        return None

    # Get absolute path for all working versions
    def getWorkingVersionsPaths(self, dptType, dptTask):
        if self.inLibrary:
            pattern = self.project.projPath + "/02_prod/assets/99_library/" + self.project.projID + "_" + assetTypeAbbr[self.assetType] + "_" + self.assetID + "/" + dptDirs[dptType] + "/00_working/" + self.project.projID + "_" + assetTypeAbbr[self.assetType] + "_" + dptTasks[dptType][dptTask] + "_" + self.assetID + "_v??_???*.mb"
        else:
            pattern = self.project.projPath + "/02_prod/assets/" + assetTypeDirs[self.assetType] + "/" + self.project.projID + "_" + assetTypeAbbr[self.assetType] + "_" + self.assetID + "/" + dptDirs[dptType] + "/00_working/" + self.project.projID + "_" + assetTypeAbbr[self.assetType] + "_" + dptTasks[dptType][dptTask] + "_" + self.assetID + "_v??_???*.mb"
        files = glob.glob(pattern)
        return files

    # Get absolute path for last working version
    def getLastWorkingVersionPath(self, dptType, dptTask):
        files = self.getWorkingVersionsPaths(dptType,dptTask)
        if files:
            # TO-DO: sort alphabetically?
            return files[-1]    # last element
        return None


############################################################
#
#    Class MayaProject
#
############################################################
class MayaProject:

    # Constructor
    def __init__(self, projID, path, author):
        self.projPath = path
        self.author = author
        self.projID = projID

    # Print project information
    def printInfo(self):
        print("Project " + self.projID + " author: " + self.author + " path: " + self.projPath)

    def getID(self):
        return self.projID
        
    def getAuthor(self):
        return self.author
        
    def getPath(self):
        return self.projPath

    # Check asset *****************************FIXME!
    def checkAsset(self, assetType, assetID):
        print("Asset type: " + str(assetType) + " ID: " + assetID)
        # Check for pipeline stages (departments)
        for d in range(0, len(dptDirs)):
            for t in range(0, len(dptTasks)):
                pattern = self.projPath + "/02_prod/assets/" + assetTypeDirs[assetType] + "/" + self.projID + "_" + assetTypeAbbr[assetType] + "_" + assetID + "/" + dptDirs[d] + "/" + self.projID + "_" + assetTypeAbbr[assetType] + "_" + dptTasks[d][t] + "_" + assetID + "_v??.mb"
                dirs = glob.glob(pattern)
                if dirs :
                    print("Department process: ", dirs)

    # Get the assets list for the project
    def getAssets(self, assetTypeDir=-1, include_library_assets=False):
        assets_list = []
        if assetTypeDir < 0:
            for t in range(0, len(assetTypeDirs)):
                pattern = self.projPath + "/02_prod/assets/" + assetTypeDirs[t] + "/" + self.projID + "_" + assetTypeAbbr[t] + "_*"
                assets = glob.glob(pattern)
                for asset in assets:
                    basename = os.path.basename(asset)
                    fields = basename.split('_')
                    if len(fields) == 3:
                        assetID = fields[2]
                        assets_list.append( Asset(self, t, assetID) )
                    else:
                        print("WARNING - Illegal asset directory name: " + basename)
                if include_library_assets:
                    pattern = self.projPath + "/02_prod/assets/99_library/" + self.projID + "_" + assetTypeAbbr[t] + "_*"
                    library_assets = glob.glob(pattern)
                    for asset in library_assets:
                        basename = os.path.basename(asset)
                        fields = basename.split('_')
                        if len(fields) == 3:
                            assetID = fields[2]
                            assets_list.append( Asset(self, t, assetID, True) )
                        else:
                            print("WARNING - Illegal asset directory name: " + basename)
        else:
            pattern = self.projPath + "/02_prod/assets/" + assetTypeDirs[assetTypeDir] + "/" + self.projID + "_" + assetTypeAbbr[assetTypeDir] + "_*"
            assets = glob.glob(pattern)
            for asset in assets:
                basename = os.path.basename(asset)
                fields = basename.split('_')
                if len(fields) == 3:
                    assetID = fields[2]
                    assets_list.append( Asset(self, assetTypeDir, assetID) )
                else:
                    print("WARNING - Illegal asset directory name: " + basename)
            if include_library_assets:
                pattern = self.projPath + "/02_prod/assets/99_library/" + self.projID + "_" + assetTypeAbbr[assetTypeDir] + "_*"
                library_assets = glob.glob(pattern)
                for asset in library_assets:
                    basename = os.path.basename(asset)
                    fields = basename.split('_')
                    if len(fields) == 3:
                        assetID = fields[2]
                        assets_list.append( Asset(self, t, assetID, True) )
                    else:
                        print("WARNING - Illegal asset directory name: " + basename)
        return assets_list


###############################################################################
#
#   Set the project for the scene path supplied
#   It is searched from 02_prod directory
#
###############################################################################
def getProjectForScene(scene_path):
    proj_dir = "02_prod"
    proj_dir_idx = scene_path.find(proj_dir)
    if proj_dir_idx < 0:
        return None
    else:
        proj_path = scene_path[0:proj_dir_idx]
        if os.path.isfile(proj_path + "/" + proj_dir + "/workspace.mel"):
            return proj_path
        else:
            return None


###############################################################################
#
#   Create a directory structure template in disk to illustrate pipeline 
#   naming convention
#
#   The directory structure is created in current directory with the pro_ID
#   supplied as an argument. The project top-level directory must not exist
#   or the function will end with an error message and create nothing
#
###############################################################################
def createDirectoryTemplate(proj_ID="TPL"):

    # Project top level directory
    try:
        os.mkdir(proj_ID)
    except FileExistsError:
        print("ERROR. The directory %s has already been created"%proj_ID)
        return None

    os.chdir(proj_ID)

    for k in topDirs:
        os.mkdir(topDirs[k])

    # Maya project (pre & prod)
    os.chdir(topDirs["pre&prod"])
    open("workspace.mel", 'a').close()
    os.mkdir("assets")
    os.mkdir("scenes")
    os.mkdir("sourceimages")
    os.mkdir("ies") # Photometric lights
    os.mkdir("shaders")
    os.mkdir("shaders/osl")

    # ASSETS
    os.chdir("assets")
    for i in range(len(assetTypeDirs)):
        os.mkdir(assetTypeDirs[i])
        os.chdir(assetTypeDirs[i])
        asset_dir = proj_ID+"_"+assetTypeAbbr[i]+"_assetID"
        os.mkdir(asset_dir)
        os.chdir(asset_dir)
        for d in range(len(dptDirs)):
            os.mkdir(dptDirs[d])
            os.chdir(dptDirs[d])
            os.mkdir("00_working")
            # Create a template (empty) file for each task (published and working)
            for task in dptTasks[d]:
                open(proj_ID+"_"+assetTypeAbbr[i]+"_"+task+"_assetID_v01.mb", 'a').close()
                open("00_working/"+proj_ID+"_"+assetTypeAbbr[i]+"_"+task+"_assetID_v01_001.mb", 'a').close()
            os.chdir("..")  # dptDir
        os.chdir("..")  # assetDir
        os.chdir("..")  # assetTypeDir

    # Library
    os.mkdir("99_library")
    os.chdir("99_library")
    for i in range(len(assetTypeDirsLibrary)):
        os.mkdir(assetTypeDirsLibrary[i])
        os.chdir(assetTypeDirsLibrary[i])
        asset_dir = proj_ID+"_"+assetTypeAbbrLibrary[i]+"_assetID"
        os.mkdir(asset_dir)
        os.chdir(asset_dir)
        for d in range(len(dptDirs)):
            os.mkdir(dptDirs[d])
            os.chdir(dptDirs[d])
            os.mkdir("00_working")
            # Create a template (empty) file for each task (published and working)
            for task in dptTasks[d]:
                open(proj_ID+"_"+assetTypeAbbrLibrary[i]+"_"+task+"_assetID_v01.mb", 'a').close()
                open("00_working/"+proj_ID+"_"+assetTypeAbbrLibrary[i]+"_"+task+"_assetID_v01_001.mb", 'a').close()
            os.chdir("..")  # dptDir
        os.chdir("..")  # assetDir
        os.chdir("..")  # assetTypeDir
    os.chdir("..")  # 99_library
    os.chdir("..")  # assets

    # SCENES
    os.chdir("scenes")
    seq_dir = "sq01"
    os.mkdir(seq_dir)
    os.chdir(seq_dir)
    shot_dir = "sh001"
    os.mkdir(shot_dir)
    os.chdir(shot_dir)
    for pd in range(len(prodDirs)):
        os.mkdir(prodDirs[pd])
        os.chdir(prodDirs[pd])
        os.mkdir("00_working")
        for t in prodTasks[pd]:
            open(proj_ID+"_"+t+"_"+seq_dir+"_"+shot_dir+"_tk01.mb", 'a').close()
            open("00_working/"+proj_ID+"_"+t+"_"+seq_dir+"_"+shot_dir+"_tk01_001.mb", 'a').close()
        os.chdir("..")  # prodDir
    os.chdir("..")  # shot_dir
    os.chdir("..")  # seq_dir
    os.chdir("..")  # scenes

    # SOURCEIMAGES
    os.chdir("sourceimages")
    for i in range(len(assetTypeDirs)):
        os.mkdir(assetTypeDirs[i])
        os.chdir(assetTypeDirs[i])
        asset_dir = proj_ID+"_"+assetTypeAbbr[i]+"_assetID"
        os.mkdir(asset_dir)
        os.chdir(asset_dir)

        # Concept art
        os.mkdir("00_conceptArt")
        os.chdir("00_conceptArt")
        # Model sheet
        open(proj_ID+"_"+assetTypeAbbr[i]+"_assetID_modelSheet_v01.pdf", 'a').close()
        for p in imgPlanePos:
            open(proj_ID+"_"+assetTypeAbbr[i]+"_assetID_" + p + "_v01.png", 'a').close()
        os.chdir("..")  # 00_conceptArt

        # Textures
        os.mkdir("01_textures")
        os.chdir("01_textures")
        # ...
        os.chdir("..")  # 01_textures
        os.chdir("..")  # asset_dir
        os.chdir("..")  # assetTypeDir

    # Library
    os.mkdir("99_library")
    os.chdir("99_library")
    for i in range(len(assetTypeDirsLibrary)):
        os.mkdir(assetTypeDirsLibrary[i])
        os.chdir(assetTypeDirsLibrary[i])
        asset_dir = proj_ID+"_"+assetTypeAbbrLibrary[i]+"_assetID"
        os.mkdir(asset_dir)
        os.chdir(asset_dir)

        # Concept art
        os.mkdir("00_conceptArt")
        os.chdir("00_conceptArt")
        # Model sheet
        open(proj_ID+"_"+assetTypeAbbrLibrary[i]+"_assetID_modelSheet_v01.pdf", 'a').close()
        for p in imgPlanePos:
            open(proj_ID+"_"+assetTypeAbbrLibrary[i]+"_assetID_" + p + "_v01.png", 'a').close()
        os.chdir("..")  # 00_conceptArt

        # Textures
        os.mkdir("01_textures")
        os.chdir("01_textures")
        # ...
        os.chdir("..")  # 01_textures

        os.chdir("..")  # assetTypeDir
        os.chdir("..")  # assetTypeDir
    os.chdir("..")  # 99_library

    os.chdir("..")  # sourceimages


if __name__ == "__main__":

    #createDirectoryTemplate()
    pass
