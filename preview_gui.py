from tkinter import *
import picture_factory

RESULT_SKIP = -1
RESULT_RENAME = 1
RESULT_REPLACE = 2





class Preview:
    def set_photos(self, new_photo1=None, new_photo2=None, size=None):
        if size:
            self.__size = size

        # set photo 1
        if new_photo1:
            # load photo 1
            img = self.img1.pic(new_photo1, size=self.__size)
            self.photo1_lbl.configure(image=img)
            self.photo1_lbl.image = img

            name = self.img1.file_name(new_photo1)
            f_dir = picture_factory.dirs(new_photo1)
            self.photo1_name_lbl.configure(text=str(name + "\n" + f_dir))
        else:
            self.photo1_lbl.configure(image=self.img1.pic())
            self.photo1_lbl.image = self.img1.pic()

            name = self.img1.file_name(self.photo1_path)
            f_dir = picture_factory.dirs(self.photo1_path)
            self.photo1_name_lbl.configure(text=str(name + "\n" + f_dir))

        # set photo 2
        if new_photo2:
            # load photo 2
            img = self.img2.pic(new_photo2, size=self.__size)
            self.photo2_lbl.configure(image=img)
            self.photo2_lbl.image = img

            name = self.img2.file_name(new_photo2)
            f_dir = picture_factory.dirs(new_photo2)
            self.photo2_name_lbl.configure(text=str(name + "\n" + f_dir))
        else:
            if self.photo2_path:
                # self.img2 = pic(img_path=self.photo2_path, size=size)
                self.photo2_lbl.configure(image=self.img2.pic())
                self.photo2_lbl.image = self.img2.pic()

                name = self.img2.file_name(self.photo2_path)
                f_dir = picture_factory.dirs(self.photo2_path)
                self.photo2_name_lbl.configure(text=str(name + "\n" + f_dir))

    def select_dir_dis(self):
        print("Preview : select_dir_dis : set_dir_dis = ", self.set_dir_dis.get())
        self.result = self.set_dir_dis.get()
        self.win.quit()

    def __init__(self, width=None, height=None, photo_1=None, photo_2=None, index=0):
        self.new_pic_name = StringVar()
        self.set_dir_dis = StringVar()
        self.result = None
        if width is None:
            self.width = 500
        else:
            if width < 500:
                self.width = 500
        if height is None:
            self.height = 300
        else:
            if height < 300:
                self.height = 300

        self.__size = 2

        self.photo1_path = photo_1
        self.photo2_path = photo_2

        if self.photo1_path:
            self.img1 = picture_factory.Picture(self.photo1_path)

        if self.photo2_path:
            self.img2 = picture_factory.Picture(self.photo2_path)

        self.win = Toplevel()
        self.win.minsize(self.width, self.height)
        self.win.title("preview")

        # call self.close_mod when the close button is pressed
        self.win.protocol("WM_DELETE_WINDOW", self.close_mod)

        self.photo1_lbl = None
        self.photo2_lbl = None

        self.photo1_name_lbl = None
        self.photo2_name_lbl = None

        self.action_lbl = None
        self.rename_btn = None
        self.rename_txt = None
        self.replace_btn = None
        self.skip_btn = None

        self.set_dir_dis.set("")
        self.new_pic_name.set("")

        # add widgets for preview mode and compare preview mode
        if photo_1 and photo_2 is None:
            self.frame = Frame(self.win)

            self.frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

            self.photo1_lbl = Label(self.frame)
            self.photo1_name_lbl = Label(self.frame, text="name1")
            self.photo1_dir_name_entry = Entry(self.frame, textvariable=self.set_dir_dis)

            self.select_dir_name_btn = Button(self.frame, text="OK", command=self.select_dir_dis)

            self.photo1_lbl.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
            self.photo1_name_lbl.grid(row=1, column=0, padx=10, pady=10, sticky=EW)
            self.photo1_dir_name_entry.grid(row=2, column=0, padx=10, pady=10, sticky=EW)

            self.select_dir_name_btn.grid(row=0, column=1, ipadx=10, ipady=10, sticky=EW)

            self.photo1_dir_name_entry.focus_set()
        elif photo_1 and photo_2:
            self.pic_frame = Frame(self.win)
            self.pic_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

            self.photo1_lbl = Label(self.pic_frame)
            self.photo1_name_lbl = Label(self.pic_frame, text="name1")

            self.photo2_lbl = Label(self.pic_frame)
            self.photo2_name_lbl = Label(self.pic_frame, text="name2")

            self.photo1_lbl.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
            self.photo2_lbl.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)

            self.action_lbl = Label(self.pic_frame, text=" > ")
            self.action_lbl.grid(row=0, column=1, pady=5, sticky=NS)

            self.photo1_name_lbl.grid(row=1, column=0, padx=10, pady=10, sticky=EW)
            self.photo2_name_lbl.grid(row=1, column=2, padx=10, pady=10, sticky=EW)

            self.btn_frame = Frame(self.win)
            self.btn_frame.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

            name, exception = picture_factory.name(self.photo1_path).split('.', -1)
            s = (name + '_' + str(index) + '.' + exception)
            self.new_pic_name.set(s)
            # print('preview_gui : Preview : __init__ : new_pic_name = ', self.new_pic_name.get())

            self.rename_txt = Entry(self.btn_frame, text=self.new_pic_name)
            self.rename_btn = Button(self.btn_frame, text="Rename", command=self.on_click_rename_btn)
            self.replace_btn = Button(self.btn_frame, text="Replace", command=self.on_click_replace_btn)
            self.skip_btn = Button(self.btn_frame, text="Skip", command=self.on_click_skip_btn)

            self.rename_txt.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
            self.replace_btn.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)
            self.rename_btn.grid(row=1, column=1, padx=20, pady=10, sticky=NSEW)
            self.skip_btn.grid(row=1, column=2, padx=20, pady=10, sticky=NSEW)

        self.set_photos(new_photo1=photo_1, new_photo2=photo_2)

    # remove this function and the call to protocol
    # then the close button will act normally
    def close_mod(self):
        if self.photo1_path and self.photo2_path:
            self.result = RESULT_SKIP, None
        self.win.quit()

    def on_click_rename_btn(self):
        self.result = RESULT_RENAME, self.new_pic_name.get()
        self.win.quit()

    def on_click_replace_btn(self):
        self.result = RESULT_REPLACE, None
        self.win.quit()

    def on_click_skip_btn(self):
        self.result = RESULT_SKIP, None
        self.win.quit()
