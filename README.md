# truefilm 

This repository outline the pipeline used to extract specific field from an xml wikipedia file dump and a csv containing movies metadata. 

The pipeline is automatized but the user needs to run few commands through the Terminal. The assumption is that the use has a MacOS and thus the pipeline was configured using this system. 

# How-to
The process uses pre-configured python scripts to generate all the steps of the process. The first Python script initialize the Python environment and installs all the libraries needed. (NOTE: the $ indicates the terminal prompt and shouldn't be copied as part of the command line)

1. Create a new project folder 
2. In Terminal, run "$ git clone git@github.com:manfredimiraula/truefilm.git"
  - This copies the files within the Git repository locally and allow to start the process. 
3. Download the data files within the folder where you cloned the repository
  - https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz
  - https://www.kaggle.com/rounakbanik/the-movies-dataset/version/7#movies_metadata.csv
  
This is the folder structure you should have at this point:
.
+-- project_folder
|   + file.py
|   + file.csv
|   + file.xml.gz

The scripts and the data files needs to be in the same folder in order for the scripts to read correctly

4. From terminal run the script "1_package_install.sh"
  - $ sh 1_package_install.sh
5. From terminal run the script "2_truefilm-extract-xml-from-gz.py"
  - $ python3 2_truefilm-extract-xml-from-gz.py
6. From terminal run the script "3_truefilm-transformation-pipeline.py"
  - python3 3_truefilm-transformation-pipeline.py
7. From terminal run the script "4_xml-title-extract.py"
  - python3 4_xml-title-extract.py
8. From terminal run the script "5_db-init.sh"
  - $ sh 5_db-init.sh
9. At this point we need to initialize the user for our Postgres databse. the shell script started the postgres service for you, insert the following command when prompted
  - $ CREATE ROLE truer WITH LOGIN PASSWORD 'filmaker';
  - $ ALTER ROLE truer CREATEDB;
  - $ \q 
9. From terminal run the script "6_load-to-postgres.py"
  - python3 6_load-to-postgres.py

At this point we completed the extraction, transformation and load of the data into the Postgres DB in the table true_film in the public schema. 

# Access the data
To query the data we have multiple options. Depending on the type of work to be done on the data, we might want to use different tools. Below I recommend installing PgADmin4 as an interactive and easy to use GUI interface to query the data. 

## Install PgAdmin4 to query through the web interface

Install PgAdmin4 
- Downaload the latest package from here https://www.pgadmin.org/download/pgadmin-4-macos/
- Once installed, configure the server using the following parameters
- username: truer
- password: filmaker
- database: postgres
- host: localhost 
- port: 5432


To access the data you can use the following query to start exploring the data
"
SELECT 
  * 
 FROM 
  public.true_film
"

# ETL Analysis and Data EDA
The full analysis on the data and approach end to end used for the ETL is described in more details in the file "eda-truefilm-etl-end-to-end.jpynb"

# Overall approach and Tool used 
The challenge asked to produce an ETL pipeline, starting from some downloaded data. The pipeline should be automated and reproducible. 

Given these premises, I approached the task thinking about the complexity of the scripts used. I wanted to make the process simple enough that it could be processed by another machine through few scripts. Also, I opted for simple Python libraries that shouldn't create problems during installation through the Terminal. 

- For data manipulation I used Pandas and the library lxml to parse the XML file. 
- To connect to the Postgres DB I used psycopg2 and SQLAlchemy. I feel the two are interchangeable. 

# Algorithmic approach
I didn't use a specific algorithmic approach and this is the bottleneck of the entire process. The slowest point of the pipeline is the parse of the XML file and the search for the tags of interest. 

This approach leads to an algorithm of type O^n. Since the XML file contains more than 6M+ rows, reproducing the step for each tag over this file cost a lot in terms of time and processing power. To improve this bottleneck we could: 
- split the XML file in smaller chunks and process them independently using the Python library multiprocessing which should improve the performance by initializing multiple processes over the chunks at the same time
- use PySpark to distribute the processing to multiple nodes. With more time, I'd try to implement this approach to parse directly the entire XML into a pandas dataframe using the Python library "pandas_read_xml" that allow to copy directly from an XML file given the Elements to be copied are known. 


