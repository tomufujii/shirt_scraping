import csv, codecs, cStringIO
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

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

    counter = 0;
    maxNum = 2
    for item in shirt_data:
        # only one want to preview 1 shirt
        if counter <= maxNum:
            shirt_name = item.find_all("li", {"id", "arrayProdName"})[0].text
            shirt_img = item.find_all("img")[0]["src"]
            shirt_page = item.find_all("a")[0]["href"]
            print shirt_name
            print shirt_img
            print shirt_page
            get_shirt_details(shirt_page)
            counter += 1
        else:
            break

        # itemWriter.writerow([shirt_name, shirt_img])

    #To download an image, you can use the urllib.request module

def get_shirt_details(url):
    r2 = requests.get(url)
    soup2 = BeautifulSoup(r2.content)
    print soup2.prettify()

    # print soup2

    # get shirt description
    # product_details = soup2.find("div", {"class": "product-detail-container"})


    # shirt_desc = product_details.find("p", class_="notranslate").text
    # print shirt_desc

    # # get technical details
    # tech_details = product_details.find("ul", class_="tech-details")
    # shit_tech_details = ""
    # counter = 0
    # for detail in tech_details.descendants:
    #     if isinstance(detail, NavigableString):
    #         if unicode(detail).strip() != "":
    #             print unicode(detail).strip()
    #             if counter == 0:
    #                shirt_tech_details = unicode(detail).strip()
    #             else:
    #                 shirt_tech_details = shirt_tech_details + " | " + unicode(detail).strip()
    #             counter += 1
    # print shirt_tech_details

    # # get fit
    # size_and_fit = product_details.find("div", class_="sizefit_desc")
    # shirt_fit = size_and_fit.find("li")
    # print shirt_fit.text
    

    # print product_details.prettify()
    # # reg_or_tall = product_details.find_all(class_="product-details_variant")
    # # for input in reg_or_tall:
    # #     print input


# get_shirts("https://www.jcrew.com/mens_category/dressshirts.jsp")
get_shirt_details("https://www.jcrew.com/mens_category/dressshirts/ludlowdress/PRD~99467/99467.jsp?color_name=fairweather-blue")