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


url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
books_category = requests.get(url)

soup = BeautifulSoup(books_category.content, "html.parser")

links = []
#explain h3 in the comment and why exactly i did it like this
for data in soup.find_all("h3"):
    for a in data.find_all("a"):
        link = (a.get('href'))
        links.append(link.replace("../../../", "http://books.toscrape.com/catalogue/"))

page2 = requests.get(url + "/page-2.html")
soup = BeautifulSoup(page2.content, "html.parser")
for data in soup.find_all("h3"):
    for a in data.find_all("a"):
        link = (a.get('href'))
        links.append(link.replace("../../../", "http://books.toscrape.com/catalogue/"))


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

    #getting review rating  ! todo - stopped working
    bs_ratings = soup.find_all("p", class_="star-rating")
    rating = []
    for rat in bs_ratings:
        rat_list = rat["class"]
        rating.append(rat_list[1])

    #getting image url
    imgurl = soup.find_all("img")[0].get('src').replace("../../", "http://books.toscrape.com/")

    
    #adding gathered info to the csv
    with open('result.csv', 'a', encoding="utf-8") as csvfile:
    #creating a writer object with the file
        writer = csv.writer(csvfile, lineterminator='\n')
        row = [book_link, upc, booktitle, pricetax, pricenotax, quantity, description, category, rating, imgurl]
        writer.writerow(row)
   

#reading the csv to make sure everything is correct
with open('result.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        print(row)