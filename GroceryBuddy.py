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

import requests
from bs4 import BeautifulSoup

# store products
walmart_products = {"Lightly Dried Organic Parsley": 0.35, "Organic Bananas": 1.42, "Organic Baby Peeled Carrots": 1.56, "Organic Grape Tomato": 2.66, "Organic Bagged Avocados": 4.98, "Fresh ORganic Mini Cucumbers": 3.46, "Organic Baby Spinach": 2.98, "Organic Spring Mix": 4.98, "Envy Apples": 1.36, "Gala Apples": 0.84}
wholefoods_products = {"Organic Honeycrisp Apple": 4.449, "Organic Large Hass Avocados": 5, "Large Hass Avocados": 4, "Organic Broccoli": 2.99, "Medium Hass Avocado": 0.99, "Honeycrisp Apples": 3.29, "Organic Blueberries Pint": 5.99, "Organic Green Asparagus": 4.39, "Organic Fuji Apples": 2.99, "Organic Raspberries": 7.99}

class MainWidget(Screen):
    pass


class SecondWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass

class ThirdWindow(Screen):
    pass


class FourthWindow(Screen):
    pass

class ScrollLabel(ScrollView):
    text = StringProperty("\n")
    pass

class FifthWindow(Screen):    
    def WholeFoods(self):
	
	    # scroll view properties
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        #creating an empty pandas DataFrame to store all of the product data
        wholefoodsDF = pd.DataFrame()
        
        #creating column for the item names
        wholefoodsDF["Items"] = []
        global stock 
        stock = []

        #go through each item and add its name to a temporary list that we will append to the dataframe
        for products in wholefoods_products:
            stock.append(products)
    
        #adding the stock to the dataframe
        wholefoodsDF["Items"] = stock # add items to dataframe
        stock = "\n".join(stock)
        return (str(stock))
    
    def press(self):
        #check if item in stock       
        user_product = self.ids.userInput.text

        if user_product in stock:
            self.ids.itemInStock.text = user_product + " in stock!"
        else:
            self.ids.itemInStock.text = user_product + " not in stock!"
    pass


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv
        

if __name__ == "__main__":
    MyMainApp().run()
