import os
import tkinter as tk
import tkinter.filedialog
from gui.widgets import themedFrame, themedLabel, themedListbox, scrollingWidgets, button, progressFrame
import style
from webhandler import opentab
from .yesNoPage import YesNoPage
from asyncthreader import threader
from PIL import Image, ImageTk
import config

class DetailPage(themedFrame.ThemedFrame):
    def __init__(self, parent):
        themedFrame.ThemedFrame.__init__(self,parent)
        self.app = parent
        self.appstore_handler = None
        self.package_parser = None
        self.selected_version = None
        self.version_index = None
        self.package = None

        self.bind("<Configure>", self.on_configure)

        self.body = themedFrame.ThemedFrame(self, background = style.secondary_color)
        self.body.place(relwidth = 1, relheight = 1, width = -style.sidecolumnwidth)

        self.image_frame = themedFrame.ThemedFrame(self.body, background = style.secondary_color)
        self.image_frame.place(relwidth=1, relheight = style.details_page_image_fraction, x = + 2 * style.offset, width = - 4 * style.offset, y = + 2 * style.offset, height = - 2 * style.offset)

        self.banner_image = themedLabel.ThemedLabel(self.image_frame,"",background = style.secondary_color,anchor="center",wraplength = None)
        self.banner_image.place(relwidth = 1, relheight = 1)

        self.details = scrollingWidgets.ScrolledThemedText(self.body, font = style.smalltext, foreground = style.detail_page_label_color)
        self.details.place(relwidth = 1, relheight = 1 - style.details_page_image_fraction, rely = style.details_page_image_fraction, x = 2 * style.offset, width = - 4 * style.offset, y = + 2 * style.offset, height = -4 * style.offset)

        #RIGHT COLUMN
        self.column = themedFrame.ThemedFrame(self, background = style.primary_color)
        self.column.place(relx = 1, rely = 0, width = style.sidecolumnwidth, relheight = 1, x = - style.sidecolumnwidth)

        self.column_body = themedFrame.ThemedFrame(self.column, background = style.primary_color)
        self.column_body.place(relwidth=1, relheight=1)

        self.column_title = themedLabel.ThemedLabel(self.column_body,"",anchor="w",font=style.smallboldtext, foreground = style.primary_text_color, background = style.primary_color)
        self.column_title.place(x = style.offset, width = - style.offset, rely = 0, relwidth = 1, height = style.detais_page_title_height)

        self.column_author = themedLabel.ThemedLabel(self.column_body,"",anchor="w",font=style.smalltext, foreground = style.detail_page_label_color, background = style.primary_color)
        self.column_author.place(x = style.offset, width = - style.offset, y = style.detais_page_title_height + style.details_item_y_multiplier, relwidth = 1, height = 0.333 * style.details_item_y_multiplier)

        self.column_version = themedLabel.ThemedLabel(self.column_body,"",anchor="w",font=style.smalltext, foreground = style.detail_page_label_color, background = style.primary_color)
        self.column_version.place(x = style.offset, width = - style.offset, y = style.detais_page_title_height + 0.333 * style.details_item_y_multiplier, relwidth = 1, height = 0.333 * style.details_item_y_multiplier)

        self.column_license = themedLabel.ThemedLabel(self.column_body,"",anchor="w",font=style.smalltext, foreground = style.detail_page_label_color, background = style.primary_color)
        self.column_license.place(x = style.offset, width = - style.offset, y = style.detais_page_title_height + 0.666 * style.details_item_y_multiplier, relwidth = 1, height = 0.333 * style.details_item_y_multiplier)

        self.column_package = themedLabel.ThemedLabel(self.column_body,"",anchor="w",font=style.smalltext, foreground = style.detail_page_label_color, background = style.primary_color)
        self.column_package.place(x = style.offset, width = - style.offset, y = style.detais_page_title_height + 1.000 * style.details_item_y_multiplier, relwidth = 1, height = 0.333 * style.details_item_y_multiplier)

        self.column_downloads = themedLabel.ThemedLabel(self.column_body,"",anchor="w",font=style.smalltext, foreground = style.detail_page_label_color, background = style.primary_color)
        self.column_downloads.place(x = style.offset, width = - style.offset, y = style.detais_page_title_height + 1.333 * style.details_item_y_multiplier, relwidth = 1, height = 0.333 * style.details_item_y_multiplier)

        self.column_updated = themedLabel.ThemedLabel(self.column_body,"",anchor="w",font=style.smalltext, foreground = style.detail_page_label_color, background = style.primary_color)
        self.column_updated.place(x = style.offset, width = - style.offset, y = style.detais_page_title_height + 1.666 * style.details_item_y_multiplier, relwidth = 1, height = 0.333 * style.details_item_y_multiplier)

        # self.column_separator_top = ThemedLabel(self.column_body, "", background=style.lg)
        # self.column_separator_top.place(rely=1,relwidth = 1, x = + style.offset, y = - 3 * (style.buttonsize + style.offset) - 3 * style.offset - style.buttonsize - 1 - 0.5 * style.buttonsize, width = - 2 * style.offset, height = 1)

        # self.column_separator_bot = ThemedLabel(self.column_body, "", background=style.lg)
        # self.column_separator_bot.place(rely=1,relwidth = 1, x = + style.offset, y = - 3 * (style.buttonsize + style.offset) - style.offset - 1, width = - 2 * style.offset, height = 1)

        self.column_open_url_button = button.Button(self.column_body, 
            callback = self.trigger_open_tab, 
            text_string = "VISIT PAGE", 
            font=style.mediumboldtext, 
            background=style.secondary_color,
            ).place(rely=1,relwidth = 1, x = + 2 * style.offset, y = - 3 * (style.buttonsize + style.offset), width = - 4 * style.offset, height = style.buttonsize)

        self.column_install_button = button.Button(self.column_body, 
            callback = self.trigger_install, 
            text_string = "INSTALL", 
            font=style.mediumboldtext, 
            background=style.secondary_color
            )
        self.column_install_button.place(rely=1,relwidth = 1, x = + 2 * style.offset, y = - 2 * (style.buttonsize + style.offset), width = - 4 * style.offset, height = style.buttonsize)

        self.column_uninstall_button = button.Button(self.column_body, 
            callback = self.trigger_uninstall, 
            text_string = "UNINSTALL", 
            font=style.mediumboldtext, 
            background=style.secondary_color
            )

        self.back_image = ImageTk.PhotoImage(Image.open("gui/assets/return.png").resize((style.buttonsize, style.buttonsize), Image.ANTIALIAS))
        self.column_backbutton = button.Button(self.column_body, image_object=self.back_image, callback=self.leave, background=style.primary_color)
        self.column_backbutton.place(rely=1,relx=1,x = -(style.buttonsize + style.offset), y = -(style.buttonsize + style.offset))

        self.progress_bar = progressFrame.ProgressFrame(self)

        self.yesnoPage = YesNoPage(self)

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

        self.details.configure(state="normal")
        self.details.delete('1.0', "end")

        #Makes newlines in details print correctly. Hacky but :shrug:
        details = package["description"].replace("\\n", """
"""
            )
        self.details.insert("1.0", details)
        self.details.configure(state="disabled")

        self.update_buttons(package)

        tags = []

    def update_buttons(self, package):
        #Hides or places the uninstalll button if not installed or installed respectively
        #get_package_entry returns none if no package is found or if the sd path is not set
        if self.appstore_handler.get_package_entry(package["name"]):
            self.column_uninstall_button.place(rely=1,relwidth = 1, x = + 2 * style.offset, y = - 1 * (style.buttonsize + style.offset), width = - (4 * style.offset + style.buttonsize), height = style.buttonsize)
            if self.column_install_button:
                if self.appstore_handler.clean_version(self.appstore_handler.get_package_version(package["name"]), package["title"]) > self.appstore_handler.clean_version(package["version"], package["title"]):
                    self.column_install_button.settext("UPDATE")
                else:
                    self.column_install_button.settext("REINSTALL")
        else:
            self.column_uninstall_button.place_forget()
            if self.column_install_button:
                self.column_install_button.settext("INSTALL")

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
            self.update_banner()

    def update_banner(self):
        self.bannerimage = self.appstore_handler.getScreenImage(self.package["name"])
        if self.bannerimage:
            self.do_update_banner(self.bannerimage)
        else:
            self.do_update_banner("gui/assets/notfound.png")

    def do_update_banner(self,image_path):
        maxheight = self.image_frame.winfo_height()
        maxwidth = self.image_frame.winfo_width()
        if maxwidth > 0 and maxheight > 0:
            art_image = Image.open(image_path)
            wpercent = (maxwidth/float(art_image.size[0]))
            hsize = int((float(art_image.size[1])*float(wpercent)))
            new_image = art_image.resize((maxwidth,hsize), Image.ANTIALIAS)
            if new_image.size[1] > maxheight:
                hpercent = (maxheight/float(art_image.size[1]))
                wsize = int((float(art_image.size[0])*float(hpercent)))
                new_image = art_image.resize((wsize,maxheight), Image.ANTIALIAS)

            art_image = ImageTk.PhotoImage(new_image)

            self.banner_image.configure(image=art_image)
            self.banner_image.image = art_image





    def show(self, package, handler):
        self.appstore_handler = handler
        self.package_parser = handler
        self.do_update_banner("gui/assets/notfound.png")
        threader.do_async(self.update_page, [package], priority = "medium")
        self.tkraise()
        for child in self.winfo_children():
            child.bind("<Escape>", self.leave)

    def leave(self):
        self.app.main_page.tkraise()
        for child in self.winfo_children():
            child.unbind("<Escape>")

    def reload_function(self):
            self.app.reload_category_frames(force = True)
            self.reload()

    def trigger_install(self):
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
            self.appstore_handler.uninstall_package(self.package)
            self.app.reload_category_frames(True)
            self.app.after(100, self.reload)

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