@echo off
call env.bat

set SCENE="scenes/AJX_pr_3Dcembro_aref_anim01_tk04.mb"

REM set LOG=-ai:ltc true -ai:lve 2
REM -ai:lfn %PROJ_DIR%/render.log

%MAYA_BIN%\Render.exe -proj %PROJ_DIR% -r arnold %LOG% %SCENE%

REM Keep the console open after finishing so we can read the output
pause
