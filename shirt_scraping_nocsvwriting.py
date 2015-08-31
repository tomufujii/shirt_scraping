import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

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

def get_shirt_details(url):
    r2 = requests.get(url)
    soup2 = BeautifulSoup(r2.content)

    # get shirt description
    product_details = soup2.find("div", {"class": "product-detail-container"})
    shirt_desc = product_details.find("p", class_="notranslate").text
    print shirt_desc

    # get technical details
    tech_details = product_details.find("ul", class_="tech-details")
    shit_tech_details = ""
    counter = 0
    for detail in tech_details.descendants:
        if isinstance(detail, NavigableString):
            if unicode(detail).strip() != "":
                print unicode(detail).strip()
                if counter == 0:
                   shirt_tech_details = unicode(detail).strip()
                else:
                    shirt_tech_details = shirt_tech_details + " | " + unicode(detail).strip()
                counter += 1
    print shirt_tech_details

    # get fit
    size_and_fit = product_details.find("div", class_="sizefit_desc")
    shirt_fit = size_and_fit.find("li")
    print shirt_fit.text
    

get_shirts("https://www.jcrew.com/mens_category/dressshirts.jsp")
get_shirt_details("https://www.jcrew.com/mens_category/dressshirts/ludlowdress/PRD~99467/99467.jsp?color_name=fairweather-blue")