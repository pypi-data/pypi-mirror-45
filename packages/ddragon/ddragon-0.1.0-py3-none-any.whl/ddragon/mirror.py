import requests, json
import tarfile
import shutil,  os, glob

def update(ddragonDir, latest=False, resize=None):
    # Get ddragon latest version
    url="http://ddragon.leagueoflegends.com/realms/euw.json"
    r = requests.get(url)
    version = r.json()["v"]

    # Check if mirror is up to date
    if not version in os.listdir():
        # Get dragontail
        r = requests.get("http://ddragon.leagueoflegends.com/cdn/dragontail-"+version+".tgz")
        with open(ddragonDir+"/dragontail.tgz","wb") as file:
            file.write(r.content)

        # Unzip dragontail
        tar = tarfile.open(ddragonDir+"/dragontail.tgz", "r:gz")
        tar.extractall(ddragonDir)
        tar.close()

        # Clean up files
        for d in glob.iglob(ddragonDir+'/lolpatch*'):
            shutil.rmtree(d)
        os.remove(ddragonDir+"/dragonhead.js")
        os.remove(ddragonDir+"/dragontail.tgz")
        os.remove(ddragonDir+"/languages.js")
        os.remove(ddragonDir+"/languages.json")

        shutil.rmtree(ddragonDir+"/"+version+"/css")
        shutil.rmtree(ddragonDir+"/"+version+"/js")
        os.remove(ddragonDir+"/"+version+"/manifest.js")
        os.remove(ddragonDir+"/"+version+"/manifest.json")

        if latest:
            # Copy last version into latest
            if os.path.exists(ddragonDir+"/latest"):
                shutil.rmtree(ddragonDir+"/latest")
            shutil.copytree(ddragonDir+"/"+version, ddragonDir+"/latest")

        if not resize is None:
            
            try:
                from PIL import Image
                from resizeimage import resizeimage
            except ImportError as e:
                print("You need to install the extra packages to use the image resize features.")
                raise(e)


            for images in resize:

                imgDir = ddragonDir+"/latest/img/{}/".format(images["group"])
                for i in os.listdir(imgDir):
                    if not i.startswith("."):
                        with open(imgDir+i, 'r+b') as f:
                            with Image.open(f) as image:
                                if type(images["width"]) == int:
                                    cover = resizeimage.resize_width(image, images["width"])
                                    cover.save(imgDir+i.split(".")[0]+"_"+str(images["width"])+"."+i.split(".")[1], image.format)
                                elif type(images["width"]) == list:
                                    for width in images["width"]:
                                        cover = resizeimage.resize_width(image, width)
                                        cover.save(imgDir+i.split(".")[0]+"_"+str(width)+"."+i.split(".")[1], image.format)

