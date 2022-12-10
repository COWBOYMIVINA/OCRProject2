This script is used for scraping the book info from https://books.toscrape.com/.

It uses the following packages:
bs4
requests
csv
os

In order to create a virtual environment, use the following commands in Windows PowerShell:
python -m venv venv
venv\Scripts\activate

Running the script.py will create a "bookstoscrape" folder in your C:\ drive, if it doesn't exist yet.
It will also create a subfolder for each book category and will populate it with book covers in JPG format and a CSV file containing the information for each book in a given category.

It takes about 10-20 minutes to complete scraping.

IMPORTANT: running script.py consecutively will APPEND the book information to the CSVs each time it's being run. If you need to get fresh info, delete "bookstoscrape" folder before running the script.
