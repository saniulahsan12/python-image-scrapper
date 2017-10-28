from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
from urllib.request import Request, urlopen
import requests
import shutil
# import queue
from bs4 import BeautifulSoup
import os

class MainWindow(Tk):

    def __init__(self):

        Tk.__init__(self)

        self.title("Image Scrapper")
        self.geometry("300x250")
        self.resizable(False, False)

        self.label  = Label(self, text="Enter URL")
        self.entry  = Entry(self, width="50")
        self.button = Button(self, text="Download Image", command=self.scrapSite)
        self.stats  = Label(self, text="Status")

        self.label.pack()
        self.entry.pack()
        self.button.pack()
        self.stats.pack()

    def scrapSite(self):
        get_url  = self.entry.get()
        counter  = 0
        dir_name = get_url.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        self.stats.config(text='Loading')

        if get_url == '':
            tkinter.messagebox.showinfo('Alert', 'Empty value not allowed')
        else:

            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            try:
                get_online_content = urlopen(Request(get_url, headers={'User-Agent': 'Mozilla/5.0'})).read(100000)
                soup = BeautifulSoup(get_online_content, 'html.parser')
                all_image = soup.findAll('img')

                for link in all_image:
                    file_name = link['src'].split('/')[-1]
                    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bpm', '.gif', '.ico')):
                        req = requests.get(link['src'], stream=True)
                        if req.status_code == 200:
                            with open(dir_name+'/'+file_name, 'wb') as file_downloaded:
                                req.raw.decode_content = True
                                shutil.copyfileobj(req.raw, file_downloaded)
                            counter = counter+1

                self.stats.config(text='Done')
                self.entry.config(text='')
                tkinter.messagebox.showinfo('Alert', str(counter)+' Image Downloaded successfully')

            except Exception:
                tkinter.messagebox.showinfo('Alert', 'There is a problem using this process')
                self.entry.config(text='')
                self.stats.config(text='Done')
        return

window = MainWindow()
window.mainloop()
