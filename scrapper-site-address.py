from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from urllib.request import Request, urlopen
import requests
import shutil
from bs4 import BeautifulSoup
import os

class MainWindow(Tk):

    def __init__(self):

        Tk.__init__(self)

        self.title("Dummy Product Seeder")
        self.geometry("800x600")
        self.resizable(False, False)

        self.label  = Label(self, text="Enter URL")
        self.scrolledtext = ScrolledText(self, width="500")
        self.button = Button(self, text="Download Products and Images", command=self.scrapSite)
        self.stats  = Label(self, text="Status")

        self.label.pack()
        self.scrolledtext.pack()
        self.button.pack()
        self.stats.pack()

    def scrapSite(self):
        scrolltext = self.scrolledtext.get(1.0,END).splitlines()
        for single_link in scrolltext:
            get_url = single_link
            dataset  = {}
            dir_name = get_url.rsplit('/', 1)[-1]
            self.stats.config(text='Loading')

            if get_url == '':
                tkinter.messagebox.showinfo('Alert', 'Empty value not allowed')
            else:

                if not os.path.exists("images"):
                    os.makedirs("images")

                if not os.path.exists("lookups"):
                    os.makedirs("lookups")

                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)

                try:
                    get_online_content = urlopen(Request(get_url, headers={'User-Agent': 'Mozilla/5.0'})).read(100000)
                    soup = BeautifulSoup(get_online_content, 'html.parser')

                    #title Download
                    dataset['title'] = dir_name

                    #model Download
                    dataset['model'] = soup.select('h3')[2].text.strip('Item Name: ')

                    #model Download
                    dataset['price'] = soup.select('h2.product_price')[0].text.strip().replace(':',',').replace(' ','')

                    # #description Download
                    dataset['description'] = soup.select('div#Description')[0].text.strip()


                    #cateegory Download
                    dataset['category'] = soup.select('h1.product-title')[0].text.strip()

                    #color Download
                    dataset['color'] = soup.select('ul.list-unstyled li')[2].text.strip('Color : ')

                    #color Download
                    dataset['wood'] = soup.select('ul.list-unstyled li')[0].text.strip('Material : ')

                    # #delivery Download
                    dataset['delivery'] = soup.select('ul.list-unstyled li')[5].text.strip('Delivery Times : ')

                    # image Download
                    dataset['image_link'] = soup.findAll('img')[2]['src']
                    dataset['image'] = dataset['image_link'].split('/')[-1]

                    #entity adding so append
                    with open("lookups/category.txt", "a") as myfile:
                        myfile.write(dataset['category'])
                        myfile.write("\n")

                    with open("lookups/color.txt", "a") as myfile:
                        myfile.write(dataset['color'])
                        myfile.write("\n")

                    with open("lookups/wood.txt", "a") as myfile:
                        myfile.write(dataset['wood'])
                        myfile.write("\n")

                    # data adding so overwrite
                    with open(dir_name+"/title.txt", "w") as myfile:
                        myfile.write(dataset['title'])
                        myfile.write("\n")

                    with open(dir_name+"/image.txt", "w") as myfile:
                        myfile.write(dataset['image'])
                        myfile.write("\n")

                    with open(dir_name+"/price.txt", "w") as myfile:
                        myfile.write(dataset['price'])
                        myfile.write("\n")

                    with open(dir_name+"/description.txt", "w") as myfile:
                        myfile.write(dataset['description'])
                        myfile.write("\n")

                    with open(dir_name+"/delivery.txt", "w") as myfile:
                        myfile.write(dataset['delivery'])
                        myfile.write("\n")

                    with open(dir_name+"/category.txt", "w") as myfile:
                        myfile.write(dataset['category'])
                        myfile.write("\n")

                    with open(dir_name+"/color.txt", "w") as myfile:
                        myfile.write(dataset['color'])
                        myfile.write("\n")

                    with open(dir_name+"/wood.txt", "w") as myfile:
                        myfile.write(dataset['wood'])
                        myfile.write("\n")

                    #image download
                    file_name = dataset['image']
                    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bpm', '.gif', '.ico')):
                        req = requests.get(dataset['image_link'], stream=True)
                        if req.status_code == 200:
                            with open('images/'+file_name, 'wb') as file_downloaded:
                                req.raw.decode_content = True
                                shutil.copyfileobj(req.raw, file_downloaded)
                                self.stats.config(text=file_name)


                except Exception as e:
                    print(e)

        self.stats  = Label(self, text="Process Finished.")
        return

window = MainWindow()
window.mainloop()
