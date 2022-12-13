#######################
#                     # 
#    GROCERY BUDDY    #
#                     #
#######################

##############
#  MODULES   #
##############

#  kivy modules for GUI
import kivy
from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.lang.builder import Builder

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

# panda module for data tables
from tkinter import Widget
import pandas as pd
import numpy as np

# SQL and Google Cloud to connect to database
import sqlalchemy
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.orm import relationship, sessionmaker
from google.cloud.sql.connector import Connector

# request and json modules for reading receipts
import requests
import json

############################
#  CLOUD DATABASE ACCESS   #
############################

# initialize parameters
INSTANCE_CONNECTION_NAME = f"grocerybuddy-370504:us-central1:grocery-buddy"
DB_USER = "GroceryBuddy"
DB_PASS = "GroceryBuddyPass7"
DB_NAME = "grocery_buddy_database"

# initialize Connector object
connector = Connector()

# function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn

# create connection pool with 'creator' argument to connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# initialize session
Session = sessionmaker(bind=pool)
session = Session()

# connect to connection pool
with pool.connect() as db_conn:

    # database table layout: id = store[0], stores = database[1], products = database[2], prices = database[3]
    database = db_conn.execute("SELECT * FROM gb_database").fetchall()
    
    # get stores from database
    db_stores = db_conn.execute("SELECT store FROM gb_database").fetchall()
    stores = [] # convert to list
    for store in db_stores:
        store = str(store)
        store = store.replace("('", "")
        store = store.replace("',)", "")
        stores.append(store)
    
    stores = [*set(stores)] # for data tables
    
    # get products from database
    db_products = db_conn.execute("SELECT product FROM gb_database").fetchall()
    products = [] # convert to list
    for product in db_products:
        product = str(product)
        product = product.replace("('", "")
        product = product.replace("',)", "")
        products.append(product)

##############
#  SCREENS   #
##############

class MainWidget(Screen):
    pass

class ScrollLabel(ScrollView):
    text = StringProperty("\n")
    pass

class WindowManager(ScreenManager):
    pass

class OptionsWindow(Screen):
    pass

class MyListWindow(Screen):
    pass

class ViewMyList(Screen):
# view items in grocery list
    def updateMyList(self):
        with open("itemname.txt", "r") as fobj:
            self.ids.itemlistlabel.text = fobj.read()

    def clearMyList(self):
        open("itemname.txt", "w").close()
    pass

class EditListWindow(Screen):
# add item to grocery list
    itemname_text_input = ObjectProperty()
    ego = NumericProperty(0)
    itemname = StringProperty('')

    def submit_itemname(self):
        self.itemname = self.itemname_text_input.text
        self.save()
        self.itemname = ''

    def save(self):
        with open("itemname.txt", "a") as fobj:
            fobj.write(str("\n"+self.itemname))
    pass

class SBPWindow(Screen):
# search for product in all stores
    def pressSBP(self): # "Submit" button - searches databse for user's product
        user_product = self.ids.userInputSBP.text  # product that user searches for

        resultProducts = ""  # products in stores that are similar to the one searched for by user
        noProductsFound = 1 # keeps track of whether or not products are found in database that are similar to the one searched for by user
        
        for prod in products:
            if user_product.lower() in prod.lower(): # if product found
                
                with pool.connect() as db_conn:

                    # get table object
                    metaData = sqlalchemy.MetaData()
                    gb_database = sqlalchemy.Table('gb_database', metaData, autoload=True, autoload_with=pool)
                    
                    # access database 
                    temp = session.query(gb_database).filter_by(product=prod).first()
                    
                    # get store name
                    store_name = temp.store
                    store_name = str(store_name)

                    # get product price
                    prod_price = temp.price
                    prod_price = str(prod_price)

                resultProducts += store_name + ": " + prod + ", $" + prod_price + "\n" # list store, product, and price
                noProductsFound = 0
        
        if noProductsFound == 1: # if no products found 
            resultProducts = "No products found."

        self.ids.itemSBP.text = resultProducts
    pass

    def backSBP(self): # "Go Back" button - clears current screen's text fields and goes back to "Options" screen
        self.ids.userInputSBP.text = ""
        self.ids.itemSBP.text = ""

class SBSWindow(Screen):
# browse through products by store
    def getStores(self):
        return stores
    
    def spinner_clicked(self, value):
        value = "'"+value+"'"
        with pool.connect() as db_conn:
            storeItems = db_conn.execute("SELECT product FROM gb_database WHERE store={}".format(value)).fetchall()
            itemPrices = db_conn.execute("SELECT price FROM gb_database WHERE store={}".format(value)).fetchall()
        
        products = [] # convert to list
        for product in storeItems:
            product = str(product)
            product = product.replace("('", "")
            product = product.replace("',)", "")
            products.append(product)
            
        prices = [] # convert to list
        for price in itemPrices:
            price = str(price)
            price = price[1:-2]
            price = "$" + price
            prices.append(price)
        
        resultList = []
        counter=0
        for x in products:
            resultList.append(x)
            resultList.append(prices[counter])
            counter += 1 
    
        resultList2 = np.array(resultList).reshape(-1,2)
        
        table = MDDataTable(
            use_pagination=True,
            pos_hint = {'center_x': 0.5, 'center_y':0.5},
            size_hint=(.9, .6),
            column_data=[
                ("Product Name", dp(70)),
                ("Price", dp(30)),
            ],
            row_data=resultList2
        )
        self.add_widget(table)
    pass

