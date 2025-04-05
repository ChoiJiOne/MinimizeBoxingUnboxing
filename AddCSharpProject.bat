@echo off

SET SCRIPT_PATH=%~dp0Script\cli.py
SET SCRIPT_COMMAND=add-csharp-project
SET ROOT_PATH=%~dp0
SET SOLUTION_NAME=MinimizeBoxingUnboxing
SET PROJECT_NAME=%1
SET LOG_PATH=%~dp0Log

python %SCRIPT_PATH% %SCRIPT_COMMAND% --root-path %ROOT_PATH% --solution-name %SOLUTION_NAME% --project-name %PROJECT_NAME% --log-path %LOG_PATH%