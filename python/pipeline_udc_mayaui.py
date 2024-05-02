import maya.cmds as cmd
import cdavtools
import os

# Global stuff

#scene_checker = "C:/Users/jtaibo/Documents/maya/2020/scripts/cdavtools/python/scenecheck.bat"  # TO-DO: configuration!
scene_checker = os.path.dirname(__file__) + "/scenecheck.bat"
cfg_tmp_dir = "X:/ENTREGAS/Mod1"


# UI elements
scene_list = ""
fullpath_scene_list = []
console_window = ""
project_sel = ""
assetType_sel = ""
asset_sel = ""
dpt_sel = ""
task_sel = ""
published_checkbox = ""
working_checkbox = ""
last_checkbox = ""
library_checkbox = ""
everything_checkbox = ""
console_window = ""
path_mode = ""

# Project info
projects = []


###############################################################################
#
#    Create dialog window
#
###############################################################################
def createInfoWindow(published_versions=[]):
   
    global scene_list
    global fullpath_scene_list
    global project_sel
    global assetType_sel
    global asset_sel
    global dpt_sel
    global task_sel
    global published_checkbox
    global working_checkbox
    global last_checkbox
    global library_checkbox
    global everything_checkbox
    global console_window
    global path_mode

    windowTitle = "CDAV-UDC Pipeline Management System"

    windowID = "infoWindowPipelineMgr"
    if cmd.window( windowID, exists=True):
        cmd.deleteUI(windowID)

    cmd.window(windowID, title=windowTitle, sizeable=True, resizeToFitChildren=True, width=400, height=150 )
    cmd.columnLayout(adjustableColumn=True)

    redColor = [1., 0., 0.]
    greenColor = [0., 1., 0.]
    orangeColor = [1., .5, 0.]

    # Button callbacks
    
    def cancelCallback( *pArgs ):
        if cmd.window( windowID, exists=True ):
            cmd.deleteUI( windowID )

    def openCallback( *pArgs ):        
        # Open selected scene
        #selected = cmd.textScrollList( scene_list, query=True, selectItem=True )
        selected_idx = cmd.textScrollList( scene_list, query=True, selectIndexedItem=True )
        if selected_idx:
            scene_path = fullpath_scene_list[selected_idx[0]-1] # warning: 0-based vs 1-based indices

        # WARNING!!! Set project has previously done IF AND ONLY IF a project is selected in the Projects selector
        # If no project selected, we do the "set project" here, searching a 02_prod directory with a workspace.mel inside
        proj_path = cdavtools.python.pipeline_udc.getProjectForScene(scene_path)
        if proj_path:
            cmd.workspace(proj_path + "/02_prod", openWorkspace=True)
        else:
            cmd.error("NO project found in the path of these scene! (complying with our pipeline")

        # Open scene
        cmd.file(scene_path, o=True, force=True)

    def searchProjectsCallback( *pArgs ):
        readProjectsFromDir()

    def openFolderCallback( *pArgs ):
        selected_idx = cmd.textScrollList( scene_list, query=True, selectIndexedItem=True )
        if selected_idx:
            selected = fullpath_scene_list[selected_idx[0]-1] # warning: 0-based vs 1-based indices
            os.startfile( os.path.dirname(selected) )

    def presentCallback( *pArgs ):
        return # This button is disabled
        cmd.file(newFile=True, force=True)
        cdavtools.python.presenter.present(fullpath_scene_list)

    def statsAllCallback( *pArgs ):
        return # This button is disabled
        # Scene paths are set in a file to avoid huge command lines
        list_file = cfg_tmp_dir + "/files_list.txt"
        cmd_line = scene_checker + " -o " + cfg_tmp_dir + " -f " + list_file
        if fullpath_scene_list:
            with open(list_file, 'w') as filehandle:
                for s in fullpath_scene_list:
                    filehandle.write("%s\n" % s)
                filehandle.close()
                os.system(cmd_line)
                os.startfile(cfg_tmp_dir + "/report_ab.csv")
                os.startfile(cfg_tmp_dir + "/report.csv")

    def statsSelectedCallback( *pArgs ):
        return # This button is disabled
        cmd_line = scene_checker + " -o " + cfg_tmp_dir + " -i"
        selected_idx = cmd.textScrollList( scene_list, query=True, selectIndexedItem=True )
        if selected_idx:
            selected = fullpath_scene_list[selected_idx[0]-1] # warning: 0-based vs 1-based indices
        if selected:
            cmd_line += " \"" + selected[0] + "\""
            #print("cmd_line = ", cmd_line)
            os.system(cmd_line)
            os.startfile(cfg_tmp_dir + "/report_ab.csv")
            os.startfile(cfg_tmp_dir + "/report.csv")

    def selectProjectCallback( *pArgs ):
        updateAssetsList()
        updateScenesList()

    def selectAssetTypeCallback( *pArgs ):
        updateAssetsList()
        updateScenesList()

    def selectAssetCallback( *pArgs ):
        updateScenesList()

    def selectDepartmentCallback( *pArgs ):
        populateTasks()
        updateScenesList()

    def selectTaskCallback( *pArgs ):
        updateScenesList()

    def publishedCheckCallback( *pArgs ):
        updateScenesList()

    def workingCheckCallback( *pArgs ):
        updateScenesList()

    def lastCheckCallback( *pArgs ):
        updateScenesList()

    def libraryCheckCallback( *pArgs ):
        updateScenesList()

    def everythingCheckCallback( *pArgs ):
        updateScenesList()

    def selectPathModeCallback( *pArgs ):
        updateScenesList()

    project_sel = cmd.optionMenu( label = "Projects", changeCommand=selectProjectCallback )
    assetType_sel = cmd.optionMenu( label = "Asset types", changeCommand=selectAssetTypeCallback )
    populateAssetTypes()
    asset_sel = cmd.optionMenu( label = "Assets", changeCommand=selectAssetCallback )
    dpt_sel = cmd.optionMenu( label = "Department", changeCommand=selectDepartmentCallback )
    populateDepartments()
    task_sel = cmd.optionMenu( label = "Task", changeCommand=selectTaskCallback )
    populateTasks()
    path_mode = cmd.optionMenu( label = "Path mode", changeCommand=selectPathModeCallback)
    populatePathModes()

    cmd.rowColumnLayout(numberOfColumns=5)
    published_checkbox = cmd.checkBox(label="Published", changeCommand=publishedCheckCallback, value=True)
    working_checkbox = cmd.checkBox(label="Working", changeCommand=workingCheckCallback, value=True)
    last_checkbox = cmd.checkBox(label="Last version only", changeCommand=lastCheckCallback, value=True)
    library_checkbox = cmd.checkBox(label="Library elements", changeCommand=libraryCheckCallback, value=False)
    everything_checkbox = cmd.checkBox(label="All scenes", changeCommand=everythingCheckCallback, value=False)
    cmd.setParent("..")

    cmd.text( label="Scene list:")
    scene_list = cmd.textScrollList( append=published_versions, doubleClickCommand=openCallback )
    cmd.separator( h=10, style="none" )

    #cmd.rowColumnLayout(numberOfColumns=3, columnWidth=[ (1,120), (2, 120), (3, 120) ], columnOffset=[ (1, "right", 2), (2, "right", 3) ] )
    cmd.rowColumnLayout(numberOfColumns=6)
    button_width = 100
    cmd.button( label = "Search directory", command=searchProjectsCallback, width=button_width )
    cmd.button( label = "Present all", command=presentCallback, width=button_width )
    cmd.button( label = "Stats all", command=statsAllCallback, width=button_width )
    cmd.button( label = "Stats selected", command=statsSelectedCallback, width=button_width )
    cmd.button( label = "Open folder", command=openFolderCallback, width=button_width )
    cmd.button( label="Cancel", command=cancelCallback, width=button_width )
    cmd.setParent("..")
    
    console_window = cmd.textField(editable=False)
    
    cmd.showWindow()


