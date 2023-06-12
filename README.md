# BakedSDF2FBX

## About
**BakedSDF2FBX** is a utility script for converting BakedSDF GLB files to FBX. This allows for BakedSDF meshes to be imported and used in real-time 3D tools like Unity and Unreal Engine. 


**BakedSDF** is a method for reconstructing high-quality meshes for photorealistic novel view synthesis. BakedSDF bakes high-quality triangle meshes that are equipped with a simple and fast view-dependent appearance model based on spherical Gaussians. 

You can read more about BakedSDF in their official page: [BakedSDF: Meshing Neural SDFs for Real-Time View Synthesis](https://bakedsdf.github.io/)

*Please note, I am not affiliated with the original authors or their institution.*

## Usage

* Start by cloning this repository.

* Install the required libraries using `pip`.

```
pip install -r requirements.txt
```

* Run the `BakedSDF2FBX.py` script on a GLB file or a folder containing multiple GLB files. (Read the details section for an overview of what the script does). By default, the script will output a new GLB file and convert it to FBX. You can skip that last step using the `--skip-fbx` flag. 

```
python BakedSDF2FBX.py "Path/to/GLB/file/"
```


## Sample Scenes
The [official BakedSDF page](https://bakedsdf.github.io/#demos) has a demo with some sample scenes. You can download the GLB files for those scenes using the `DownloadBakedSDFSamples.py` script. 
You can run the script by specifying the path where you want to download the files, and a sample scene name. Alternatively, use the `--all` flag to download all the available sample scenes.

```
python DownloadBakedSDFSamples.py "Path/where/to/download/" --name SceneName
```
## Requirements
* **Blender:** For the GLB/FBX conversion to work, you'll need Blender installed and added to your system `path` variable.
If you only intend to use the `BakedSDF2FBX.py` script with the `--skip-fbx` flag then Blender is not required.  


## Details

**BakedSDF** uses a set of spherical Gaussian lobes for the view-dependent appearance. For each spherical gaussian, a color (Three 8-bit integers), mean (Three 8-bit integers) and a scale (One 8-bit integer) are stored per vertex. 

In the original meshes, the data is passed in custom vertex attributes since it's supported by glTF. However, real-time 3D tools like Unity and Unreal Engine have limited support for glTF and especially for custom vertex attributes. 

**BakedSDF2FBX** encodes all the required data for each spherical gaussian in one UV channel. The vertex shader that will be used later to render the mesh decodes the data from the UV. The detailed areas of the BakedSDF meshes use three spherical gaussians so the output encoded output will have three sets of UVs. The less detailed important areas of the mesh use only one spherical gaussian, but the script will ignore those in order to reduce the size of the mesh.



## References
[BakedSDF: Meshing Neural SDFs for Real-Time View Synthesis](https://bakedsdf.github.io/)
