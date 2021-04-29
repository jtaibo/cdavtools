@echo off
call env.bat

set INPUT_FRAMES="D:/Google Drive/Almacen/CDAV/Materiales&Iluminacion/maya_projects/MEI/02_prod/images/test_aovs_v02/test_aovs_v02.exr"
set OUTPUT_FRAMES="D:/Google Drive/Almacen/CDAV/Materiales&Iluminacion/maya_projects/MEI/02_prod/images/test_aovs_v02/test_aovs_v02_denoised.exr"

set EXTRA_FRAMES=0
set SEARCH_RADIUS=9
set PATCH_RADIUS=3
set VARIANCE_THRESHOLD=0.5
set EXTRA_AOVS=-l diffuse -l specular

REM %ARNOLD_BIN%\noice -h
%ARNOLD_BIN%\noice -i %INPUT_FRAMES% -o %OUTPUT_FRAMES% -ef %EXTRA_FRAMES% -sr %SEARCH_RADIUS% -pr %PATCH_RADIUS% -v %VARIANCE_THRESHOLD% %EXTRA_AOVS% 

REM Keep the console open after finishing so we can read the output
pause
