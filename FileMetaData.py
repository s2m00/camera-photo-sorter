from exif import Image


def getImageTakedDate(f_name):
    try:
        with open(f_name, 'rb') as image_file:
            my_image = Image(image_file)
            if my_image.has_exif:
                return my_image.get('datetime')
    except:
        return None


def getImageOrientation(f_name):
    try:
        with open(f_name, 'rb') as image_file:
            my_image = Image(image_file)
            if my_image.has_exif:
                return my_image.get('orientation')
    except:
        return None


def getImageMetadataTags(f_name):
    try:
        with open(f_name, 'rb') as image_file:
            my_image = Image(image_file)
            return dir(my_image)
    except:
        return "Open error."
