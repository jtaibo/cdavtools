@echo off
call env.bat

REM set SCENE="scenes/AJX_pr_3Dcembro_aref_anim01_tk04.mb"

REM set LOG=-ai:ltc true -ai:lve 2
REM -ai:lfn %PROJ_DIR%/render.log

REM %MAYA_BIN%\Render.exe -proj %PROJ_DIR% -r arnold %LOG% %SCENE%

REM Execute the line below to get help about Render.exe command-line options
REM %MAYA_BIN%\Render.exe -help
REM Or the one below for Arnold specific options
REM %MAYA_BIN%\Render.exe -help -r arnold

REM These are the most useful options (besides -proj):
REM
REM     -s float                    Starting frame for an animation sequence
REM     -e float                    End frame for an animation sequence                                                     
REM     -cam name                   Specify which camera to be rendered
REM     -rd path                    Directory in which to store image file
REM

REM You can also read all Arnold options in file batch_render_options_arnold.txt

REM To render several scenes one after the other, just create one line for each
REM in this script. When one render finishes, the next one will start.
REM Example below (replace scene path to your real scenes)

%MAYA_BIN%\Render.exe -proj %PROJ_DIR% scenes/first_scene_to_render.mb
%MAYA_BIN%\Render.exe -proj %PROJ_DIR% scenes/second_scene_to_render.mb
%MAYA_BIN%\Render.exe -proj %PROJ_DIR% scenes/third_scene_to_render.mb
%MAYA_BIN%\Render.exe -proj %PROJ_DIR% scenes/fourth_scene_to_render.mb
%MAYA_BIN%\Render.exe -proj %PROJ_DIR% scenes/fifth_scene_to_render.mb

REM Keep the console open after finishing so we can read the output
pause
