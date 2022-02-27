@echo off & CHCP 65001

REM This example mounts OneDrive folder in U: virtual unit to shorten paths and avoid special characters that Arnold does not like
subst U: "D:\OneDrive - Universidade da Coruña"
