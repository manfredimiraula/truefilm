# Owner: Manfredi Miraula
# Date created: Jan 16 2021
# The script ingest two csv containing Wikipedia abstracts and movie media metadata
# Transform the data in the final format we want to ingest into a Postgres databse


# import lib
import pandas as pd
import sys


# import wikipedia-latest-abstract.csv
wiki_df = pd.read_csv('wikipedia-latest-abstract.csv')

# remove the wikipedia pattern from the title string
wiki_df['title'] = wiki_df['title'].map(lambda x: x.lstrip('Wikipedia: '))
print('wiki_df is ready for merging')

# load media csv
media_df = pd.read_csv('movies_metadata.csv')

# transform the column values with text in integer 
mask = media_df[media_df['budget'].str.isnumeric() == False].index
media_df.loc[mask,'budget'] = 0

# convert column type to int
media_df['budget'] = media_df['budget'].astype(int)

# transform the populatity column into a float excluding string types
media_df['popularity'] = pd.to_numeric(media_df['popularity'],errors='coerce').astype(float)

# we check the amount of entries we carry over by applying these masks
median_budget = media_df[media_df['budget'] > 0]['budget'].median()
median_revenue = media_df[media_df['revenue'] > 0]['revenue'].median()

media_df = media_df[(media_df['budget'] >= median_budget) & (media_df['revenue'] > median_revenue)]

# we create the ratio column
media_df['ratio'] = media_df['budget']/media_df['revenue']

# subsetting to columns of interest
media_df = media_df[['original_title', 'title', 'budget', 'release_date', 'revenue', 'ratio','popularity', 'production_companies']]

# keep only the duplicates where the release_date is different
media_df = media_df.drop_duplicates(subset=['release_date','title'], keep='first')

# order by the ratio value and take the first 1000 entries. This reduces the data to join
media_df = media_df.sort_values('ratio', ascending = False).head(1000)

print('media_df is ready for merging')

# left merge to join the two dataset
temp = media_df.merge(wiki_df, how = 'left', on = 'title')

# subsetting and renaming
final_df = temp[['title', 'budget', 'release_date', 'revenue', 'ratio','popularity', 'production_companies', 'abstract', 'url']]

# by joining we inserted some additional duplication. We can remove it by ordering by ratio and taking the first 1000 entries
final_df = final_df.sort_values('ratio', ascending = False).head(1000)

final_df.rename(columns = {
    'original_title':'title', 
    'optimized_budget':'budget', 
    'release_date': 'year', 
    'popularity':'rating', 
    'production_companies': 'production_company'}, inplace = True)

# storing csv before loading into Postgres
final_df.to_csv('pre-load.csv', index = False)
print('the number of rows stored are ' + str(len(final_df)))
print('final df is stored')


sys.exit('process complete')

