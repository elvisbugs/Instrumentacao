from cefpython3 import cefpython as cef
import ctypes
import tkinter as tk

class MainFrame(tk.Frame):

    def __init__(self, root,position,size,url):
        self.browser_frame = None
        # MainFrame
        tk.Frame.__init__(self, root)
        # BrowserFrame
        self.browser_frame = BrowserFrame(self,position,size,url)

        # Pack MainFrame
        self.browser_frame.grid(row=1, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

class BrowserFrame(tk.Frame):

    def __init__(self, master,position,size,url):
        self.browser = None
        self.url = url
        self.xPos = position.rsplit(';')[0]
        self.yPos = position.rsplit(';')[1]
        self.height = size.rsplit(';')[0]
        self.width = size.rsplit(';')[1]
        tk.Frame.__init__(self, master,bg = '#161719')
        self.bind("<Configure>", self.on_configure)

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [self.xPos, self.yPos, self.width, self.height]
        window_info.SetAsChild(self.winfo_id(), rect)
        self.browser = cef.CreateBrowserSync(window_info, url=self.url)
        #assert self.browser
        self.message_loop_work()

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

class WebPage:
    def __init__(self,window, position, size, dir, url):
        self.app = MainFrame(window, position, size, url)
        settings = {
            "cache_path": dir + "\\cache\\"
        }
        cef.Initialize(settings = settings)

    def close(self):
        cef.Shutdown()