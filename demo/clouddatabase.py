from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import update

# initialize parameters
INSTANCE_CONNECTION_NAME = f"grocerybuddy-370504:us-central1:grocery-buddy"
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "GroceryBuddy"
DB_PASS = "GroceryBuddy7!"
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
        db=DB_NAME,
    )
    return conn

# create connection pool with 'creator' argument to connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# connect to connection pool
with pool.connect() as db_conn:
  # create table in database
  # db_conn.execute(
  #     "CREATE TABLE IF NOT EXISTS gb_database" 
  #     "( id SERIAL NOT NULL, store VARCHAR(255) NOT NULL, "
  #     "product VARCHAR(255) NOT NULL, price FLOAT NOT NULL, "
  #     "PRIMARY KEY (id));"
  #)

  # get table object
  metaData = sqlalchemy.MetaData()
  gb_database = sqlalchemy.Table('gb_database', metaData, autoload=True, autoload_with=pool)

  # insert data into table
  insert_database = sqlalchemy.text(
      "INSERT INTO gb_database (store, product, price) VALUES (:store, :product, :price)",
  )

  # to insert new data: stores, products, and prices [EXAMPLE BELOW: insert "Organic Large Brown Eggs, 24 oz" for "5.79"]
  #db_conn.execute(insert_database, store="wholefoods, product="Organic Large Brown Eggs, 24 oz", price="5.79")

  # to update data [EXAMPLE BELOW: update price for "Organic Large Hass Avocados" to "5.00"]
  # query = sqlalchemy.update(gb_database).values(price="5.00").where(gb_database.columns.product=="Organic Large Hass Avocados") 
  # db_conn.execute(query)

  # get table results
  results = db_conn.execute("SELECT * FROM gb_database").fetchall()

  # show results
  for row in results:
    print(row)