###############################################################################
#
#
#
###############################################################################
def populateAssetTypes():
    # Populate menuItems in optionMenus
    items = cmd.optionMenu(assetType_sel, query=True, itemListLong=True)
    if items:
        cmd.deleteUI(items, menuItem=True)
    cmd.menuItem( "* - All", parent = assetType_sel )
    for i in range(len(cdavtools.python.pipeline_udc.assetTypeDirs)):
        at_dir = cdavtools.python.pipeline_udc.assetTypeDirs[i]
        at_abbr = cdavtools.python.pipeline_udc.assetTypeAbbr[i]
        cmd.menuItem( at_abbr + " - " + at_dir, parent = assetType_sel )

###############################################################################
#
#
#
###############################################################################
def populateDepartments():
    # Populate menuItems in optionMenus
    items = cmd.optionMenu(dpt_sel, query=True, itemListLong=True)
    if items:
        cmd.deleteUI(items, menuItem=True)
    cmd.menuItem( "* - All", parent = dpt_sel )
    for dpt in cdavtools.python.pipeline_udc.dptDirs:
        cmd.menuItem( dpt, parent = dpt_sel )

###############################################################################
#
#
#
###############################################################################
def populateTasks():
    tasks = []
    dpt_select_idx = cmd.optionMenu(dpt_sel, query=True, select=True)
    if dpt_select_idx == 1:
        # UPDATE: When "all departments" are selected, no task filter is enable ("all tasks" is the only choice)
        pass
        #for d in range(len(cdavtools.python.pipeline_udc.dptDirs)):
        #    for t in cdavtools.python.pipeline_udc.dptTasks[d]:
        #        tasks.append(t)
    else:
        d = dpt_select_idx-2
        for t in cdavtools.python.pipeline_udc.dptTasks[d]:
            tasks.append(t)
    # Populate menuItems in optionMenus
    items = cmd.optionMenu(task_sel, query=True, itemListLong=True)
    if items:
        cmd.deleteUI(items, menuItem=True)
    cmd.menuItem( "* - All", parent = task_sel )
    for task in tasks:
        cmd.menuItem( task, parent = task_sel )

