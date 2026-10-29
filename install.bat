@echo off
setlocal
cd /d "%~dp0"

echo ALI Animation local setup check
echo ==============================

if not exist "%~dp0install.py" goto missing_project
if not exist "%~dp0studio\index.html" goto missing_project

where py >nul 2>nul
if errorlevel 1 goto check_python
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>nul
if errorlevel 1 goto check_python

echo Python 3 is ready. No AI model, cloud account, API key, or Python packages are needed.
echo First-run check passed. Starting the Studio...
call "%~dp0start.bat"
exit /b %ERRORLEVEL%

:check_python
where python >nul 2>nul
if errorlevel 1 goto no_python
python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>nul
if errorlevel 1 goto no_python

echo Python 3 is ready. No AI model, cloud account, API key, or Python packages are needed.
echo First-run check passed. Starting the Studio...
call "%~dp0start.bat"
exit /b %ERRORLEVEL%

:missing_project
echo Could not find install.py and studio\index.html.
echo Extract the entire project and keep this file in its root folder.
goto error

:no_python
echo Python 3.8 or newer was not found.
echo Install Python 3.8+ once, then run install.bat again.
goto error

:error
pause
exit /b 1
