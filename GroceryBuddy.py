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

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp

import requests
from bs4 import BeautifulSoup

# store products
wholefoods_products = {"Organic Honeycrisp Apple": "4.45", "Organic Large Hass Avocados": "5.00", "Large Hass Avocados": "4.00", "Organic Broccoli": "2.99", "Medium Hass Avocado": "0.99", "Honeycrisp Apples": "3.29", "Organic Blueberries Pint": "5.99", "Organic Green Asparagus": "4.39", "Organic Fuji Apples": "2.99", "Organic Raspberries": "7.99"}
walmart_products = {"Lightly Dried Organic Parsley": "0.35", "Organic Bananas": "1.42", "Organic Baby Peeled Carrots": "1.56", "Organic Grape Tomato": "2.66", "Organic Bagged Avocados": "4.98", "Fresh Organic Mini Cucumbers": "3.46", "Organic Baby Spinach": "2.98", "Organic Spring Mix": "4.98", "Envy Apples": "1.36", "Gala Apples": "0.84"}

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
                
                productInStore += str(product) + ", $" + str(wholefoods_products.get(product)) + "\n"
        productInStore += "\n"
        
        for product in walmart_products: # Walmart Products
            if (user_product.lower() in product.lower()): 
                displayNPFWal = False
                if (displayWalHeader == True):
                        productInStore += "Walmart Products: \n"
                        displayWalHeader = False

                productInStore += str(product) + ", $" + str(walmart_products.get(product)) + "\n"
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
    def WholeFoods(self):
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
        return (str(stockWF))
    
    def pressWF(self):
        #check if item in stock       
        user_product = self.ids.userInputWF.text

        if user_product.lower() in stockWF.lower():
            self.ids.productInWFStock.text = user_product + " are available! The product is priced at $" + str(wholefoods_products.get(user_product))
        else:
            self.ids.productInWFStock.text = "Our records indicate that " + user_product + " are currently unavailable."
    
    def add_datatable(self):
        resultList = list(wholefoods_products.items())
        table = MDDataTable(
            size_hint=(0.9, 0.8),
            column_data=[
                ("Product Name", dp(60)),
                ("Price", dp(60)),
            ],
            row_data=resultList
        )
        self.add_widget(table)
    pass

class SeventhWindow(Screen):    
    def Walmart(self):
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
        return (str(stockWal))
    
    def pressWal(self):
        #check if item in stock       
        user_product = self.ids.userInputWal.text

        if user_product.lower() in stockWal.lower():
            self.ids.productInWalStock.text = user_product + " are available! The product is priced at $" + str(walmart_products.get(user_product))
        else:
            self.ids.productInWalStock.text = "Our records indicate that " + user_product + " are currently unavailable."
    
    def add_datatable(self):
        resultList = list(walmart_products.items())
        table = MDDataTable(
            size_hint=(0.9, 0.8),
            column_data=[
                ("Product Name", dp(60)),
                ("Price", dp(60)),
            ],
            row_data=resultList
        )
        self.add_widget(table)
    pass


kv = Builder.load_file("my.kv")


class MyMainApp(MDApp):
    def build(self):
        return kv
        

if __name__ == "__main__":
    MyMainApp().run()
