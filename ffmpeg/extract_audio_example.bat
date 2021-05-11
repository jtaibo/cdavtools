REM @echo off

REM Add ffmpeg binaries location to PATH environment variable
set PATH=%PATH%;bin

set INPUT_FILE=frames\GAI_anmtcTeaser_audio.mp4
set OUTPUT_FILE=frames\GAI_anmtcTeaser_audio.aac

ffmpeg -i %INPUT_FILE% -vn -acodec copy %OUTPUT_FILE%

pause
