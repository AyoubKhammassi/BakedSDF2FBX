import trimesh
import struct
import glob
import os
from pathlib import Path
import argparse
    

def PackFloat32(x,y,z,w):
    packed = struct.pack('4B', int(x),int(y),int(z),int(w))  # pack 4 int8 into a binary string
    float_val = struct.unpack('f', packed)[0]
    return float_val

#Packs one int8 in the two exponents of the UV floats
def PackInExponents(x):
    e1 = int((x & 0xF) | 96) 
    e2 = int(((x >> 4) & 0xF) | 96)
    return e1,e2

from ModifiedTrimeshFunctions import _append_multi_uv_mesh
trimesh.exchange.gltf._append_mesh = _append_multi_uv_mesh

def EncodeSHDataInUVs(filePath, convert=True):
    print("Loading GLB file: " + filePath)
    scene = trimesh.load(filePath)
    print("Encoding custom attributes in UVs...")
    todel = []
    for meshName in scene.geometry:
        mesh = scene.geometry[meshName]
        if not '_sg_mean_1' in mesh.vertex_attributes.keys():
            todel.append(meshName)
            continue
        uv0 = []
        for mean, color, scale in zip(mesh.vertex_attributes['_sg_mean_0'], mesh.vertex_attributes['_sg_color_0'], mesh.vertex_attributes['_sg_scale_0']):
            exp = PackInExponents(scale)
            uvx = PackFloat32(mean[0], mean[1], mean[2], exp[0])
            uvy = PackFloat32(color[0], color[1], color[2], exp[1])
            uv0.append([uvx, uvy])
        uv1 = []
        for mean, color, scale in zip(mesh.vertex_attributes['_sg_mean_1'], mesh.vertex_attributes['_sg_color_1'], mesh.vertex_attributes['_sg_scale_1']):
            exp = PackInExponents(scale)
            uvx = PackFloat32(mean[0], mean[1], mean[2], exp[0])
            uvy = PackFloat32(color[0], color[1], color[2], exp[1])
            uv1.append([uvx, uvy])
        uv2 = []
        for mean, color, scale in zip(mesh.vertex_attributes['_sg_mean_2'], mesh.vertex_attributes['_sg_color_2'], mesh.vertex_attributes['_sg_scale_2']):
            exp = PackInExponents(scale)
            uvx = PackFloat32(mean[0], mean[1], mean[2], exp[0])
            uvy = PackFloat32(color[0], color[1], color[2], exp[1])
            uv2.append([uvx, uvy])

        texvisual = trimesh.visual.TextureVisuals(uv=uv0)
        texvisual1 = trimesh.visual.TextureVisuals(uv=uv1)
        texvisual2 = trimesh.visual.TextureVisuals(uv=uv2)
        texvisual.vertex_attributes = {'color': mesh.visual.vertex_colors, 'uv' : texvisual.uv, 'uv1' : texvisual1.uv, 'uv2' : texvisual2.uv}
        mesh.visual = texvisual
        del mesh.vertex_attributes['_sg_mean_0']
        del mesh.vertex_attributes['_sg_scale_0']
        del mesh.vertex_attributes['_sg_color_0']
        del mesh.vertex_attributes['_sg_mean_1']
        del mesh.vertex_attributes['_sg_scale_1']
        del mesh.vertex_attributes['_sg_color_1']    
        del mesh.vertex_attributes['_sg_mean_2']
        del mesh.vertex_attributes['_sg_scale_2']
        del mesh.vertex_attributes['_sg_color_2']

    scene.delete_geometry(todel)
    basedir, filenameNoExtension = os.path.split(Path(filePath).with_suffix(''))
    glbEncodedDir = "{0}/EncodedGLB".format(basedir)
    fbxEncodedDir = "{0}/EncodedFBX".format(basedir)
    glbEncodedPath = "{0}/{1}Encoded.glb".format(glbEncodedDir, filenameNoExtension)
    fbxEncodedPath = "{0}/{1}Encoded.fbx".format(fbxEncodedDir, filenameNoExtension)

    print("Exporting encoded GLB...")
    if(not os.path.exists(glbEncodedDir)):
        os.makedirs(glbEncodedDir)
    scene.export(glbEncodedPath)

    if convert:
        print("Converting to FBX...")
        if(not os.path.exists(fbxEncodedDir)):
            os.makedirs(fbxEncodedDir)
        glb2fbxCommand = "blender.exe --background --python GLB2FBX.py  -- --input {0} --output {1}".format(glbEncodedPath, fbxEncodedPath)
        os.system(glb2fbxCommand)

parser = argparse.ArgumentParser(
                    prog = 'BakedSDF2FBX',
                    description = 'A utility script to encode the custom vertex attributes of the BakedSDF GLB file in the UV channels and convert it to FBX.',
                    )

parser.add_argument('path', help="The path for a BakedSDF GLB file or a directoy that contains multiple GLB files for batch processing.") 
parser.add_argument('-s', '--skip-fbx', required=False, help="By default, the script will convert the GLB file to FBX. Use this flag to skip the convertion step.",
                    action='store_false')  # on/off flag

args = parser.parse_args()
path = args.path
if(not os.path.exists(path)):
    print(path + " doesn't exist!")
    exit()

if os.path.isfile(path):
    if Path(path).suffix == ".glb":
        EncodeSHDataInUVs(path, args.skip_fbx)
    else:
        print(path + " is not a GLB file!")
        
elif os.path.isdir(path):
    files = glob.glob(path+"/*.glb")
    for file in files:
        EncodeSHDataInUVs(file, args.skip_fbx)


