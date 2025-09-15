@echo off
REM Reset licensing configuration

C:
cd %CommonProgramFiles(x86)%\Autodesk Shared\AdskLicensing\Current\helper\
AdskLicensingInstHelper.exe change -pk 657Q1 -pv 2025.0.0.F -lm ""
