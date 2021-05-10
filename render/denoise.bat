@echo off
call env.bat

REM Replace the value of variables declared in the lines below with :
REM
REM     INPUT_FRAMES - Prefix path of renders
REM         e.g.: D:/Google Drive/Almacen/CDAV/Materiales&Iluminacion/maya_projects/MEI/02_prod/images/pruebarapida/pruebarapida.0001.exr
REM
REM     FRAME_START - 4-digit start frame
REM     FRAME_END   - 4-digit end frame
REM
REM NOTE: Padding is assumed to be 4 digits in all renders
REM
REM     EXTRA_FRAMES, SEARCH_RADIUS, PATCH_RADIUS, VARIANCE_THRESHOLD are values set in "Arnold > Utilities > Arnold denoiser (noice)" window in Maya
REM
REM     For more information about these parameters, read the Arnold denoiser documentation in
REM         https://docs.arnoldrenderer.com/pages/viewpage.action?pageId=76316887
REM
REM     EXTRA_AOVS  - additional (to beauty) AOVs to denoise. Each AOV must be preceded by "-l" as in the example below
REM

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
