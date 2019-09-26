from PIL import Image, ImageTk
from shutil import copy2
from shutil import move
from shutil import copytree
from shutil import disk_usage
from shutil import rmtree
import os
from preview_gui import Preview
from preview_gui import RESULT_RENAME, RESULT_REPLACE, RESULT_SKIP

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


def name(path):
    if os.path.isfile(path):
        return os.path.basename(path)
    else:
        return os.path.dirname(path)


def request_view(photo1=None, photo2=None, index=0):
    global parent
    p = Preview(photo_1=photo1, photo_2=photo2, index=index)
    p.win.mainloop()
    p.win.destroy()
    return p.result


def __copy(source, target):
    if os.path.isfile(target):
        return False
    else:
        return copy2(source, target)


def copy(source, target):
    t_dir = dirs(target)
    if not os.path.isdir(t_dir):
        os.makedirs(t_dir, mode=0o777, exist_ok=True)

    r = False
    index = 0
    while not r:
        r = __copy(source, target)
        if not r:
            res, new_name = request_view(source, target, index)
            if res == RESULT_RENAME:
                r = __copy(source, dirs(target) + "/" + new_name)
            elif res == RESULT_REPLACE:
                r = True
            elif res == RESULT_SKIP:
                r = True
            index += 1


class Picture:
    def __init__(self,img_path, new_size=ULTRA):

        self.__take_date = None
        self.__take_time = None

        self.__path = img_path

        self.__image = None

        self.__size = SIZE[new_size]

        self.__dir = dirs(img_path)
        self.__name = name(img_path)
        trash, self.__type = os.path.splitext(img_path)

        import FileMetaData
        self.__take_date = FileMetaData.getImageTakedDate(img_path)

        if self.__take_date is not None:
            self.__take_time = self.__take_date.replace(":", ":")[11:19]
            # print(self.__take_time)
            self.__take_date = self.__take_date.replace(":", "/")[0:10]
            # print(self.__take_date)

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

    def full_path(self):
        return self.__path

    def file_name(self, path=None):
        if path:
            if os.path.isfile(path):
                return os.path.basename(path)
            else:
                return None
        else:
            return self.__name

    def _set_size(self, new_size):
        if new_size in range(len(SIZE)):
            self.__size = SIZE[new_size]

    def take_time(self):
        return self.__take_time

    def take_date(self):
        return self.__take_date

    def take_date_per(self):
        import ConvertToPersian
        import jalali

        # print('picture_factory : Picture : take_date_per : jalali_take_date = ', self.__take_date)

        jalali_take_date  = jalali.Gregorian(self.__take_date).persian_string_full_format()
        # print('picture_factory : Picture : take_date_per : jalali_take_date = ', jalali_take_date)
        pic_take_date_per = ConvertToPersian.getPer(jalali_take_date)
        return pic_take_date_per
