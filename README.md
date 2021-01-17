# truefilm 

This repository outline the pipeline used to extract specific field from an xml wikipedia file dump and a csv containing movies metadata. 

The pipeline is automatized but the user needs to run few commands through the Terminal. The assumption is that the use has a MacOS and thus the pipeline was configured using this system. 

# How-to
The process uses pre-configured python scripts to generate all the steps of the process. The first Python script initialize the Python environment and installs all the libraries needed. (NOTE: the $ indicates the terminal prompt and shouldn't be copied as part of the command line)

1. Create a new project folder 
2. In Terminal, run 
```"$ git clone git@github.com:manfredimiraula/truefilm.git"```
  - This copies the files within the Git repository locally and allow to start the process. 
3. Download the data files within the folder where you cloned the repository
  - https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz
  - https://www.kaggle.com/rounakbanik/the-movies-dataset/version/7#movies_metadata.csv
  
This is the folder structure you should have at this point:
```
.
+-- project_folder
|   + file.py
|   + file.csv
|   + file.xml.gz
```

The scripts and the data files needs to be in the same folder in order for the scripts to read correctly

4. From terminal run the script "1_package_install.sh"
```$ sh 1_package_install.sh```
5. From terminal run the script "2_truefilm-extract-xml-from-gz.py"
```$ python3 2_truefilm-extract-xml-from-gz.py```
6. From terminal run the script "3_truefilm-transformation-pipeline.py"
```python3 3_truefilm-transformation-pipeline.py```
7. From terminal run the script "4_xml-title-extract.py"
```python3 4_xml-title-extract.py```
8. From terminal run the script "5_db-init.sh"
```$ sh 5_db-init.sh```
9. At this point we need to initialize the user for our Postgres databse. the shell script started the postgres service for you, insert the following command when prompted
```
$ CREATE ROLE truer WITH LOGIN PASSWORD 'filmaker';
$ ALTER ROLE truer CREATEDB;
$ \q 
 ```
9. From terminal run the script "6_load-to-postgres.py"
```python3 6_load-to-postgres.py```

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
```
SELECT 
  * 
 FROM 
  public.true_film
```
NOTE: for testing purposes, I uploaded also the file "pre-load.csv". This file is used by the script "6_load-to-postgres.py" to load the Postgres db with the clean data. Since the extraction process takes roughly 1.30 hrs, I decided to have the final dataframe ready for inspection. 

# ETL Analysis and Data EDA
The full analysis on the data and approach end to end used for the ETL is described in more details in the file "eda-truefilm-etl-end-to-end.jpynb". There I explain the choices and the decisions made to transform the data. 

# Overall approach and Tool used 
The challenge asked to produce an ETL pipeline, starting from some downloaded data. The pipeline should be automated and reproducible. 

Given these premises, I approached the task thinking about the complexity of the scripts used. I wanted to make the process simple enough that it could be processed by another machine through few scripts. Also, I opted for simple Python libraries that shouldn't create problems during installation through the Terminal. 

- I used Python as the scripting language of choice for the transformation and load. Some shell scripting was usefull to prepare the environment and making sure that the packages I used could be installed ina new machine. 
- For data manipulation I used Pandas and the library lxml to parse the XML file. 
- To connect to the Postgres DB I used psycopg2 and SQLAlchemy. I feel the two are interchangeable. 

I'm comfortable with Python as I use it regularly. Moreover, python is a well-supported language with a wide community of users. This brings multiple advantages but the two key advantages that led me to use this language are: 

1. Wide community and forums where you can trouble shoot and self-serve is something breaks or if you need to do something new. Chances are, someone have already faced the same (or a similar) problem, thus you can leverage multiple experiences to solve the issue or improve your code. 
2. A wide variety of open source libraries to tackly multiple problems. For instance, Pandas is an open source library that is, in my opinion, the standard library to manage data using Python. The library is supported and used widely and it is optimized to handle data in an efficient way. 

On a side note, I learned to love Postgres SQL. In my past experiences I used AWS Redshift and Presto SQL. Both have their advantages. However, I experienced Postgres in the last year and I believe it is a great open source SQL language. In particular, the extensions available to the language (e.g. PostGIS to handle and manipulate Geospatial data) make it the language of choice if you have to manage a number of heterogeneous data. 

# Algorithmic approach
I didn't use a specific algorithmic approach and I realise that this is the bottleneck of the entire process. The slowest point of the pipeline is the parse of the XML file and the search for the tags of interest. 

This approach leads to an algorithm of type O^n. Since the XML file contains more than 6M+ rows, reproducing the step for each tag over this file cost a lot in terms of time and processing power. To improve this bottleneck we could: 
- split the XML file in smaller chunks and process them independently using the Python library multiprocessing which should improve the performance by initializing multiple processes over the chunks at the same time
- use PySpark to distribute the processing to multiple nodes. With more time, I'd try to implement this approach to parse directly the entire XML into a pandas dataframe using the Python library "pandas_read_xml" that allow to copy directly from an XML file given the Elements to be copied are known. 

# Testing for correctness
I did split the process in different .py files. This breaking points are not random, as I believe it would make sense to insert KPIs and checkpoints at those stages. For example: 
1. Assuming the pipeline has to be an ongoing process, it would make sense to store the raw data in a datalake (e.g. AWS S3 bucket) with the timestamp at which the data was scraped. As time passes, we should expect to see an increasing number of rows (i.e. it makes sense to me that the movie sector creates more and more movies over time). If we observe a lesser number of rows at a later point, when comparing the previous "snapshot" we should raise a flag to investigate if there is something wrong with the ingestion of the raw data. 
2. Part of the checks that I would like to introduce are outlined in the file "eda-truefilm-etl-end-to-end.jpynb". For example, checking for duplication is an important check we should always carry. However, I also realise that duplication of data sometime is acceptable (e.g. when two movies have the same title but different release_date), thus there should be allignment between technical and business stakeholders to really understand the goal of the data and how the data should ultimately be used to craft a piepeline that make it easier to query the data for the ultimate-user. 
3. I notices that some of the abstracts and URLs extracted form the wikipedia dump are inconsistent with movie titles. This makes sense since sometimes movie titles are similar to English (or other languages) words and composition of words. In order to have a cleaner output, we could think of implementing a simple NLP process by which we analyze the text in the abstract to take into account words that can be referred to the movie industry (e.g. produced, movie/film, actors, etc..). Currently we have some spurious data in the final database as some URLs refer to pages on Wikipedia that are not related to the movie title. With the data at hand I wasn't able to find a good way to parametrize the cleaning of those bits. 

# Known issues and next steps
1. Increase the efficiency of the XML parsing by implementing multiprocessing or using PySpark
2. Cleanse the wikipedia dump from spurious data
