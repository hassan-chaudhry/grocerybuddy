# Import Modules
import requests
from bs4 import BeautifulSoup

# Store URl of Whole Foods website
wholefoods_url = "https://www.wholefoodsmarket.com/products/all-products"

# Get HTML Code
page = requests.get(wholefoods_url)
source_code = page.text
soup = BeautifulSoup(page.content, "html.parser") 

# Get Grocery Stock
id_results = soup.find(id="main-content") # narrow down id
results = id_results.find_all("img")  # narrow down class

stock = []

for item in results:
    stock.append(item.get('alt', '')) # add items to stock list

# print(stock) 

# Get item from user
user_item = input("Enter the item you would like to buy: ").title()

# Check if user item is in stock 
item_in_stock = False
if user_item in stock:
     print(user_item, "is in stock at Whole Foods!") # in stock
     print()
     item_in_stock = True

if item_in_stock == False:
    print("Sorry,", user_item, "is not in stock!") # not in stock
    print()
    

