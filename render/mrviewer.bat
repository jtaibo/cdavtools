@echo off
call env.bat

REM OCIO environment file is not defined in env.bat to let Maya use its own configuration
REM Uncomment the line below to define the OCIO config to be used by mrViewer
REM set OCIO=X:\OCIO\OpenColorIO-Configs\aces_1.1\config.ocio

%MRVIEWER_BIN%\mrviewer

REM Keep the console open after finishing so we can read the output
REM pause
