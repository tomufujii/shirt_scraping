import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

# input is the jcrew dress shirts page
# goes to every shirt and rtrieves the name, image url, and shirt url
# then calls get_shirt_details to visit the shirt page to retrieve further data

def get_shirts(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)

    # retrieve each shirt grid
    shirts = soup.find_all("td", {"class": "arrayProdCell"})

    # the counter and maxNum variables are only used to limit items for testing
    counter = 0;
    maxNum = 2
    for shirt in shirts:
        if counter < maxNum:
            shirt_name = shirt.find_all("li", {"id", "arrayProdName"})[0].text
            shirt_img = shirt.find_all("img")[0]["src"]
            shirt_page = shirt.find_all("a")[0]["href"]
            #print to console for testing
            print shirt_name
            print shirt_img
            print shirt_page
            # visit the shirt page to retrieve further data
            get_shirt_details(shirt_page)
            counter += 1
        else:
            break

# input is the shirt page url
# used to capture shirt details, such as description, technical details, etc.

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
# get_shirt_details("https://www.jcrew.com/mens_category/dressshirts/ludlowdress/PRD~99467/99467.jsp?color_name=fairweather-blue")