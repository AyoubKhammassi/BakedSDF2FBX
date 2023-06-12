import os
import wget
import argparse
 
scene_list = {
    "gardenvase" : "7srlfofbiryehn6/gardenvase.glb",
    "bicycle" : "3ss5rc56bg0s9k5/bicycle.glb",
    "kitchenlego" : "jbjhvht3s6vvir2/kitchenlego.glb",
    "stump" : "1hqrcw1ax59b34z/stump.glb",
    "officebonsai" : "6bghm2gdmgzg32n/officebonsai.glb",
    "fulllivingroom" : "8r83yv14c0d2wxe/fulllivingroom.glb",
    "kitchencounter" : "zw6trrwjnh56pyp/kitchencounter.glb"
}

baseurl = "https://dl.dropboxusercontent.com/s/"


def download_scenes(scene_names, base_dir):
    for scene in scene_names:
        print("\n\n")
        print("*********************************************")
        print("Downloading BakedSDF sample scene: " + scene)
        scene_dir = os.path.abspath(base_dir)
        if(not os.path.exists(scene_dir)):
            os.makedirs(scene_dir)

        scene_url = baseurl + scene_list[scene] 

        print("Downloading files...")
        print("From URL: " + scene_url)
        print("To directory: "+ scene_dir)

        response = wget.download(scene_url, scene_dir)
        print(response)


parser = argparse.ArgumentParser(
                    prog = 'DownloadBakedSDFDemoSamples',
                    description = 'A helper script to download BakedSDF demo samples',
                    )

parser.add_argument('downloadPath', help="The path where the sample scenes will be downloaded.") 
parser.add_argument('-n', '--name', required=False, help="The name of a specific sample scene.", choices= scene_list.keys())
parser.add_argument('-a', '--all', required=False, help="Download all the sample scenes. Ignores --name if this is used",
                    action='store_true')  # on/off flag

args = parser.parse_args()

if args.all or args.name is None:
    print("Downloading all BakedSDF demo samples.")
    download_scenes(scene_list.keys, os.path.join(args.downloadPath, "BakedSDF_Samples"))
else:
    print("Downloading {0} BakedSDF demo sample .".format(args.name))
    download_scenes(([args.name]), os.path.join(args.downloadPath))




        





