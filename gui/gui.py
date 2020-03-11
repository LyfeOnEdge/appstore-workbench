import os, sys, json, glob, importlib, traceback
import tkinter as tk
import style, config
from .pages import __pages__
from .detailPage import DetailPage
from .widgets import *
from asyncthreader import threader


#Frame handler, raises and pages in z layer,
class window(tk.Tk):
	def __init__(self, args, geometry, version):
		tk.Tk.__init__(self)
		self.configure(background = style.primary_color)
		self.geometry(geometry)
		self.args = args
		self.frame_titles = None
		self.current_frame = None
		self.last_selection = None
		self.path = None
		self.pagelist = []
		self.has_update = None
		self.plugins = []
		self.version = version
		# self.resizable(False, False)

		self.detail_page = DetailPage(self)
		self.detail_page.place(relwidth = 1, relheight = 1)

		self.main_page = themedFrame.ThemedFrame(self, background = style.primary_color)
		self.main_page.place(relwidth = 1, relheight = 1)

		#Left column 
		self.column = themedFrame.ThemedFrame(self.main_page, background = style.primary_color)
		self.column.place(relx = 0, rely = 0, width = style.sidecolumnwidth, relheight = 1)

		self.column_title = themedLabel.ThemedLabel(self.column,"Appstore\nWorkbench\nGPLv3",anchor="center",font=style.largeboldtext, background = style.primary_color)
		self.column_title.place(relx = 0, y = + style.offset, relwidth = 1, height = style.column_headerheight - 2 * style.offset)

		self.column_title_separator = themedLabel.ThemedLabel(self.column, "", background=style.separator_color)
		self.column_title_separator.place(x = style.offset, y = style.column_headerheight - 1.5 * style.offset, relwidth = 1, width = -2 * style.offset, height = 1)

		self.category_listbox = scrollingWidgets.ScrolledThemedListBox(self.column, foreground = style.lg, borderwidth = 0, highlightthickness = 0)
		self.category_listbox.configure(activestyle = "none")
		self.category_listbox.place(relx = 0, relwidth = 1, y = style.column_headerheight, relheight = 1, height = - (2 * style.listbox_footer_height + style.column_headerheight + 2 * style.offset), width = - style.offset)
		self.category_listbox.bind('<<ListboxSelect>>',self.select_frame)

		self.column_footer_separator = themedLabel.ThemedLabel(self.column, "", background=style.separator_color)
		self.column_footer_separator.place(x = style.offset, rely = 1, y = - (2 * style.listbox_footer_height + style.offset), relwidth = 1, width = -2 * style.offset, height = 1)

		self.column_footer = themedFrame.ThemedFrame(self.column, background = style.primary_color)
		self.column_footer.place(relx = 0, rely = 1, relwidth = 1, height = 2 * style.listbox_footer_height, y = - 2 * style.listbox_footer_height)

		self.column_set_sd = button.Button(self.column_footer, 
			callback = self.set_sd, 
			text_string = "- Select Target Folder -", 
			font=style.mediumtext, 
			background=style.set_sd_button_background,
			foreground=style.set_sd_button_foreground
			).place(relwidth = 1, y = 0, x = style.offset, width = - 2 * style.offset, height = style.listbox_footer_height)

		self.column_sd_status_label = themedLabel.ThemedLabel(self.column_footer,"SD - Not Set",anchor="center",font=style.smalltext, background = style.primary_color, foreground= style.pathdisplaytextcolor)
		self.column_sd_status_label.place(x = style.offset, relwidth = 1, width = - 2 * style.offset, y = -style.listbox_footer_height, height = style.listbox_footer_height, rely=1,  )

		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		self.container = themedFrame.ThemedFrame(self.main_page)
		self.container.place(x = style.sidecolumnwidth, width = - style.sidecolumnwidth, relwidth = 1, relheight = 1)

		self.frames = {}

		self.load_plugins()
		#Stack pages in container	
		self.load_utility_pages()

		self.category_listbox.select_set(0) #sets focus on the first item in listbox
		self.category_listbox.event_generate("<<ListboxSelect>>")

		self.show_frame(self.pagelist[0].name)

		#Pull the main page to focus
		self.main_page.tkraise()

	def select_frame(self, event):
		try:
			widget = event.widget
			selection = widget.curselection()
			picked = widget.get(selection[0])
			if not picked == self.last_selection:
				frame = None
				for f in self.frames:
					self.frames[f].picked = False
					if self.frames[f].name.strip() == picked.strip():
						self.frames[f].picked = True #Only reload frame if it's visible, saves a lot of unnecessary page rebuilds and makes resizing faster
						self.show_frame(self.frames[f].name)
				self.last_selection = picked
		except Exception as e:
			print(e)
			pass

	def show(self):
		self.tkraise()

	def show_frame(self, page_name):
		#Show frame for the given page name
		frame = self.frames[page_name]
		frame.event_generate("<<ShowFrame>>")
		frame.tkraise()
		print("Raised frame - {}".format(page_name))

	def set_version(self, version_string):
		self.version = version_string

	def load_plugins(self):
		"""Loads plugins at a given path"""

		pagelist = []
		def load_pages(plugin):
			pages = plugin.get_pages()
			if pages:
				numpages = len(pages)
				print(f"Adding {numpages} pages")
			else:
				print("No pages to load")

			pagelist.extend(pages)

		def get_plugins(plugins_path):
			plugins = []
			print(f"Searching for plugins at - {plugins_path}")
			modules = glob.glob(os.path.join(plugins_path,"*"))
			for m in modules:
				if (os.path.isfile(m) and m.endswith('.py') and not m.endswith('__init__.py')):
					plugins.append(m[1:])
				elif os.path.isfile(os.path.join(m, "plugin.py")):
					plugins.append(os.path.join(m, "plugin.py")[1:])
			print(f"Found {len(plugins)} plugins:")
			print(json.dumps(plugins, indent = 2))
			return plugins

		print("\n# Loading plugins.")
		plugins = []
		plugins_paths = ["./gui/plugins", "./plugins"]
		# plugins_paths.extend(plugins_path_list)
		for path in plugins_paths:
			plugins.extend(get_plugins(path))
		pluginlist = []
		for plugin in plugins:
			try:
				print(f"Loading plugin at {plugin}")
				plugin = plugin[:-3].replace("/", ".").replace("\\", ".")[1:]
				m = importlib.import_module(plugin)	#Import plugin
				plugin_object = m.setup(self, self.container) #Import lib and call setup to get plugin object
				pluginlist.append(plugin_object)
			except Exception as e:
				print(f"Exception loading plugin {plugin} - {e}")
				traceback.print_exc()

		threader.do_group()
		threader.join_group()

		print("Loading plugin pages")
		for plugin in pluginlist:
			self.load_pages(plugin.get_pages())

		print("# Done loading plugins.\n")
		self.load_pages(pagelist)

	def load_pages(self, pagelist):
		"""Sort pages in alphabetical order"""
		#Add pages as frames to dict, with keyword being the name of the frame
		pagelist.sort(key=lambda x: x.name, reverse=False)
		if pagelist:
			for F in pagelist:
				page_name = F.name
				self.frames[page_name] = F
				self.category_listbox.insert("end", " {}".format(page_name))

				#place the frame to fill the whole window, stack them all in the same place
				F.place(relwidth = 1, relheight = 1)
				self.pagelist.append(F)
		else:
			print("No pages to initialize.")

	def load_utility_pages(self):
		pagelist = []
		if __pages__:
			for page in __pages__:
				spec = importlib.util.spec_from_file_location(os.path.basename(page)[:-3], page)
				p = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(p)
				pagelist.append(p.setup(self, self.container))
		self.load_pages(pagelist)

	def reload_category_frames(self, force):
		print("Reloading frames")
		for frame in self.frames:
			try:
				self.frames[frame].configure(event = None, force = force)
			except Exception as e:
				f = self.frames[frame]
				print(f"Exception reloading frame - {f.name} - {e}")
				traceback.print_exc()

	def set_sd(self):
		chosensdpath = tk.filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
		self.path = chosensdpath
		self.reload_category_frames(True)
		self.update_sd_path()

	def update_sd_path(self, path = None):
		if not path:
			path = self.path
		chosensdpath = path
		if chosensdpath:
			#Get the basename
			basepath = os.path.basename(os.path.normpath(chosensdpath))
			#If we didn't find it, assume it's a root dir and just return the whole path
			if not basepath:
				basepath = chosensdpath
		else:
			basepath = "Not Set"
		self.column_sd_status_label.set("SD - {}".format(basepath))

	def exit(self):
		for plugin in self.plugins:
			plugin.exit()
		threader.exit()
		sys.exit()