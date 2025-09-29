set PROJECT_ROOT=%~dp0

set MAYA_EXE="C:\Program Files\Autodesk\Maya2025\bin\maya.exe"

:: 1. Path for MEL and Python scripts
set MAYA_SCRIPT_PATH=%PROJECT_ROOT%\scripts;%MAYA_SCRIPT_PATH%
echo Scripts Path: %MAYA_SCRIPT_PATH%

:: 2. Path for plug-ins (.mll, .py, etc.)
set MAYA_PLUG_IN_PATH=%PROJECT_ROOT%\plug-ins;%MAYA_PLUG_IN_PATH%
echo Plug-ins Path: %MAYA_PLUG_IN_PATH%

:: 3. Path for Python modules (if you have separate libraries)
set PYTHONPATH=%PROJECT_ROOT%\python;%PYTHONPATH%
echo Python Path: %PYTHONPATH%

:: 4. Path for custom icons (for shelves, etc.)
set XBMLANGPATH=%PROJECT_ROOT%\icons;%XBMLANGPATH%
echo Icons Path: %XBMLANGPATH%

:: 5. Path for custom shelves
set MAYA_SHELF_PATH=%PROJECT_ROOT%\shelves;%MAYA_SHELF_PATH%
echo Shelves Path: %MAYA_SHELF_PATH%

:: 6. Set OCIO environment for color management (optional)
set OCIO=K:\AcaciaTools\OCIOv2\studio-config-v1.0.0_aces-v1.3_ocio-v2.0.ocio
echo OCIO Config: %OCIO%

echo ---------------------------------
echo.


:: --- LAUNCH MAYA ---
echo Launching Maya for My Awesome Project...
start "Maya" %MAYA_EXE%