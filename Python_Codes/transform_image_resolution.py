from PIL import Image
import os
import argparse
def rescale_images(directory, size):
    for img in os.listdir(directory):
        im = Image.open(directory+img)
        im_resized = im.resize(size, Image.ANTIALIAS)
        im_resized.save(directory+img)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rescale images")
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing the images')
    parser.add_argument('-s', '--size', type=int, nargs=2, required=True, metavar=('width', 'height'), help='Image size')
    args = parser.parse_args()
    rescale_images(args.directory, args.size)


#python3 transform_image_resolution.py -d /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Yamaha_Oficial_Images/yamaha_2_960x540/ -s 960 540
#python3 transform_image_resolution.py -d /home/igor/Documentos/Developments/Experiment_Plan/Images_Generated_Blender/Test1_Images_Train/ -s 960 540