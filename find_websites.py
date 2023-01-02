# python3 find_websites.py
#
# This code takes your Google API KEY plus your Google Custom Search engine, 
# and returns the results of the Google Search. The basic concept is that we 
# will grab 1 page of Google results (10 results), and process those results 
# to see if any are likely to contain the Events that we are looking for.
#
# Your own API KEY and Search Engine ID should be stored in two files by 
# themselves, one level above this project.
#
# Below from: https://www.thepythoncode.com/article/use-google-custom-search-engine-api-in-python


import os
import requests

import extract_test_events #EJ file



# Get proper directories:
path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))

# get the API KEY here: https://developers.google.com/custom-search/v1/overview
api_file = open(parent_path + "/API_KEY", 'r')
API_KEY = api_file.readline().strip()
api_file.close()
print("API_KEY: " + API_KEY)

# get your Search Engine ID on your CSE control panel
search_engine_id_file = open(parent_path + "/ProgrammableSearchEngineID", 'r')
SEARCH_ENGINE_ID = search_engine_id_file.readline().strip()
search_engine_id_file.close()
print("Search Engine ID: " + SEARCH_ENGINE_ID)

# get your search city names from file
city_names_file = open(parent_path + "/Data/CitiesList/cities_list.tsv", 'r')
a_line_list = city_names_file.readline().strip().split()
city = a_line_list[0].lower()
county = a_line_list[1].lower()
state = a_line_list[2].lower()
a_city_and_state = city + '+' + state
print("Query: " + a_city_and_state)

# get your search keyphrases from file
keyphrases_file = open(parent_path + "/Data/KeyphrasesList/keyphrases.tsv", 'r')
a_keyphrase = keyphrases_file.readline().strip().replace(' ', '+')
print("Keyphrase: " + a_keyphrase)


# the search query you want
query = a_city_and_state + '+' + a_keyphrase
# using the first page (10 results)
page = 1
# constructing the URL
# doc: https://developers.google.com/custom-search/v1/using_rest
# calculating start, (page=2) => (start=11), (page=3) => (start=21)
start = (page - 1) * 10 + 1
url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"

print('URL: ' + str(url))

# make the API request
data = requests.get(url).json()


# get the result items
search_items = data.get("items")

"""
# iterate over 10 results found
for i, search_item in enumerate(search_items, start=1):
    try:
        long_description = search_item["pagemap"]["metatags"][0]["og:description"]
    except KeyError:
        long_description = "N/A"
    # get the page title
    title = search_item.get("title")
    # page snippet
    snippet = search_item.get("snippet")
    # alternatively, you can get the HTML snippet (bolded keywords)
    html_snippet = search_item.get("htmlSnippet")
    # extract the page url
    link = search_item.get("link")
    # print the results
    print("="*10, f"Result #{i+start-1}", "="*10)
    print("Title:", title)
    print("Description:", snippet)
    print("Long description:", long_description)
    print("URL:", link, "\n")
"""

# iterate over 10 results found
print("All URLs: ")
for i, search_item in enumerate(search_items, start=1):
    # extract the page url
    link = search_item.get("link")
    print("#"+str(i)+" " + str(link))
    
# identify the urls with city words
print("Our target URLs: ")
good_url = ""
for i, search_item in enumerate(search_items, start=1):
    # extract the page url
    link = search_item.get("link")
    if city in link or county in link:
    	print("#"+str(i)+" " + str(link))
    	if good_url == "":
    		good_url = link
    
# Peek at the html for one of these good sites:
a_html = requests.get(good_url).text
#print(str(a_html))
    
# Try extracting events
tsv_file = open(parent_path + "/Data/ExtractedEvents/test_events.tsv", 'w')
extract_test_events.get_events_from_a_string(str(a_html), good_url, a_city_and_state, tsv_file)
    

