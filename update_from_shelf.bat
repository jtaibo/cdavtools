@echo off

echo Updating shelf from current Maya config
echo =======================================
echo(

set SHELVES_DIR=..\..\prefs\shelves

if exist %SHELVES_DIR% (
    echo Copying shelf files
    copy %SHELVES_DIR%\shelf_CDAVTools.mel shelf
) else (
    echo Shelves directory not found!
)

echo(
echo Update finished!
echo(	

pause
