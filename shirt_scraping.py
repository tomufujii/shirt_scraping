import csv, codecs, cStringIO
import requests
from bs4 import BeautifulSoup

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def get_shirts(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)

    shirt_data = soup.find_all("td", {"class": "arrayProdCell"})

    #Open csv file
    #For each shirt, write shirt name and image path in two separate column
    with open("test.csv", "wb") as c:
	    itemWriter = UnicodeWriter(c)
	    for item in shirt_data:
		    shirt_name = item.find_all("li", {"id", "arrayProdName"})[0].text
		    shirt_img = item.find_all("img")[0]["src"]
            shirt_page = item.find_all("a")[0]["href"]
            print shirt_name
            print shirt_img
            print shirt_page
            get_shirt_details(shirt_page)

            # itemWriter.writerow([shirt_name, shirt_img])

    c.close()

    #To download an image, you can use the urllib.request module

def get_shirt_details(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)

    shirt_color = soup.find("div", {"id", "color_title"}).[0].text
    print shirt_color

get_shirts("https://www.jcrew.com/mens_category/dressshirts.jsp")