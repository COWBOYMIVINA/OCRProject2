#installing required packages
import requests
from bs4 import BeautifulSoup
import csv
import os

#making soup out of the main page of website to scrape
url = "http://books.toscrape.com/"
main_page = requests.get(url)

soup = BeautifulSoup(main_page.content, "html.parser")

#getting the list of book categories from main page
categories_list = []

for data in soup.find_all(class_="side_categories"):
    for a in data("a"):
        link = (a.get("href"))
        categories_list.append(link.replace("catalogue/", "http://books.toscrape.com/catalogue/"))

#removing the "All books" category from the list as having it will produce dupes
categories_list.remove("http://books.toscrape.com/catalogue/category/books_1/index.html")

#creating headers list
headers = ["product_page_url", "universal_ product_code (upc)", "book_title", "price_including_tax", "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating", "image_url"]

#getting the list of book categories from main page
categories_list = []

for data in soup.find_all(class_="side_categories"):
    for a in data("a"):
        link = (a.get("href"))
        categories_list.append(link.replace("catalogue/", "http://books.toscrape.com/catalogue/"))

#removing the "All books" category from the list as having it will produce dupes
categories_list.remove("http://books.toscrape.com/catalogue/category/books_1/index.html")

#creating a directory for each category and putting an output csv file inside
for cat_link in categories_list:
    cat_url = requests.get(cat_link)
    soup = BeautifulSoup(cat_url.content, "html.parser")
    cat_name = soup.find(class_="active")
    cat_list_name = cat_name.string
    #creating a directory named after the category of the book
    os.makedirs(f"c:/bookstoscrape/{cat_list_name}/", exist_ok=True)
    #creating the output csv file and writing headers while making sure it's utf8-friendly
    with open(f"c:/bookstoscrape/{cat_list_name}/{cat_list_name}.csv", "a", encoding="utf-8", newline='') as csvfile:
    #creating a writer object with the file
        writer = csv.writer(csvfile)
        writer.writerow(headers)
    csvfile.close

#creating a list of links to each separate book
links = []

#populating the list of links by going into each category and finding books links
for category_link in categories_list:
    #getting the category html and making the soup out of it
    page = requests.get(category_link)
    soup = BeautifulSoup(page.content, "html.parser")

    #books links can be identified by the h3 tag in the html – this tag isn't used for anything else but the book links
    for data in soup.find_all("h3"):
        for a in data:
            link = (a.get('href'))
            links.append(link.replace("../../../", "http://books.toscrape.com/catalogue/"))
    
    #making sure that categories with two or more pages of books are parsed correctly. the biggest category has 8 pages.
    #creating a list of link to 2+ category pages if they exist
    pages = []    
    
    #getting the number of pages from category html by getting the number of books per category, dividing it by 20 (numberof books per category and adding 1 in case there will be lest than 20 books on the last page)
    number_of_books = soup.find(class_="form-horizontal").contents[3].string
    page_number = int(number_of_books)//20 + (int(number_of_books) % 20 > 0)
    if page_number > 1:
        extra_pages = list(range(2,page_number+1))
        for number in extra_pages:
            pages.append(category_link.replace("index.html", f"page-{number}.html"))
  
           
    #if a category has two or more pages, they will be parsed for book links which will be added to the "links" list
    for page in pages:
        nextpage = requests.get(page)
        soup = BeautifulSoup(nextpage.content, "html.parser")
        for data in soup.find_all("h3"):
            for a in data:
                link = (a.get('href'))
                links.append(link.replace("../../../", "http://books.toscrape.com/catalogue/"))


#extracting and writing information from the book pages
for book_link in links:
    #getting the page html using requests
    page = requests.get(book_link)

    #transforming html into a soup object 
    soup = BeautifulSoup(page.content, "html.parser")

    #creating a contents list from the text inside <td>: some required information is stored in a table, which can be identified by the td tag
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
    category = bs_cat[3].string
    
    #getting review rating
    bs_ratings = soup.find("p", class_="star-rating").get("class")
    rating = bs_ratings[1]

    #getting image url
    imgurl = soup.find_all("img")[0].get("src").replace("../../", "http://books.toscrape.com/")

    #saving the img file
    filename = os.path.split(imgurl)[1]
    r = requests.get(imgurl, stream=True)
    if r.status_code == 200:
        with open(f"c:/bookstoscrape/{category}/{filename}.jpg", 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        f.close
        
    #adding gathered info to the csv
    with open(f"c:/bookstoscrape/{category}/{category}.csv", "a", encoding="utf-8") as csvfile:
    #creating a writer object with the file
        writer = csv.writer(csvfile, lineterminator='\n')
        row = [book_link, upc, booktitle, pricetax, pricenotax, quantity, description, category, rating, imgurl]
        writer.writerow(row)
    csvfile.close