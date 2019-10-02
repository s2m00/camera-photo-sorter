from exif import Image


def get_image_take_date(f_name):
    # print('FileMetaData : get_image_take_date : f_name = ', f_name)
    t, exception = f_name.split('.', -1)

    if exception.lower() == 'png':
        # from tkinter import simpledialog
        # date_string = simpledialog.askstring("set date [format: yyyy:mm:dd hh:mm:ss]", f_name)
        # print('FileMetaData : get_image_take_date : user input - date_string = ', date_string)

        # if date_string:
            # return date_string
        # else:
            return None

    try:
        with open(f_name, 'rb') as image_file:
            my_image = Image(image_file)

            if my_image.has_exif:
                date_string = my_image.get('datetime')
                if date_string:
                    if "?" in date_string:
                        return None
                    else:
                        # print('FileMetaData : get_image_take_date : file read - date_string = ', date_string)
                        return date_string
                else:
                    return None
            else:
                return None
    except NameError:
        return None


def get_image_orientation(f_name):
    try:
        with open(f_name, 'rb') as image_file:
            my_image = Image(image_file)
            if my_image.has_exif:
                return my_image.get('orientation')
    except NameError:
        return None


def get_image_metadata_tags(f_name):
    try:
        with open(f_name, 'rb') as image_file:
            my_image = Image(image_file)
            return dir(my_image)
    except NameError:
        return "Open error." + NameError
