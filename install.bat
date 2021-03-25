@echo off

echo Maya CDAVTools installer
echo =====================
echo(

set SHELVES_DIR=..\..\prefs\shelves

if exist %SHELVES_DIR% (
    echo Copying shelf files
    copy shelf\* %SHELVES_DIR%
) else (
    echo Shelves directory not found!
)

echo(
echo Installation finished!
echo(	

pause
