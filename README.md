# Grocery Buddy

Welcome to Grocery Buddy! Grocery Buddy is an application that will help users find the best stores, prices, and deals for all their grocery-related needs. The program uses receipts from users to add stores, products, and prices to a MySQL databse that is hosted on a Google Cloud server. The user can access the database in many ways. The functionality of the program will be outlined further in this file.

For an in-depth explanation on how to set up the program, please visit our "Running the Program" page on our Confluence wiki. **It is reccomended that you view this page**: https://grocerybuddy.atlassian.net/wiki/spaces/GROCERYBUD/pages/8945667/Running+the+Program

For more information about what each part of the program does, please visit the "How-to article" page on our Confluence wiki:
https://grocerybuddy.atlassian.net/wiki/spaces/GROCERYBUD/pages/229475/How-to+article

## Setting Up

### Virtual Environment

It is recommended that you create a virtual environment to run the program. This can be achieved by running the following commands:

'''
virtualenv kivy_venv --python=python3.10.4
'''
'''
source kivy_venv/bin/activate
'''
Note that you should have python installed before you create a virtual environment (see "Installing Modules" for more).

### Installing Modules

Here is a list of all the necessary modules for the program:
- Install Python: https://www.python.org/downloads/
- Install pip: https://pip.pypa.io/en/stable/installation/
- Install Pandas: pip install pandas
- Install KivyMD: pip install kivymd
- Install pymysql: pip install pymysql
- Install sqlalchemy: pip install sqlalchemy
- Install MySQL Driver: pip install mysql-connector-python
- Install Google Cloud: pip install google-cloud-storage
- Install SQL Connector: pip install "cloud-sql-python-connector[pymysql]"
- Install the gcloud CLI: https://cloud.google.com/sdk/docs/install

### Getting Authorized 

After installing "gcloud CLI," run the following command to log into an NYU email:
'''
gcloud auth login
'''
Only the developers of thr project and the TAs overlooking its development currently have access to the program.

### Running the Program

To run the program, download "GroceryBuddy.py" and "my.kv" and place them in the same directory as the one you created your virtual environment in. Then, you can run the following to start the program:
'''
python GroceryBuddy.py
'''
### Troubleshooting

If you have any issues with the set up, please check out the "Running the Program" page on our Confluence wiki linked above. Also, please feel free to reach out to the developers for help!

## How It Works

The program consists of 5 pages, each with a different function. Here is a breakdown of what each page does and how to use it.

### My List

The “My List” page allows the user to “View My List” and “Edit My List.” The “View My List” option allows the user to see all the items in their grocery list (which is saved in a text file in the same directory as the program). It also allows the user to clear their grocery list when they have finished using it. They can start a new one using the “Edit My List.” Speaking of which, the “Edit My List” option allows the user to add items to their Grocery List.

### Shop By Product 

The “Shop by Product” page allows the user to search the entire database for a product. After the user types in a product name, the program returns the store, product name, and price of all similar or matching products.

### Shop by Store

The “Shop by Store” page allows the user to browse the inventories of each store in the database and check their prices. 

### Add Receipt

The “Add Receipt” page allows the user to submit a receipt of grocery items in order to add them to the database. The receipt is read by the Asprise Receipt OCR API which returns a .json file. The file is then read and printed to the screen for the user to change. This is because we want the user to be able to modify any mistakes that the API may have made in translating the receipt data. After the user makes any intended changes, they submit the receipt which adds all products (along with the store names and prices) to the database if they aren’t already in there. 

### Sales 

The “Sales” page keeps track of any price changes for the user. If the user submits a receipt with a product (and store) that is already in the database but with a different price, that is considered a price change. The program prints the price change to the “Sales” page in the following format: ““. The user also has the option to “Clear All Sales” which makes sure they can delete the price change notifications after they see them.

