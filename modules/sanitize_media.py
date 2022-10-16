from PIL import Image
import moviepy.editor as mp
from os import remove, path

from modules.media_type import *

def convert_img_to_jpg(file_path):
    path_tuple = path.splitext(file_path)
    new_path = f'{path_tuple[0]}.jpg'
    image = Image.open(file_path)
    image.convert('RGB').save(new_path)
    remove(file_path)
    return new_path

def gif_to_mp4(file_path):
    from time import sleep
    new_path = file_path.replace(".gif", ".mp4")
    clip = mp.VideoFileClip(file_path)
    clip.write_videofile(new_path)
    clip.close()
    remove(file_path)
    return new_path