import platform
import tkinter as tk
from PIL import Image, ImageTk
from timeit import default_timer as timer
import style
from widgets import ThemedLabel, ThemedListbox
from locations import notfoundimage
from appstore import Store_handler
from asyncthreader import threader

class categorylistFrame(tk.Frame):
    def __init__(self,parent,controller,framework, packages):
        #list of packages to be displayed by this frame
        self.packages = packages
        self.parent = parent
        self.controller = controller #Frame manager
        self.framework = framework #**Scheduler
        self.appstore_handler = Store_handler #Tool to get installed package data etc
        self.current_search = None
        self.selected = False
        self.sort_type = None
        self.listbox_list = []

        tk.Frame.__init__(self, parent, background = style.w, border = 0, highlightthickness = 0)

        threader.do_async(self.build_listframe)

    def build_listframe(self):
        columnwidth = 0.33 * (self.winfo_width() - style.updated_column_width)
        self.body_frame = tk.Frame(self, background = style.color_1)
        self.body_frame.place(relwidth = 1, relheight = 1) 
        self.scrollbar = tk.Scrollbar(self.body_frame, troughcolor = style.color_1, bg = style.color_2)
        self.scrollbar.place(relheight = 1, width = style.scrollbarwidth, relx = 1, x = -style.scrollbarwidth, height = - (style.listbox_footer_height + style.listbox_footer_height), y = + style.listbox_footer_height)
        self.listbox_frame = tk.Frame(self.body_frame, background = style.color_2)
        self.listbox_frame.place(relwidth = 1, relheight = 1, height =-style.listbox_footer_height, width = -style.scrollbarwidth)
        self.scaling_listboxes_frame = tk.Frame(self.listbox_frame, background = style.color_2)
        self.scaling_listboxes_frame.place(relwidth = 1, relheight = 1, width = -style.updated_column_width)
        self.scaling_listboxes_frame_header = tk.Frame(self.scaling_listboxes_frame, background = style.color_2)
        self.scaling_listboxes_frame_header.place(relwidth = 1, height = style.listbox_header_height)
        self.scaling_listboxes_frame_body = tk.Frame(self.scaling_listboxes_frame, background = style.color_2)
        self.scaling_listboxes_frame_body.place(relwidth = 1, relheight = 1, y = style.listbox_header_height, height = -style.listbox_header_height)
        self.package_listbox = ThemedListbox(self.scaling_listboxes_frame_body, background = style.color_2,font = style.smallboldtext, borderwidth = 1, foreground = style.w)
        self.package_listbox.place(relx = 0, relwidth = 0.33333, relheight = 1)
        self.package_listbox_label = ThemedLabel(self.scaling_listboxes_frame_header, text = "Package", background = style.color_1, font = style.mediumboldtext)
        self.package_listbox_label.place(relx = 0, relwidth = 0.33333, relheight = 1)
        self.title_listbox = ThemedListbox(self.scaling_listboxes_frame_body, background = style.color_2,font = style.smalltext, borderwidth = 1)
        self.title_listbox.place(relx = 0.33333, relwidth = 0.33333, relheight = 1)
        self.title_listbox_label = ThemedLabel(self.scaling_listboxes_frame_header, text = "Title", background = style.color_1, font = style.mediumboldtext)
        self.title_listbox_label.place(relx = 0.33333, relwidth = 0.33333, relheight = 1)
        self.author_listbox = ThemedListbox(self.scaling_listboxes_frame_body, background = style.color_2,font = style.smalltext, borderwidth = 1)
        self.author_listbox.place(relx = 0.66666, relwidth = 0.33333, relheight = 1)
        self.author_listbox_label = ThemedLabel(self.scaling_listboxes_frame_header, text = "Author", background = style.color_1, font = style.mediumboldtext)
        self.author_listbox_label.place(relx = 0.66666, relwidth = 0.33333, relheight = 1)
        self.updated_listbox = ThemedListbox(self.listbox_frame, background = style.color_2,font = style.smalltext, borderwidth = 1)
        self.updated_listbox.place(relx = 1, width = style.updated_column_width, x = -style.updated_column_width, relheight = 1, y = style.listbox_header_height, height = -style.listbox_header_height)
        self.updated_listbox_label = ThemedLabel(self.listbox_frame, text = "Updated", background = style.color_1, font = style.mediumboldtext)
        self.updated_listbox_label.place(relx = 1, width = style.updated_column_width, x = -style.updated_column_width, height = style.listbox_header_height)
        self.listbox_list = [
            self.package_listbox,
            self.title_listbox,
            self.author_listbox,
            self.updated_listbox
        ]
        self.listbox_frame_footer = tk.Frame(self, background = style.color_1)
        self.listbox_frame_footer.place(relwidth = 1, rely = 1, y = - style.listbox_footer_height, height = style.listbox_footer_height)
        self.installed_label = ThemedLabel(self.listbox_frame_footer, text = "Installed - ◆", background = style.color_1, foreground = "green", anchor = "center")
        self.installed_label.place(relx = 0, relwidth = 0.333, relheight = 1)
        self.hasupdate_label = ThemedLabel(self.listbox_frame_footer, text = "Update Available - ◆", background = style.color_1, foreground = "yellow", anchor = "center")
        self.hasupdate_label.place(relx = 0.333, relwidth = 0.333, relheight = 1)
        self.notinstalled_label = ThemedLabel(self.listbox_frame_footer, text = "Not installed - ◆", background = style.color_1, foreground = "white", anchor = "center")
        self.notinstalled_label.place(relx = 0.666, relwidth = 0.333, relheight = 1)
        self.package_listbox.configure({"selectbackground" : style.lg})
        self.package_listbox.configure({"selectmode" : "single"})
        self.package_listbox.bind("<<ListboxSelect>>", self.on_listbox_selection)

        self.scrollbar.config(command=self.on_scroll_bar)
        self.package_listbox.config(yscrollcommand=self.scrollbar.set)         

        self.set_sort_type(None)
        self.rebuild()


    def get_current_packages(self):
        packages = self.search_packages(self.current_search)
        if self.sort_type:
            packages = self.sort_packages(packages, self.sort_type)
        return packages

    def configure(self, event = None):
        self.rebuild()

    def search_packages(self, search: str = ""):
        if search:
            packages = []
            for package in self.packages:
                try:
                    for field in ["author", "name", "title", "description"]:
                        if search.lower() in package[field].lower():
                            packages.append(package)
                            break
                except:
                    pass
            return packages if packages else [{"name" : "NO RESULTS", "title" : "", "author" : "", "updated" : ""}]
        else:
            return self.packages

    def on_listbox_selection(self, event):
        selection=self.package_listbox.curselection()
        picked = self.package_listbox.get(selection[0])
        for package in self.packages:
            if package["name"] == picked:
                self.open_details(package)

    def sort_packages(self, packages, sort_method):
        reverse = False
        if sort_method.endswith('-'):
            reverse = True
            sort_method = sort_method.strip('-')

        return sorted(packages, key=lambda k: k[sort_method], reverse = reverse)

    def rebuild(self):
        self.build_frame(self.get_current_packages())
    
    def build_frame(self, packages):
        def do_build_frame():
            if not packages:
                return

            self.clear()

            if self.listbox_list:
                for lb in self.listbox_list:
                    lb.configure(state = "normal")

                installed_packages = self.appstore_handler.get_packages(silent = True)

                for package in packages:
                    self.package_listbox.insert('end', package["name"])
                    self.title_listbox.insert('end', package["title"])
                    self.author_listbox.insert('end', package["author"])
                    self.updated_listbox.insert('end', package["updated"])
                    if installed_packages:
                        if package["name"] in installed_packages:
                            if self.appstore_handler.get_package_version(package["name"]) == package["version"]:
                                self.package_listbox.itemconfig('end', {"fg" : "green"})
                            else:
                                self.package_listbox.itemconfig('end', {"fg" : "yellow"})

                for lb in self.listbox_list:
                    lb.configure(state = "disable")
                self.package_listbox.configure(state = 'normal')

                bindlist = [
                    self,
                    self.package_listbox,
                    self.title_listbox,
                    self.author_listbox,
                    self.updated_listbox
                ]

                if platform.system() == 'Windows' or platform.system() == "Darwin":
                    for b in bindlist:
                        b.bind("<MouseWheel>", self.on_mouse_wheel)
                elif platform.system() == "Linux":
                    for b in bindlist:
                        b.bind("<Button-4>", self.on_mouse_wheel)
                        b.bind("<Button-5>", self.on_mouse_wheel)
                        
        threader.do_async(do_build_frame)

    def open_details(self, package):
        self.controller.frames["detailPage"].show(package)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def is_selected(self):
        return self.selected

    def search(self, searchterm):
        self.current_search = searchterm
        self.rebuild()

    def clear(self):
        if self.listbox_list:
            for lb in self.listbox_list:
                lb.configure(state = "normal")
                lb.delete(0, "end")
                lb.configure(state = "disable")

    def on_scroll_bar(self, move_type, move_units, __ = None):
        if move_type == "moveto":
            for lb in self.listbox_list:
                lb.yview("moveto", move_units)

    def on_mouse_wheel(self, event):
        try:
            if platform.system() == 'Windows':
                self.package_listbox.yview("scroll", int(-1*(event.delta/120),"units"))
            elif platform.system() == "Linux":
                if event.num == 5:
                    self.package_listbox.yview("scroll", 1,"units")
                if event.num == 4:
                    self.package_listbox.yview("scroll", -1,"units")
            elif platform.system() == "Darwin":
                self.package_listbox.yview("scroll", event.delta,"units")

            for listbox in self.listbox_list:
                listbox.yview_moveto(self.package_listbox.yview()[0])

            return "break"
        except:
            pass

    def set_sort_type(self, sort_type):
        self.sort_type = sort_type