# -*- coding: utf-8 -*-
#coding=UTF-*

from tkinter import *
from tkinter.ttk import Progressbar
import picture_factory
import getFiles

photo_sorter = None


def state(v, t, d):
    print(str(v) + " " + str(t) + " " + str(d))
    sort_btn['text'] = str(v) + " " + str(t) + " " + str(d)
    process["maximum"] = t
    process['value'] = v
    win.update_idletasks()

class PhotoSorter:
    def __init__(self):
        # variables

        self.sf = None
        self.photos_list_object = []
        self.s_list = []
        self.dir_date_name_list = []
        self.photo_path_list = getFiles.getPhotoFiles(source_dir.get())
        self.process = 0
        self.total = len(self.photo_path_list)
        # print('main_gui : PhotoSorter : out_dir = ', self.out_dir)

        if output_dir.get() == "":
            self.out_dir = source_dir.get() + "/out"
        else:
            self.out_dir = output_dir.get()

    def __set_state(self, where, total):
        self.process = where
        self.total = total

        if self.sf:
            self.sf(self.process, self.total, "{:.4}%".format((self.process * 100 / self.total)))

    def get_state(self, state_func):
        self.sf = state_func

    def get_photos(self):
        return self.photo_path_list

    def sort_photos(self):
        if output_dir.get() == "":
            self.out_dir = source_dir.get() + "/out"
        else:
            self.out_dir = output_dir.get()

        # get sorted photos path list
        for file in self.photo_path_list:
            self.photos_list_object.append(picture_factory.Picture(file, self.out_dir))

        # copy files to dirs and get duplicates command
        for i in range(len(self.photos_list_object)):
            self.photos_list_object[i].copy()
            self.__set_state(i+1, len(self.photos_list_object))

        print('PhotoSorter : sort_photos : Done')


def load_list():
    file_list_lst.delete(0, END)
    for p in photos:
        file_list_lst.insert(END, p)


def on_file_list_double_click(event):
    selected_item = file_list_lst.curselection()[0]
    # print("selected item = ", selected_item, "Event = ", event)

    picture_factory.request_view(photos[selected_item])

    source_dir_lbl['text'] = file_list_lst.get(selected_item)


def on_file_list_selected(event):
    selected_item = file_list_lst.curselection()[0]
    source_dir_lbl['text'] = file_list_lst.get(selected_item)


def start_sorting():
    if photo_sorter.get_photos() is not None:
        photo_sorter.get_state(state)
        photo_sorter.sort_photos()


def source_dir_selector():
    from tkinter import filedialog
    d = filedialog.askdirectory()
    if d:
        source_dir.set(d)

        get_photos()

        load_list()


def output_dir_selector():
    from tkinter import filedialog
    d = filedialog.askdirectory()
    if d:
        output_dir.set(d)


def get_photos():
    global photo_sorter
    # initialize PhotoSorter class with source path
    photo_sorter = PhotoSorter()

    global photos
    photos = photo_sorter.photo_path_list


if __name__ == '__main__':
    width = 300
    height = 150

    win = Tk()
    win.title("Sort Photo Files")
    win.minsize(width, height)

    win.rowconfigure(2, weight=1)
    win.columnconfigure(0, weight=1)

    source_dir = StringVar()
    output_dir = StringVar()

    import os
    home = os.path.expanduser('~')
    source_dir.set(home + "/Pictures")
    output_dir.set(home + "/Pictures/out")

    # define file list widget
    scrollbar = Scrollbar(win, orient=VERTICAL)
    file_list_lst = Listbox(win, yscrollcommand=scrollbar.set)
    scrollbar.config(command=file_list_lst.yview)
    scrollbar.grid(row=1, column=4, rowspan=3, sticky=N + S)

    # define label widget
    source_dir_lbl = Label(win, textvariable=source_dir)

    # define select source dir button widget
    select_source_btn = Button(text="Browse...", command=source_dir_selector)

    # define label widget
    output_dir_lbl = Label(win, textvariable=output_dir)

    # define select source dir button widget
    select_output_btn = Button(text="Browse...", command=output_dir_selector)

    photos = []

    get_photos()

    # define start sort button widget
    sort_btn = Button(win, text="Sort to dir", command=start_sorting)

    # define process bar
    process = Progressbar(win, length=100, value=0, orient=HORIZONTAL, mode='indeterminate')


    # add widgets
    source_dir_lbl.grid(row=0, column=0, columnspan=2, sticky=W, padx=10, pady=10)
    select_source_btn.grid(row=0, column=2)

    output_dir_lbl.grid(row=1, column=0, columnspan=2, sticky=W, padx=10, pady=10)
    select_output_btn.grid(row=1, column=2)

    file_list_lst.grid(row=2, column=0, columnspan=3, rowspan=3, padx=5, sticky=NSEW)

    sort_btn.grid(row=5, column=2)

    process.grid(row=5, column=0, columnspan=2, padx=5, sticky=EW)

    file_list_lst.bind('<Double-Button-1>', on_file_list_double_click)
    file_list_lst.bind('<<ListboxSelect>>', on_file_list_selected)

    # load photo list into list widget
    load_list()

    win.mainloop()
