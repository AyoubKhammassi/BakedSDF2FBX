import sys
import bpy, os

#Clean the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
inputPath = ""
outputPath = ""

if "--input" in argv:
    inputPath = argv[argv.index("--input") + 1]

if "--output" in argv:
    outputPath = argv[argv.index("--output") + 1]

if inputPath and outputPath:
    parent_dir = os.path.dirname(outputPath)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    bpy.ops.import_scene.gltf(filepath=inputPath)
    bpy.ops.export_scene.fbx(filepath=outputPath, check_existing=False, object_types={'MESH'})
else:
    print("You need to specify the GLB path as --input and the FBX desired path as --output!")