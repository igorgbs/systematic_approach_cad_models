
from PIL import Image  # Python Image Library - Image Processing
import glob
#print(glob.glob("*.png"))
# based on SO Answer: https://stackoverflow.com/a/43258974/5086335
for file in glob.glob("/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Images_Generated_Blender/Test12_Real_Images_Test/*.jpg"):
    im = Image.open(file)
    rgb_im = im.convert('RGB')
    rgb_im.save(file.replace("jpg", "png"), quality=95)
