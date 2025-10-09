set PROJECT_ROOT=%~dp0

set MAYA_EXE="C:\Program Files\Autodesk\Maya2024\bin\maya.exe"


set MAYA_SCRIPT_PATH=%PROJECT_ROOT%\scripts
set MAYA_PLUG_IN_PATH=%PROJECT_ROOT%\plugins
set PYTHONPATH=%PROJECT_ROOT%\python
set XBMLANGPATH=%PROJECT_ROOT%\icons
set MAYA_SHELF_PATH=%PROJECT_ROOT%\shelves
set OCIO=K:\AcaciaTools\OCIOv2\studio-config-v1.0.0_aces-v1.3_ocio-v2.0.ocio

"maya.exe" %* %MAYA_EXE%