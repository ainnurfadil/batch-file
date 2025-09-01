
set ACACIA=C:\workspace\learning\batch-file\Blender-ABC

set PATH=%PATH%;C:\Program Files\Blender Foundation\Blender 4.5

@REM set PYTHONPATH=%PYTHONPATH%;C:\Users\mFadil\AppData\Local\Programs\Python\Python311\Lib

@REM set BLENDER_USER_SCRIPTS=C:\workspace\learning\batch-file\Blender-ABC
set BLENDER_CUSTOM_SPLASH=%ACACIA%\images\Sample_Splashscreens.png
set BLENDER_USER_EXTENSIONS=C:\workspace\learning\batch-file\Blender-ABC\addons

blender.exe --python-use-system-env
