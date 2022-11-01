from tkinter import Widget
import kivy
import pandas as pd

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


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
        
        #removed this part for now becuase cannot obtain user input in the GUI yet
        '''# Get item from user
        user_item = input("Enter the item you would like to buy: ").title()

        # Check if user item is in stock 
        item_in_stock = False
        if user_item in stock:
            print(user_item, "is in stock at Whole Foods!") # in stock
            print()
            item_in_stock = True

        if item_in_stock == False:
            print("Sorry,", user_item, "is not in stock!") # not in stock
            print()''' 
    pass


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