###############################################################################
#
#
#
###############################################################################
def populatePathModes():
    items = cmd.optionMenu(path_mode, query=True, itemListLong=True)
    if items:
        cmd.deleteUI(items, menuItem=True)
    cmd.menuItem( "Full path", parent = path_mode)
    cmd.menuItem( "In-project path", parent = path_mode)
    cmd.menuItem( "File name", parent = path_mode)


###############################################################################
#
#
#
###############################################################################
def printConsoleMessage(msg):
    global console_window
    cmd.textField(console_window, edit=True, text=msg)

###############################################################################
#
#
#
###############################################################################
def readProjectsFromDir(projects_dir=""):
    global projects
    printConsoleMessage("Searching projects...")
    if projects_dir == "":
        dialog_sel = cmd.fileDialog2( caption="Seleccione directorio con los proyectos", fileMode=2)
        projects_dir = dialog_sel[0]
    projects = cdavtools.python.pipeline_udc.getProjectsInPath(projects_dir)
    printConsoleMessage(str(len(projects)) + " project(s) found!")
    
    # Projects list (drop-down selection)
    updateProjectsList()    

###############################################################################
#
#
#
###############################################################################
def updateProjectsList():
    # Populate menuItems in optionMenus
    items = cmd.optionMenu(project_sel, query=True, itemListLong=True)
    if items:
        cmd.deleteUI(items, menuItem=True)
    cmd.menuItem( "* - All", parent = project_sel )
    for p in projects:
        cmd.menuItem( p[0] + " - " + p[1], parent = project_sel )

    # Assets list (drop-down selection)
    updateAssetsList()
    
    # Update scenes list
    updateScenesList()
        
###############################################################################
#
#
#
###############################################################################
def updateAssetsList():
    global asset_sel
    assets = []
    select_idx = cmd.optionMenu(project_sel, query=True, select=True)
    if select_idx == 1:
        # All projects selected
        for p in projects:
            proj_id = p[select_idx-2][0]
            proj_path = p[select_idx-2][1]
            proj = cdavtools.python.pipeline_udc.MayaProject(proj_id, proj_path, proj_id) 
            addProjAssets(proj, assets)
    else:
        proj_id = projects[select_idx-2][0]
        proj_path = projects[select_idx-2][1]
        proj = cdavtools.python.pipeline_udc.MayaProject(proj_id, proj_path, proj_id) 
        addProjAssets(proj, assets)
        # If only one project is selected, we do the "set project" for this project
        printConsoleMessage( "Setting project " + proj_id + " - " + str(len(assets)) + " asset(s) found!")
        print( "Setting project " + proj_id + " - " + str(len(assets)) + " asset(s) found! - projpath=" + proj_path)
        cmd.workspace(proj_path + "/02_prod", openWorkspace=True)

    # Populate menuItems in optionMenus
    items = cmd.optionMenu(asset_sel, query=True, itemListLong=True)
    if items:
        cmd.deleteUI(items, menuItem=True)
    cmd.menuItem( "* - All", parent = asset_sel )
    for a in assets:
        cmd.menuItem( a.getDirectory(), parent = asset_sel )
    

###############################################################################
#
#    Add assets from project "proj" to "assets" array
#
###############################################################################
def addProjAssets(proj, assets):
    selected_assetType_idx = cmd.optionMenu(assetType_sel, query=True, select=True)
    include_library_assets = cmd.checkBox(library_checkbox, query=True, value=True)
    ass = proj.getAssets(selected_assetType_idx-2, include_library_assets)
    for a in ass:
        assets.append( a )


