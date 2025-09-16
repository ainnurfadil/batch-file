import bpy

# Atur Frame Rate (FPS)
bpy.context.scene.render.fps = 20

# Atur Resolusi Render
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

print(f"FPS: {bpy.context.scene.render.fps}")
print(f"Resolution: {bpy.context.scene.render.resolution_x}x{bpy.context.scene.render.resolution_y}")