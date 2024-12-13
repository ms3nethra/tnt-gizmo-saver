@echo off

REM Set the current script's directory
SET CURRENT_DIR=%~dp0

REM Set the nuke path
SET NUKE_PATH=%CURRENT_DIR%;%NUKE_PATH%

REM Launch Nuke
"C:\Program Files\Nuke15.1v3\Nuke15.1.exe"