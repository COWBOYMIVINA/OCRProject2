#installing required packages
import requests
from bs4 import BeautifulSoup
import csv

#getting the page html using requests
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)

#transforming html into a soup object 
soup = BeautifulSoup(page.content, "html.parser")

#creating a headers list
bs_heads = soup.find_all("th")

heads = []
for head in bs_heads:
    heads.append(head.string)


#creating a contents list
bs_contents = soup.find_all("td")

contents = []
for content in bs_contents:
    contents.append(content.string)


#creating a csv and writing data from headers and contents list

#creating an empty headers list
headers = []

#opening a new file to write
with open('result.csv', 'w', encoding="utf-8", newline='') as csvfile:
    #creating a writer object with the file
    writer = csv.writer(csvfile, delimiter='=')
    writer.writerow(headers)
    #looping through each element in headers and contents list
    for i in range(len(heads)):
        #creating a new row with the title and description at that point in the loop
        row = [heads[i], contents[i]]
        writer.writerow(row)


#reading the csv to make sure everything is correct
with open('result.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        print(row)