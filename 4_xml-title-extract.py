# Owner: Manfredi Miraula
# Date created: Jan 16 2021
# The script takes the file enwiki-latest-abstract.xml and parse the following tags
# "title", "url", "abstract" into a dataframe. the dataframe is stored into a csv for later use

# import lib
from lxml import etree
import pandas as pd
import sys

# parse the xml
tree = etree.parse('enwiki-latest-abstract.xml')
root = tree.getroot()

print('xml parsed correctly')

def append(title):
    """This function uses etree method to extract the text from specific tag
    We will use it to map the xml and extract the content of the tags
    """
    return title.text

# here we use the lxml method to find all tags within the root with and iterate over the doc
titles = list(map(append, root.findall('.//title', namespaces=root.nsmap)))

print('Titles extracted')

# here we use the lxml method to find all tags within the root with and iterate over the doc
urls = list(map(append, root.findall('.//url', namespaces=root.nsmap)))

print('Urls extracted')

# here we use the lxml method to find all tags within the root with and iterate over the doc
abstracts = list(map(append, root.findall('.//abstract', namespaces=root.nsmap)))

print('Abstracts extracted')

# we generate a dataframe of the dataset
df = pd.DataFrame()

df['title'] = titles
df['url'] = urls
df['abstract'] = abstracts

df.to_csv('wikipedia-latest-abstract.csv', index = False)

print('XML stored in csv')

sys.exit('Process executed and closed')

