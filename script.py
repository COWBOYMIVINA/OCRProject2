#installing required packages
import requests
from bs4 import BeautifulSoup
import csv

#creating a csv and writing data from headers and contents list
#creating headers list
headers = ["product_page_url", "universal_ product_code (upc)", "book_title", "price_including_tax", "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating", "image_url"]

#creating the csv file and writing headers
with open('result.csv', 'w', encoding="utf-8", newline='') as csvfile:
    #creating a writer object with the file
    writer = csv.writer(csvfile)
    writer.writerow(headers)

#url of the website to scrape
url = "http://books.toscrape.com/"
main_page = requests.get(url)

soup = BeautifulSoup(main_page.content, "html.parser")

#getting the list of categories from main page
categories_list = []

for data in soup.find_all(class_="side_categories"):
    for a in data("a"):
        link = (a.get('href'))
        categories_list.append(link.replace("catalogue/", "http://books.toscrape.com/catalogue/"))

#removing the All books category from the list as we don't need it
categories_list.remove("http://books.toscrape.com/catalogue/category/books_1/index.html")

#creating a list of links to each separate book
links = []

for category_link in categories_list:
    #getting the cat html using requests
    page = requests.get(category_link)

    #transforming html into a soup object 
    soup = BeautifulSoup(page.content, "html.parser")

    #explain h3 in the comment and why exactly i did it like this
    for data in soup.find_all("h3"):
     for a in data:
        link = (a.get('href'))
        links.append(link.replace("../../../", "http://books.toscrape.com/catalogue/"))

    pages = []
    pages.append(category_link)
    pages.append(category_link.replace("index.html", "page-2.html")) 
    pages.append(category_link.replace("index.html", "page-3.html"))
    pages.append(category_link.replace("index.html", "page-4.html"))
    pages.append(category_link.replace("index.html", "page-5.html"))
    pages.append(category_link.replace("index.html", "page-6.html"))
    pages.append(category_link.replace("index.html", "page-7.html"))
    pages.append(category_link.replace("index.html", "page-8.html"))

    for i in pages:
        nextpage = requests.get(i)
        print(i)
        soup = BeautifulSoup(nextpage.content, "html.parser")
        for data in soup.find_all("h3"):
            for a in data:
                link = (a.get('href'))
                links.append(link.replace("../../../", "http://books.toscrape.com/catalogue/"))   


#extracting and writing information from separate book pages
for book_link in links:
    #getting the page html using requests
    page = requests.get(book_link)

    #transforming html into a soup object 
    soup = BeautifulSoup(page.content, "html.parser")

    #creating a contents list from the text inside <td>
    bs_contents = soup.find_all("td")

    contents = []
    for content in bs_contents:
        contents.append(content.string)

    #getting UPC
    upc = contents[0]

    #getting price with tax
    pricetax = contents[2]

    #getting price excluding tax
    pricenotax = contents[3]

    #getting quantity
    quantity = contents[5]

    #getting a book title 
    bs_title = soup.h1.string
    booktitle = bs_title

    #getting a book description 
    bs_desc = soup.find_all("p")
   
    desc = bs_desc[3]
    description = desc.string

    #getting category
    bs_cat = soup.find_all("a")
    cat = bs_cat[3]
    category = cat.string

    #getting review rating
    bs_ratings = soup.find("p", class_="star-rating").get("class")
    rating = bs_ratings[1]

    #getting image url
    imgurl = soup.find_all("img")[0].get("src").replace("../../", "http://books.toscrape.com/")

    #adding gathered info to the csv
    with open('result.csv', 'a', encoding="utf-8") as csvfile:
    #creating a writer object with the file
        writer = csv.writer(csvfile, lineterminator='\n')
        row = [book_link, upc, booktitle, pricetax, pricenotax, quantity, description, category, rating, imgurl]
        writer.writerow(row)

with open('result.csv', encoding="utf-8") as f:
  data = list(csv.reader(f))
  new_data = [a for i, a in enumerate(data) if a not in data[:i]]
  with open('result.csv', 'w', encoding="utf-8") as t:
     write = csv.writer(t, lineterminator='\n')
     write.writerows(new_data)