class AddReceiptWindow(Screen):
# drag & drop receipt
    filePath = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_dropfile=self._on_file_drop)

    def reduced_image(self): # fit on screen
        print(self.filePath)

    def _on_file_drop(self, window, file_path): # drag & drop
        print(file_path)
        self.filePath = file_path.decode("utf-8") # read file path
        self.ids.receipt.source = self.filePath
        self.ids.receipt.reload() # reload screen with image
    pass

class CheckReceiptWindow(Screen):
# read data from receipt
    def pressReceipt(self): # "Check Results" button - reads and prints receipt
 
        # use API to read data from receipt
        # receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt' # Receipt OCR API endpoint
        # imageFile = self.manager.get_screen("AddReceipt").ids.receipt.source # get file path from TenthWindow

        # # access API and get receipt results as JSON file
        # receiptData = requests.post(receiptOcrEndpoint, data = {
        #     'api_key': 'TEST',          # Use 'TEST' for testing purpose
        #     'recognizer': 'US',         # can be 'US', 'CA', 'JP', 'SG' or 'auto'
        #     'ref_no': 'ocr_python_123', # optional caller provided ref code
        #  },
        # files = {"file": open(imageFile, "rb")})

        # # returns JSON object as a dictionary
        # receiptDic = json.loads(receiptData.text, strict=False)

        # use in place of API for demo purposes to limit API requests
        filePath = "/Users/hassanchaudhry/Desktop/receipt.text" # replace with path to receipt.text
        receiptData = open(filePath, "r")
        receiptDic = json.loads(receiptData.read(), strict=False)

        # iterate through receipt and print: store name, store address, products, prices
        printReceipt = ""
        for receipt in receiptDic['receipts']:
                store_name = "" + str(receipt['merchant_name']) + " at " + str(receipt['merchant_address'])
                printReceipt += "Store: " + store_name + "\n \n"
                for item in receipt['items']:
                        store_product = str(item['description'])
                        store_price = str(item['amount'])
                        printReceipt += store_product + ",  $" + store_price + "\n"

        self.ids.checkReceiptInput.text = printReceipt # print receipt to text field

    def submitReceipt(self): # "Submit" button - uploads receipt info to database
        # connect to connection pool
        with pool.connect() as db_conn:

            # get table object
            metaData = sqlalchemy.MetaData()
            gb_database = sqlalchemy.Table('gb_database', metaData, autoload=True, autoload_with=pool)

            # get info from printReceipt
            receiptPrinted = self.manager.get_screen("CheckReceipt").ids.checkReceiptInput.text # get file path from TenthWindow

            receiptLines = receiptPrinted.split("\n") # split receipt info into lines
            store_name = receiptLines[0] # first line of receipt info is store name 
            store_name = store_name.replace("Store: ", "") # remove substring to get store name only

            for i in range(2, len(receiptLines)-1): # iterate trhough lines of products in receipt info
                if (receiptLines[i]): # account for change in size of list by user
                    receiptLine = receiptLines[i].split(",") # for each line, split into product and price
                    store_product = receiptLine[0] # first part is product name
                    store_price = receiptLine[1] # second part is product price
                    store_price = store_price.replace(" $", "") # remove substirng to get only product price
                    store_price = store_price.strip() # remove white spaces in product price
            
                # update database if necessary
                if store_name in stores: # if store in database
                    if store_product in products: # if product in database
                        
                        # get price of product 
                        temp = session.query(gb_database).filter_by(product=store_product).first()
                        curr_price = temp.price
                        curr_price = str(curr_price)

                        if store_price != curr_price: # if price is different than one in database
                            # update price
                            query = sqlalchemy.update(gb_database).where(gb_database.columns.store==store_name, gb_database.columns.product==store_product).values(price=store_price)
                            db_conn.execute(query)
                            session.commit()
                            # update "sales" page
                            self.manager.get_screen("Sales").ids.salesText.text += store_name + ": \n" + store_product + " changed in price from " + curr_price + " to " + store_price + "\n"
                    else: # if product not in database
                        # add product and price to database
                        query = sqlalchemy.insert(gb_database).values(store=store_name, product=store_product, price=store_price)
                        db_conn.execute(query)
                        session.commit()
                else: # if store and/or product not in database
                    # add store, product, and price to database
                    query = sqlalchemy.insert(gb_database).values(store=store_name, product=store_product, price=store_price)
                    db_conn.execute(query)
                    session.commit()

        # reset receupt input
        self.ids.checkReceiptInput.text = ""

        # update lists
        App.get_running_app().update()
    pass

class SalesWindow(Screen):
# show sales and general price changes of products
    def clearSales(self): # ""Clear All Sales"" - clears all price changes on page
        self.ids.salesText.text = ""
    pass

####################################
#  BUILD KIVY FILE  & RUN PROGRAM  #
####################################

kv = Builder.load_file("my.kv")

class MyMainApp(MDApp):
    def build(self): # build kivy 
        return kv
    def update(self): # update lists after database has been updated
        # connect to connection pool
        with pool.connect() as db_conn:
            # get stores from database
            db_stores = db_conn.execute("SELECT store FROM gb_database").fetchall()
            stores = [] # convert to list
            for store in db_stores:
                store = str(store)
                store = store.replace("('", "")
                store = store.replace("',)", "")
                stores.append(store)

            # get products from database
            db_products = db_conn.execute("SELECT product FROM gb_database").fetchall()
            products = [] # convert to list
            for product in db_products:
                product = str(product)
                product = product.replace("('", "")
                product = product.replace("',)", "")
                products.append(product)

if __name__ == "__main__": 
    MyMainApp().run()
