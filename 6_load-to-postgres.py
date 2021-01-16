# Owner: Manfredi Miraula
# Date created: Jan 16 2021
# The script initialize the table that will receive the data extracted
# the postgres database is initialized, using the following role
# user: truer, pwd: filmaker, db: postgres, host: localhost, port: 5432

# import libraries
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

# create a connection with the database, we use psycopg2 to create the table
try:
    conn = psycopg2.connect(database = "postgres", user = "truer", password = "filmaker", host = "localhost", port = "5432")
except:
    print("I am unable to connect to the database") 

# we initialize the table with the format we need 
cur = conn.cursor()
try:
    cur.execute("""
    DROP TABLE IF EXISTS true_film;
    CREATE TABLE IF NOT EXISTS true_film
	(
        id SERIAL NOT NULL, 
        
        title varchar(255),
        
        budget bigint,

		year date,
        
        revenue numeric, 
        
        ratio numeric, 
        
        rating numeric, 

        production_company text,
        
        abstract text,
        
        url varchar(255), 

		created_at timestamp without time zone NOT NULL DEFAULT NOW(),
    	updated_at timestamp without time zone DEFAULT NULL,
    	CONSTRAINT true_film_key PRIMARY KEY (id)

		)
	WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE true_film
    OWNER to truer;

CREATE INDEX true_film_title ON true_film(title, production_company, ratio, revenue);""")
except:
    print("I can't drop our test database!")

conn.commit() # <--- makes sure the change is shown in the database
conn.close()
cur.close()

# we load the extracted and transformed data
df = pd.read_csv('pre-load.csv')

# we use sqlalchemy to load the data to Postgres
engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/postgres' \
    .format('truer', # username
            'filmaker', # password
            'localhost', # host
            '5432' # local port
           ) 
    , echo=False)

# we load into Postgres table created
df.to_sql('true_film', engine, if_exists = 'append', index = False,
               chunksize = 1000, method = 'multi')
