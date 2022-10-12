#installing required packages
import requests
from bs4 import BeautifulSoup
import csv

#getting the page html using requests
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)

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

#getting a book title ! TODO check if i need two lines – experiment but remember about readability
booktitle = soup.h1.string
#booktitle = bs_title.string

#getting a book description ! TODO remove " ...more"?
bs_desc = soup.find_all("p")
desc = bs_desc[3]
description = desc.string

#getting category
bs_cat = soup.find_all("a")
cat = bs_cat[3]
category = cat.string

#getting review rating
bs_ratings = soup.find_all("p", class_="star-rating")
rating = []
for rat in bs_ratings:
    rat_list = rat["class"]
    rating.append(rat_list[1])



print(rating)

#getting image url --> TODO replace "../../" with real part of the url
imgs = soup.find_all("img")
imgurl=[]
for img in imgs:
    imgurl.append(img["src"])


##creating a csv and writing data from headers and contents list
#creating headers list
headers = ["product_page_url", "universal_ product_code (upc)", "book_title", "price_including_tax", "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating", "image_url"]

#opening a new file to write
with open('result.csv', 'w', encoding="utf-8", newline='') as csvfile:
    #creating a writer object with the file
    writer = csv.writer(csvfile, delimiter='=')
    writer.writerow(headers)
    #writing data to a row
    for i in range(len(headers)):
        #creating a new row with the title and description at that point in the loop
        row = [url, upc, booktitle, pricetax, pricenotax, quantity, description, category, rating, imgurl]
        writer.writerow(row)


#reading the csv to make sure everything is correct
#with open('result.csv') as file:
#    reader = csv.reader(file, delimiter=',')
#    for row in reader:
#        print(row)

