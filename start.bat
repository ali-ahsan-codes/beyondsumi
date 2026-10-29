@echo off
setlocal
cd /d "%~dp0"

if not exist "%~dp0install.py" goto missing_project
if not exist "%~dp0studio\index.html" goto missing_project

where py >nul 2>nul
if errorlevel 1 goto check_python
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>nul
if errorlevel 1 goto check_python

echo Starting ALI Animation Studio locally. No AI, cloud, or package install is used.
py -3 install.py
set "EXIT_CODE=%ERRORLEVEL%"
goto finish

:check_python
where python >nul 2>nul
if errorlevel 1 goto no_python
python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>nul
if errorlevel 1 goto no_python

echo Starting ALI Animation Studio locally. No AI, cloud, or package install is used.
python install.py
set "EXIT_CODE=%ERRORLEVEL%"
goto finish

:missing_project
echo Could not find install.py and studio\index.html next to this launcher.
echo Keep start.bat inside the extracted ALI Animation project folder.
set "EXIT_CODE=1"
goto error

:no_python
echo Python 3.8 or newer was not found.
echo Install Python 3.8+ once, then double-click start.bat again.
set "EXIT_CODE=1"
goto error

:error
pause
exit /b %EXIT_CODE%

:finish
if not "%EXIT_CODE%"=="0" pause
exit /b %EXIT_CODE%
