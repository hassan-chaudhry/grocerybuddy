from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete

# initialize parameters
INSTANCE_CONNECTION_NAME = f"grocerybuddy-370504:us-central1:grocery-buddy"
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
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

  # insert data into table - OLD
  # query = sqlalchemy.insert(gb_database).values(store="Whole Foods Market at 1095 6th Ave, New York, NY 10036, USA", product="SALTED CORN CHIPS", price="2.59")
  # db_conn.execute(query)

  # to update data [EXAMPLE BELOW: update price for "Organic Large Hass Avocados" to "5.00"]
  # query = sqlalchemy.update(gb_database).values(store="Walmart at 500 Bayonne Crossing Way, Bayonne, NJ 07002, USA").where(gb_database.columns.store=="Walmart") 
  # db_conn.execute(query)

  # get specific row results
  # wholefoodsproducts = db_conn.execute("SELECT * FROM gb_database WHERE store='whole_foods'").fetchall()

  # get specific coloum results 
  # products = db_conn.execute("SELECT product FROM gb_database").fetchall()
  # for prod in products:
  # 	 print(prod)

  # to delete data
  # query = sqlalchemy.delete(gb_database).where(gb_database.c.id == 97)
  # db_conn.execute(query)

  # get entire table results
  results = db_conn.execute("SELECT * FROM gb_database").fetchall()

  # show results
  for row in results:
        print(row)
