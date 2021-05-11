REM @echo off

REM Add ffmpeg binaries location to PATH environment variable
set PATH=%PATH%;bin

REM ffmpeg -help

set INPUT_FRAMES="frames\tiff\GAI_anmtcTeaser_pruebaTiff%%08d.tif"
set INPUT_AUDIO=frames\GAI_anmtcTeaser_audio.aac
set OUTPUT_NAME=output.mp4
set FRAME_RATE=24
set START_FRAME=00086400

REM With audio (extract audio first with extract_audio.bat when necessary)
ffmpeg -framerate %FRAME_RATE% -start_number %START_FRAME% -i %INPUT_FRAMES% -i %INPUT_AUDIO% -c:a copy -c:v libx264 -shortest out_a.mp4

REM Without audio
REM ffmpeg -framerate %FRAME_RATE% -start_number %START_FRAME% -i %INPUT_FRAMES% -c:v libx264 out.mp4

pause
