from PIL import Image, ImageTk
from shutil import copy2
from shutil import move
import os
from preview_gui import Preview
from preview_gui import RESULT_RENAME, RESULT_REPLACE, RESULT_SKIP, RESULT_DELETE

MIN = 0
DEFAULT = 1
MAX = 2
EXTRA = 3
ULTRA = 4

MIN_SIZE = (64, 64)
DEFAULT_SIZE = (128, 128)
MAX_SIZE = (256, 256)
EXTRA_SIZE = (512, 512)
ULTRA_SIZE = (1024, 1024)

SIZE = [
    MIN_SIZE,
    DEFAULT_SIZE,
    MAX_SIZE,
    EXTRA_SIZE,
    ULTRA_SIZE
]


def dirs(path):
    if os.path.isdir(path):
        return path
    else:
        return os.path.dirname(path)

def take_date_time(file_name):
    import FileMetaData
    date_time = FileMetaData.get_image_take_date(file_name)
    return date_time

def picture_size(file_name):
    return os.path.getsize(file_name)

def name(path):
    if os.path.isfile(path):
        return os.path.basename(path)
    else:
        return os.path.dirname(path)

def request_view(photo1=None, photo2=None, index=0):
    p = Preview(photo_1=photo1, photo_2=photo2, index=index)
    p.win.mainloop()
    p.win.destroy()
    return p.result


# def _copy(source, target):
#     if os.path.isfile(target):
#         return False
#     else:
#         return copy2(source, target)

def _copy(source, target, state=False):
    if state:
        return move(source, target)
    else:
        if os.path.isfile(target):
            return False
        else:
            return move(source, target)

class Picture:
    def __init__(self, img_path, out_dir=None, new_size=ULTRA):

        self.__take_date = None
        self.__take_time = None

        self.__image = None

        self.__size = SIZE[new_size]

        self.__path = img_path
        self.__out_dir = out_dir
        self.__name = name(img_path)

        trash, self.__type = os.path.splitext(img_path)

    def take_date(self):
        import FileMetaData
        date_time = FileMetaData.get_image_take_date(self.__path)

        if date_time:
            self.__take_time = date_time.replace(":", ":")[11:19]
            # print(self.__take_time)
            self.__take_date = date_time.replace(":", "/")[0:10]
            # print(self.__take_date)
            return self.__take_date
        else:
            return None

    def pic(self, img_path=None, size=None):
        if img_path:
            self.__path = img_path

        if size:
            self.__size = SIZE[size]

        if self.__image is None:
            self.__image = Image.open(self.__path)

        r_img = self.__image.resize(self.__size, Image.ANTIALIAS)
        return ImageTk.PhotoImage(r_img)

    def type_ex(self):
        return self.__type

    def file_name(self, path=None):
        if path:
            if os.path.isfile(path):
                return os.path.basename(path)
            else:
                return None
        else:
            if self.__name:
                return self.__name
            else:
                return os.path.basename(self.__path())

    def _set_size(self, new_size):
        if new_size in range(len(SIZE)):
            self.__size = SIZE[new_size]

    def picture_size(self):
        return os.path.getsize(self.__path)

    def take_time(self):
        return self.__take_time

    def take_date_per(self):
        import ConvertToPersian
        import jalali


        # print('picture_factory : Picture : take_date_per : file = ', self.__path)
        # print('picture_factory : Picture : take_date_per : jalali_take_date = ', self.__take_date)

        file_date = self.take_date()
        jalali_take_date = jalali.Gregorian(file_date).persian_string_full_format()

        # print('picture_factory : Picture : take_date_per : jalali_take_date = ', jalali_take_date)
        pic_take_date_per = ConvertToPersian.getPer(jalali_take_date)
        return pic_take_date_per


    def get_path(self):
        try:
            fl = os.listdir(self.__out_dir)

            for p in fl:
                # print(p[0:10], " -> ", self.take_date_per())
                if p[0:10] == self.take_date_per():
                    return self.__out_dir + "/" + p + "/" + self.file_name()

        except FileNotFoundError:
            print('FNF')

        des = request_view(self.__path)
        if des:
            return self.__out_dir + "/" + self.take_date_per() + "_" + des + "/" + self.file_name()
        else:
            return self.__out_dir + "/" + self.take_date_per() + "/" + self.file_name()

    def get_dir(self):
        return dirs(self.__path)

    def copy(self):

        source = self.__path

        if self.take_date():
            target = self.get_path()
        else:
            target = self.__out_dir + "/other/" + self.file_name()

        # print('Picture : source = ', source)
        # print('Picture : target = ', target)

        if not os.path.isdir(dirs(target)):
            os.makedirs(dirs(target), mode=0o777, exist_ok=True)

        # print('Picture : source = ', source)
        # print('Picture : target = ', target)

        if target == source:
            return



        r = False
        index = 0
        while not r:
            r = _copy(source, target)
            if not r:
                if take_date_time(source) == take_date_time(target) and take_date_time(source) is not None:
                    if picture_size(source) == picture_size(target):
                        return

                res, new_name = request_view(source, target, index)
                if res == RESULT_RENAME:
                    r = _copy(source, dirs(target) + "/" + new_name)
                elif res == RESULT_REPLACE:
                    r = _copy(source, target, True)
                elif res == RESULT_SKIP:
                    r = True
                elif res == RESULT_DELETE:
                    try:
                        # print("Picture : copy : res == RESULT_DELETE : called.")
                        os.remove(source)
                        r = True
                    except NameError:
                        r = False
                index += 1
