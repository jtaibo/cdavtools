REM @echo off

REM Add ffmpeg binaries location to PATH environment variable
set PATH=%PATH%;bin

REM Create a new directory to avoid messing up too much
md frames

set START_TIME=0
set DURATION=100
set WIDTH=320

set INPUT_FILE=Spiderman.mp4
set OUTPUT_NAME=spiderman

ffmpeg -ss %START_TIME% -t %DURATION% -i %INPUT_FILE% -vf scale=%WIDTH%:-1 frames/%OUTPUT_NAME%_%%04d.png

pause
