from tkinter import Widget
import kivy
import pandas as pd

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.core.window import Window

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp

from PIL import Image
from pytesseract import pytesseract

import requests
from bs4 import BeautifulSoup

# store products
wholefoods_products = {"Organic Honeycrisp Apple": "4.45", "Organic Large Hass Avocados": "5.00", "Large Hass Avocados": "4.00", "Organic Broccoli": "2.99", "Medium Hass Avocado": "0.99", "Honeycrisp Apples": "3.29", "Organic Blueberries Pint": "5.99", "Organic Green Asparagus": "4.39", "Organic Fuji Apples": "2.99", "Organic Raspberries": "7.99", "Organic Grade A Whole Milk, 1 gallon": "6.99", "Full Fat Oat Milk, 64 fl oz": "5.99", "Organic Large Brown Eggs, 24 oz": "5.79", "Large Eggs, 36 oz": "8.79"}
walmart_products = {"Lightly Dried Organic Parsley": "0.35", "Organic Bananas": "1.42", "Organic Baby Peeled Carrots": "1.56", "Organic Grape Tomato": "2.66", "Organic Bagged Avocados": "4.98", "Fresh Organic Mini Cucumbers": "3.46", "Organic Baby Spinach": "2.98", "Organic Spring Mix": "4.98", "Envy Apples": "1.36", "Gala Apples": "0.84", "a2 Milk Whole Milk": "3.97", "Great Value Whole Vitamin D Milk, Gallon, 128 fl oz": "$4.37", "Deans TruMoo 1% Low Fat Chocolate Milk, Gallon, 128 fl oz": "5.37", "Great Value Large White Eggs, 12 Count": "2.82", "Great Value Large White Eggs, 18 Count":"4.12"}

class MainWidget(Screen):
    pass


class SecondWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass

class ThirdWindow(Screen):
    pass


class FourthWindow(Screen):
    def pressSBP(self):
        user_product = self.ids.userInputSBP.text # product that user searches for 

        productInStore = "" # products in stores that are similar to the one searched for
        displayWFHeader = True
        displayNPFWF = True # if no products found in Whole Foods
        displayWalHeader = True
        displayNPFWal = True # if no products found in Walmart
        
        for product in wholefoods_products: # Whole Foods Products
            if (user_product.lower() in product.lower()): 
                displayNPFWF = False
                if (displayWFHeader == True):
                        productInStore += "Whole Foods Products: \n"
                        displayWFHeader = False
                
                productInStore += product + ", $" + wholefoods_products.get(product) + "\n"
        productInStore += "\n"
        
        for product in walmart_products: # Walmart Products
            if (user_product.lower() in product.lower()): 
                displayNPFWal = False
                if (displayWalHeader == True):
                        productInStore += "Walmart Products: \n"
                        displayWalHeader = False

                productInStore += product + ", $" + walmart_products.get(product) + "\n"
        productInStore += "\n"

        if (displayNPFWF == True and displayNPFWal == True):
            productInStore = "No products found."
                    
        self.ids.itemSBP.text = productInStore
     
    pass

class FifthWindow(Screen):
    pass

class ScrollLabel(ScrollView):
    text = StringProperty("\n")
    pass

class SixthWindow(Screen):    
    def pressWF(self):
        # scroll view properties
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        #creating an empty pandas DataFrame to store all of the product data
        wholefoodsDF = pd.DataFrame()
        
        #creating column for the item names
        wholefoodsDF["Items"] = []
        global stockWF 
        stockWF = []

        # go through each item and append to stock
        for product in wholefoods_products:
            stockWF.append(product)
    
        # adding the stock to the dataframe
        wholefoodsDF["Items"] = stockWF # add items to dataframe
        stockWF = "\n".join(stockWF)
        #check if item in stock       
        user_product = self.ids.userInputWF.text

        if user_product.lower() in stockWF.lower():
            self.ids.productInWFStock.text = user_product + " are available at Whole Foods! The product is priced at $" + wholefoods_products.get(user_product) + "."
        else:
            self.ids.productInWFStock.text = "Our records indicate that " + user_product + " are currently unavailable at Whole Foods."
    pass

class SeventhWindow(Screen):     
    def pressWal(self):
        # scroll view properties
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        #creating an empty pandas DataFrame to store all of the product data
        walmartDF = pd.DataFrame()
        
        #creating column for the item names
        walmartDF["Items"] = []
        global stockWal
        stockWal = []

        # go through each item and append to stock
        for product in walmart_products:
            stockWal.append(product)
    
        # adding the stock to the dataframe
        walmartDF["Items"] = stockWal # add items to dataframe
        stockWal = "\n".join(stockWal)

        #check if item in stock       
        user_product = self.ids.userInputWal.text

        if user_product.lower() in stockWal.lower():
            self.ids.productInWalStock.text = user_product + " are available at Walmart! The product is priced at $" + walmart_products.get(user_product) + "."
        else:
            self.ids.productInWalStock.text = "Our records indicate that " + user_product + " are currently unavailable at Walmart."
    pass

class EighthWindow(Screen):
    def add_datatable(self):
        resultList = list(walmart_products.items())
        table = MDDataTable(
            use_pagination=True,
            size_hint=(1, .5),
            column_data=[
                ("Product Name", dp(70)),
                ("Price", dp(70)),
            ],
            row_data=resultList
        )
        self.add_widget(table)
    pass

class NinthWindow(Screen):
    def add_datatable(self):
        resultList = list(wholefoods_products.items())
        table = MDDataTable(
            use_pagination=True,
            size_hint=(1, .5),
            column_data=[
                ("Product Name", dp(70)),
                ("Price", dp(70)),
            ],
            row_data=resultList
        )
        self.add_widget(table)
    pass

class TenthWindow(Screen):
    filePath = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_dropfile=self._on_file_drop)

    def reduced_image(self):
        print(self.filePath)

    def _on_file_drop(self, window, file_path):
        print(file_path)
        self.filePath = file_path.decode("utf-8") # convert byte to string
        self.ids.receipt.source = self.filePath
        self.ids.receipt.reload()  
    pass

class EleventhWindow(Screen):
    def pressReceipt(self):
        filePath = '/Users/hassanchaudhry/Desktop/receipt1.jpg'
        path_to_tesseract = r'/usr/local/bin/tesseract'
        pytesseract.tesseract_cmd = path_to_tesseract
        img = Image.open(filePath)
        self.ids.checkReceiptInput.text = str(pytesseract.image_to_string(img))
    pass

kv = Builder.load_file("my.kv")

class MyMainApp(MDApp):
    def build(self):
        return kv
        

if __name__ == "__main__":
    MyMainApp().run()

