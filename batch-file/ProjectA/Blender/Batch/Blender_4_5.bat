@REM CALL I:\core\Acacia\hosts\LMNpype\batch\Main.bat

set WORKSPACE_DIRECTORY=%~dp0..

set PATH=C:\Program Files\Blender Foundation\Blender 4.5
set OCIO=K:\AcaciaTools\OCIOv2\studio-config-v1.0.0_aces-v1.3_ocio-v2.0.ocio
set PYTHONPATH=%PYTHONPATH%;C:\Python-interpreter\Python311\Lib\site-packages;K:\

set BLENDER_CUSTOM_SPLASH=%WORKSPACE_DIRECTORY%\images\Sample_Splashscreens.png
set BLENDER_SYSTEM_SCRIPTS=%WORKSPACE_DIRECTORY%
set blender_project_config=%WORKSPACE_DIRECTORY%\scripts\project-config-setup.py

blender.exe --python-use-system-env --python %blender_project_config%