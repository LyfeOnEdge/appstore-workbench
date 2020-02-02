import os
import tkinter as tk
import tkinter.filedialog
import locations
from widgets import ThemedFrame, ThemedLabel, ThemedListbox, activeFrame, scrolledText, button, tooltip, ScrolledThemedListBox
from appstore import Parser, Store_handler
from customwidgets import progressFrame
import style
from appstore import getScreenImage
from webhandler import opentab
from .yesnopage import yesnoPage
from asyncthreader import threader
from PIL import Image, ImageTk

class detailPage(activeFrame):
    def __init__(self, parent, controller):
        activeFrame.__init__(self,parent,controller)
        self.controller = controller
        self.appstore_handler = Store_handler
        self.package_parser = Parser
        self.selected_version = None
        self.version_index = None
        self.package = None

        self.bind("<Configure>", self.on_configure)

        self.column = ThemedFrame(self, background = style.color_1)
        self.column.place(relx = 1, rely = 0, width = style.sidecolumnwidth, relheight = 1, x = - style.sidecolumnwidth)

        self.column_body = ThemedFrame(self.column, background = style.color_1)
        self.column_body.place(relwidth=1, relheight=1)

        self.column_title = ThemedLabel(self.column_body,"",anchor="w",font=style.mediumboldtext, foreground = style.w, background = style.color_1)
        self.column_title.place(x = style.offset, width = - style.offset, rely = 0, relwidth = 1, height = style.detailspagemultiplier)

        self.column_author = ThemedLabel(self.column_body,"",anchor="w",font=style.smalltext, foreground = style.w, background = style.color_1)
        self.column_author.place(x = style.offset, width = - style.offset, y = style.detailspagemultiplier, relwidth = 1, height = 0.333 * style.detailspagemultiplier)

        self.column_version = ThemedLabel(self.column_body,"",anchor="w",font=style.smalltext, foreground = style.w, background = style.color_1)
        self.column_version.place(x = style.offset, width = - style.offset, y = 1.333 * style.detailspagemultiplier, relwidth = 1, height = 0.333 * style.detailspagemultiplier)

        self.column_license = ThemedLabel(self.column_body,"",anchor="w",font=style.smalltext, foreground = style.w, background = style.color_1)
        self.column_license.place(x = style.offset, width = - style.offset, y = 1.666 * style.detailspagemultiplier, relwidth = 1, height = 0.333 * style.detailspagemultiplier)

        self.column_package = ThemedLabel(self.column_body,"",anchor="w",font=style.smalltext, foreground = style.w, background = style.color_1)
        self.column_package.place(x = style.offset, width = - style.offset, y = 2.000 * style.detailspagemultiplier, relwidth = 1, height = 0.333 * style.detailspagemultiplier)

        self.column_downloads = ThemedLabel(self.column_body,"",anchor="w",font=style.smalltext, foreground = style.w, background = style.color_1)
        self.column_downloads.place(x = style.offset, width = - style.offset, y = 2.333 * style.detailspagemultiplier, relwidth = 1, height = 0.333 * style.detailspagemultiplier)

        self.column_updated = ThemedLabel(self.column_body,"",anchor="w",font=style.smalltext, foreground = style.w, background = style.color_1)
        self.column_updated.place(x = style.offset, width = - style.offset, y = 2.666 * style.detailspagemultiplier, relwidth = 1, height = 0.333 * style.detailspagemultiplier)

        # self.column_separator_top = ThemedLabel(self.column_body, "", background=style.lg)
        # self.column_separator_top.place(rely=1,relwidth = 1, x = + style.offset, y = - 3 * (style.buttonsize + style.offset) - 3 * style.offset - style.buttonsize - 1 - 0.5 * style.buttonsize, width = - 2 * style.offset, height = 1)

        # self.column_separator_bot = ThemedLabel(self.column_body, "", background=style.lg)
        # self.column_separator_bot.place(rely=1,relwidth = 1, x = + style.offset, y = - 3 * (style.buttonsize + style.offset) - style.offset - 1, width = - 2 * style.offset, height = 1)

        self.column_open_url_button = button(self.column_body, 
            callback = self.trigger_open_tab, 
            text_string = "VISIT PAGE", 
            font=style.mediumboldtext, 
            background=style.color_2,
            ).place(rely=1,relwidth = 1, x = + style.offset, y = - 3 * (style.buttonsize + style.offset), width = - 2 * style.offset, height = style.buttonsize)

        self.column_install_button = button(self.column_body, 
            callback = self.trigger_install, 
            text_string = "INSTALL", 
            font=style.mediumboldtext, 
            background=style.color_2
            )
        self.column_install_button.place(rely=1,relwidth = 1, x = + style.offset, y = - 2 * (style.buttonsize + style.offset), width = - 2 * style.offset, height = style.buttonsize)

        self.column_uninstall_button = button(self.column_body, 
            callback = self.trigger_uninstall, 
            text_string = "UNINSTALL", 
            font=style.mediumboldtext, 
            background=style.color_2
            )

        self.back_image = ImageTk.PhotoImage(Image.open(locations.backimage).resize((style.buttonsize, style.buttonsize), Image.ANTIALIAS))

        self.column_backbutton = button(self.column_body, image_object=self.back_image, callback=self.leave, background=style.color_1)
        self.column_backbutton.place(rely=1,relx=1,x = -(style.buttonsize + style.offset), y = -(style.buttonsize + style.offset))
        # self.column_backbutton_ttp = tooltip(self.column_backbutton,"Back to list")

        self.content_frame = ThemedFrame(self, background = style.color_2)
        self.content_frame.place(x = 0, width = -style.sidecolumnwidth, rely = 0, relheight = 1, relwidth = 1)

        self.content_frame_header = ThemedFrame(self.content_frame, background = style.color_2)
        self.content_frame_header.place(x = style.offset, width = - 2 * style.offset, rely = 0, relwidth = 1, height = style.detailspagemultiplier)

        self.content_frame_body = ThemedFrame(self.content_frame, background = style.color_2)
        self.content_frame_body.place(x = style.offset, width = - 2 * style.offset, y = style.detailspagemultiplier,relwidth = 1, height = -style.detailspagemultiplier, relheight=1)

        self.content_banner_image_frame = ThemedFrame(self.content_frame, background=style.color_2)
        self.content_banner_image_frame.place(x=0, y = + style.detailspagemultiplier, relwidth=1, height = - style.detailspagemultiplier, relheight = 0.4)

        self.content_banner_image = ThemedLabel(self.content_banner_image_frame,"",background = style.color_2,foreground=style.w,anchor="center",wraplength = None)
        self.content_banner_image.place(x=0, y = 0, relwidth=1, relheight = 1)

        self.content_frame_details = scrolledText(self.content_frame_body, wrap = 'word', font = style.smalltext, background = style.lg)
        self.content_frame_details.place(rely=0.4, relx=0,relwidth=1,relheight=0.6,x=+style.offset, width = - 2 * (style.offset), height=-style.offset)

        #Displays app name
        self.header_label = ThemedLabel(self.content_frame_header,"",anchor="w",font=style.giantboldtext, background = style.color_2, foreground=style.b)
        self.header_label.place(rely=0, y=0, relheight=0.65)

        #Displays app name
        self.header_author = ThemedLabel(self.content_frame_header,"",anchor="w",font=style.smalltext, background = style.color_2, foreground=style.color_1)
        self.header_author.place(rely=0.65, y=0, relheight=0.35)

        self.progress_bar = progressFrame(self)

        self.yesnoPage = yesnoPage(self)

    def on_menu_update(self, option):
        self.selected_tag_name.set(option)
        self.select_version(option)

    def update_page(self,package):
        self.selected_version = None

        self.package = package

        threader.do_async(self.update_banner)

        version = package["version"]

        self.column_title.set("Title: {}".format(package["title"]))

        self.column_author.set("Author: {}".format(package["author"]))
        self.column_version.set("Latest Version: {}".format(package["version"]))
        try:
            self.column_license.set("License: {}".format(package["license"]))
        except:
            self.column_license.set("License: N/A")


        self.column_package.set("Package: {}".format(package["name"]))

        ttl_dl = 0
        try:
            ttl_dl += package["web_dls"]
        except:
            pass
        try:
            ttl_dl += package["app_dls"]
        except:
            pass

        self.column_downloads.set("Downloads: {}".format(ttl_dl))
        self.column_updated.set("Updated: {}".format(package["updated"]))

        self.content_frame_details.configure(state="normal")
        self.content_frame_details.delete('1.0', "end")

        #Makes newlines in details print correctly. Hacky but :shrug:
        details = package["description"].replace("\\n", """
"""
            )
        self.content_frame_details.insert("1.0", details)
        self.content_frame_details.configure(state="disabled")


        self.header_label.set(package["title"])
        self.header_author.set(package["author"])

        #Hides or places the uninstalll button if not installed or installed respectively
        #get_package_entry returns none if no package is found or if the sd path is not set
        if self.appstore_handler.get_package_entry(package["name"]):
            self.column_uninstall_button.place(rely=1,relwidth = 1, x = + style.offset, y = - 1 * (style.buttonsize + style.offset), width = - (3 * style.offset + style.buttonsize), height = style.buttonsize)
            if self.column_install_button:
                if self.appstore_handler.clean_version(self.appstore_handler.get_package_version(package["name"]), package["title"]) > self.appstore_handler.clean_version(package["version"], package["title"]):
                    self.column_install_button.settext("UPDATE")
                else:
                    self.column_install_button.settext("REINSTALL")
        else:
            self.column_uninstall_button.place_forget()
            if self.column_install_button:
                self.column_install_button.settext("INSTALL")

        tags = []

    def select_version(self, option):
        try:
            self.selected_version = option
            self.version_index = self.controller.appstore_handler.get_tag_index(self.package["github_content"], self.selected_version)
            self.update_release_notes()
        except Exception as e:
            # print(e)
            pass

    def on_configure(self, event=None):
        if self.package:
            self.after(100, self.update_banner())

    def update_banner(self):
        self.bannerimage = getScreenImage(self.package["name"])
        if self.bannerimage:
            self.do_update_banner(self.bannerimage)
        else:
            self.do_update_banner(locations.notfoundimage)

    def do_update_banner(self,image_path):
        maxheight = self.content_banner_image_frame.winfo_height()
        maxwidth = self.content_banner_image_frame.winfo_width()
        if maxwidth > 0 and maxheight > 0:
            art_image = Image.open(image_path)
            wpercent = (maxwidth/float(art_image.size[0]))
            hsize = int((float(art_image.size[1])*float(wpercent)))
            w_img = art_image.resize((maxwidth,hsize), Image.ANTIALIAS)
            if w_img.size[0] > maxheight:
                hpercent = (maxheight/float(art_image.size[1]))
                wsize = int((float(art_image.size[0])*float(hpercent)))
                art_image = art_image.resize((maxwidth,hsize), Image.ANTIALIAS)
            else:
                art_image = w_img

            art_image = ImageTk.PhotoImage(art_image)

            self.content_banner_image.configure(image=art_image)
            self.content_banner_image.image = art_image

    def show(self, repo):
        self.do_update_banner(locations.notfoundimage)
        threader.do_async(self.update_page, [repo], priority = "medium")
        self.tkraise()
        for child in self.winfo_children():
            child.bind("<Escape>", self.leave)

    def leave(self):
        self.controller.show_frame("appstorePage")
        for child in self.winfo_children():
            child.unbind("<Escape>")

    def reload_function(self):
            self.controller.frames["appstorePage"].reload_category_frames()
            self.reload()

    def trigger_install(self):
        index = self.version_index or 0
        if not self.appstore_handler.check_path():
            self.set_sd()
        if self.appstore_handler.check_path():
            if self.appstore_handler.check_if_get_init():
                if self.package:
                    threader.do_async(self.appstore_handler.handler_install_package, [self.package, self.progress_bar.update, self.reload_function, self.progress_bar.set_title], priority = "high")
            else:
                self.yesnoPage.getanswer("The homebrew appstore has not been initiated here yet, would you like to initiate it?", self.init_get_then_continue)

    def init_get_then_continue(self):
        self.appstore_handler.init_get()
        self.trigger_install()

    def trigger_uninstall(self):
        if self.package:
            threader.do_async(self.appstore_handler.uninstall_package, [self.package], priority = "high")
            self.controller.frames["appstorePage"].reload_category_frames()
            self.schedule_callback(self.reload(), 100)

    def reload(self):
        threader.do_async(self.update_page, [self.package])

    def trigger_open_tab(self):
        if self.package:
            try:
                url = self.package["url"]
                opentab(url)
            except Exception as e:
                print("Failed to open tab - {}".format(e))

    def set_sd(self):
        chosensdpath = tkinter.filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
        self.appstore_handler.set_path(chosensdpath)
        self.reload()