###############################################################################
#
#
#
###############################################################################
def updateScenesList():
    cmd.textScrollList( scene_list, edit=True, removeAll=True)
    scenes = []
    global fullpath_scene_list
    fullpath_scene_list = []
    
    selected_project_idx = cmd.optionMenu(project_sel, query=True, select=True)
    everything = cmd.checkBox(everything_checkbox, query=True, value=True)
    every_scene_extensions = ["mb", "ma", "obj"]

    if selected_project_idx == 0:
        # No projects, no scene list
        return
    if selected_project_idx == 1:
        # Include all projects
        for p in projects:
            if everything:
                fullpath_scene_list += cdavtools.python.miscutils.selectScenesInDirectory( p[1], every_scene_extensions )
            else:
                addScenesForProject(p, fullpath_scene_list)
    else:
        p = projects[selected_project_idx-2]
        if everything:
            fullpath_scene_list += cdavtools.python.miscutils.selectScenesInDirectory( p[1], every_scene_extensions )
        else:
            addScenesForProject(p, fullpath_scene_list)

    # Filter scene names
    path_mode_idx = cmd.optionMenu(path_mode, query=True, select=True)
    if path_mode_idx == 1:  # Full path
        scenes = fullpath_scene_list
        pass
    elif path_mode_idx == 2: # In-project path
        for s in fullpath_scene_list:
            proj_path = cdavtools.python.pipeline_udc.getProjectForScene(s)
            if(proj_path):
                maya_proj_path = proj_path + "/02_prod"
                scenes.append( os.path.relpath(s, maya_proj_path) )
    elif path_mode_idx == 3: # File name
        for s in fullpath_scene_list:
            scenes.append( os.path.basename(s) )
    
    selected_idx = cmd.textScrollList( scene_list, edit=True, append=scenes )


###############################################################################
#
#   Add scenes for project and selected filters to "sc" list
#
###############################################################################
def addScenesForProject(p, sc):
    proj_id = p[0]
    proj_path = p[1]
    proj_author = proj_id
    proj = cdavtools.python.pipeline_udc.MayaProject(proj_id, proj_path, proj_author)
    
    selected_asset = cmd.optionMenu(asset_sel, query=True, select=True)
    selected_assetType_idx = cmd.optionMenu(assetType_sel, query=True, select=True)   
    include_library_assets = cmd.checkBox(library_checkbox, query=True, value=True)
    assets = proj.getAssets(selected_assetType_idx-2, include_library_assets)

    for a in assets:

        # If not all assets selected, filter the selected asset
        if selected_asset != 1 and a.getID() != assets[selected_asset-2].getID():
            continue

        #a.printInfo()
        selected_dpt_idx = cmd.optionMenu(dpt_sel, query=True, select=True)
        selected_task_idx = cmd.optionMenu(task_sel, query=True, select=True)

        dpt_idxs = []
        if selected_dpt_idx == 1:
            # All departments
            for dpt in range(0,len(cdavtools.python.pipeline_udc.dptDirs)):
                dpt_idxs.append(dpt)
        else:
            dpt_idxs.append(selected_dpt_idx-2)

        for dpt in dpt_idxs:
            if selected_task_idx == 1:
                for task in range(0,len(cdavtools.python.pipeline_udc.dptTasks[dpt])):
                    addScenesForAsset(a, dpt, task, sc)
            else:
                task = selected_task_idx-2
                addScenesForAsset(a, dpt, task, sc)

    printConsoleMessage( str(len(sc)) + " asset(s) found for current search criteria")

###############################################################################
#
#   Add scenes for asset and selected filters to "sc" list
#
###############################################################################
def addScenesForAsset(asset, dpt, task, sc):
    pub_cb = cmd.checkBox(published_checkbox, q=True, value=True)
    work_cb = cmd.checkBox(working_checkbox, q=True, value=True)
    last_cb = cmd.checkBox(last_checkbox, q=True, value=True)

    if pub_cb:
        published_assets = asset.getPublishedVersionsPaths(dpt, task)
        if published_assets:
            if last_cb:
                sc.append( published_assets[-1] )
            else:
                for p in published_assets:
                    sc.append(p)

    if work_cb:
        working_assets = asset.getWorkingVersionsPaths(dpt, task)
        if working_assets:
            if last_cb:
                sc.append( working_assets[-1] )
            else:
                for p in working_assets:
                    sc.append(p)

###############################################################################

################################################################################
#
#   Entry point (called from shelf button)
#
###############################################################################
def pipelineManager():
    createInfoWindow()


###############################################################################

###############################################################################
#
#   Create a directory structure template in disk to illustrate pipeline 
#   naming convention (called from shelf button)
#
###############################################################################
def createDirectoryTemplateUI():
    proj_id = "TPL"
    dialog_sel = cmd.fileDialog2( caption="Seleccione directorio donde crear la plantilla del pipeline", fileMode=2)
    target_dir = dialog_sel[0]
    os.chdir(target_dir)
    cdavtools.python.pipeline_udc.createDirectoryTemplate(proj_id)


if __name__ == "__main__":

    createInfoWindow()
