@echo off
call env.bat

set INPUT_FRAMES="D:/Google Drive/Almacen/CDAV/Materiales&Iluminacion/maya_projects/MEI/02_prod/images/pruebarapida/pruebarapida"
set OUTPUT_FRAMES_SUFFIX="_denoised"
set FRAME_START=0001
set FRAME_END=0010

set EXTRA_FRAMES=0
set SEARCH_RADIUS=9
set PATCH_RADIUS=3
set VARIANCE_THRESHOLD=0.5
set EXTRA_AOVS=-l diffuse -l specular

REM %ARNOLD_BIN%\noice -h
REM %ARNOLD_BIN%\noice -i %INPUT_FRAMES% -o %OUTPUT_FRAMES% -ef %EXTRA_FRAMES% -sr %SEARCH_RADIUS% -pr %PATCH_RADIUS% -v %VARIANCE_THRESHOLD% %EXTRA_AOVS% 

REM I really hate Windows!!!
setlocal enabledelayedexpansion
set /A start=1%FRAME_START%
set /A end=1%FRAME_END%
set step=1
for /L %%i in ( %start%,%step%,%end% ) do (
    set FRAME_NUMBER=%%i
    set FRAME_NUMBER=!FRAME_NUMBER:~1!
    %ARNOLD_BIN%\noice -i %INPUT_FRAMES%.!FRAME_NUMBER!.exr -o %INPUT_FRAMES%.!FRAME_NUMBER!%OUTPUT_FRAMES_SUFFIX%.exr -ef %EXTRA_FRAMES% -sr %SEARCH_RADIUS% -pr %PATCH_RADIUS% -v %VARIANCE_THRESHOLD% %EXTRA_AOVS% 
)

REM Keep the console open after finishing so we can read the output
pause
