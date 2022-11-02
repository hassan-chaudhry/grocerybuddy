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

import requests
from bs4 import BeautifulSoup


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

class FifthWindow(Screen):
    def demo(self):
        # Store URl of Whole Foods website
        wholefoods_url = "https://www.wholefoodsmarket.com/products/all-products"

        # Get HTML Code
        page = requests.get(wholefoods_url)
        source_code = page.text
        soup = BeautifulSoup(page.content, "html.parser") 

        # Get Grocery Stock
        id_results = soup.find(id="main-content") # narrow down id
        results = id_results.find_all("img")  # narrow down class

        #creating an empty pandas DataFrame to store all of the product data
        wholefoodsDF = pd.DataFrame()
        
        #creating column for the item names
        wholefoodsDF["Items"] = []
        stock = []

        #go through each item and add its name to a temporary list that we will append to the dataframe
        for item in results:
            temp = str(item.get('alt', ''))
            stock.append(temp)
    
        #adding the stock to the dataframe
        wholefoodsDF["Items"] = stock # add items to dataframe
        return(str(wholefoodsDF))

    def press(self):
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

        #go through each item and add its name to a temporary list that we will append to the dataframe
        for item in results:
            temp = str(item.get('alt', ''))
            stock.append(temp)

        #check if item in stock       
        item = self.ids.userInput.text

        if item in stock:
            self.ids.itemInStock.text = item + " in stock!"
        else:
            self.ids.itemInStock.text = item + " not in stock!"
    pass


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
