@echo off
REM Reset licensing configuration

C:
cd %CommonProgramFiles(x86)%\Autodesk Shared\AdskLicensing\Current\helper\
AdskLicensingInstHelper.exe change -pk 657P1 -pv 2024.0.0.F -lm ""
