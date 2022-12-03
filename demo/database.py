import mysql.connector

# connect to database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="GroceryBuddy7!",
  database="mydatabase"
)

mycursor = mydb.cursor()

# select "stock" table
mycursor.execute("SELECT * FROM stock")
myresult = mycursor.fetchall()

# print results in table
for x in myresult:
  print(x)
