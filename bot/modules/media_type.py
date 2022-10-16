from enum import Enum
import os

class MediaType(Enum):
    INVALID = 0
    IMAGE = 1
    GIF = 2
    VIDEO = 3

def which_media_type(image_path):
    path_tuple = os.path.splitext(image_path)

    match path_tuple[1]:
        case ".jpg" | ".png" | ".webp" | ".jpeg":
            return MediaType.IMAGE
        case ".mp4":
            return MediaType.VIDEO
        case ".gif":
            return MediaType.GIF
        case other:
            return MediaType.INVALID