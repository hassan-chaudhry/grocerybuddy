from google.cloud.sql.connector import Connector
import sqlalchemy

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
        db=DB_NAME
    )
    return conn

# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# connect to connection pool
with pool.connect() as db_conn:
  # create ratings table in our movies database
  db_conn.execute(
      "CREATE TABLE IF NOT EXISTS gb_database "
      "( id SERIAL NOT NULL, store VARCHAR(255) NOT NULL, "
      "product VARCHAR(255) NOT NULL, price FLOAT NOT NULL, "
      "PRIMARY KEY (id));"
  )

 # insert data into our ratings table
  insert_stmt = sqlalchemy.text(
      "INSERT INTO gb_database (store, product, price) VALUES (:store, :product, :price)",
  )

 # query and fetch ratings table
  results = db_conn.execute("SELECT * FROM gb_database").fetchall()

  # show results
  for row in results:
    print(row)
