@REM CALL I:\core\Acacia\hosts\LMNpype\batch\Main.bat

set ACACIA=C:\workspace\learning\batch-file\ProjectA\Blender
set PATH=C:\Program Files\Blender Foundation\Blender 4.5
set OCIO=K:\AcaciaTools\OCIOv2\studio-config-v1.0.0_aces-v1.3_ocio-v2.0.ocio
set PYTHONPATH=C:\workspace\learning\batch-file;C:\Python-interpreter\Python311\Lib\site-packages;I:\core

@REM set BLENDER_USER_SCRIPTS=C:\workspace\learning\batch-file\Blender-ABC
set BLENDER_CUSTOM_SPLASH=%ACACIA%\images\Sample_Splashscreens.png
set BLENDER_SYSTEM_SCRIPTS=C:\workspace\learning\batch-file\ProjectA\Blender
set blender_project_config=C:\workspace\learning\batch-file\ProjectA\Blender\scripts\project-config-setup.py

blender.exe --python-use-system-env --python %blender_project_config%