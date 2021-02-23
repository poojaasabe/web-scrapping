import requests # for making standard html requests
from bs4 import BeautifulSoup # magical tool for parsing html data
import json # for parsing data
from pandas import DataFrame as df # premier library for data organization


#requesting data
page = requests.get("https://locations.familydollar.com/id/")
soup = BeautifulSoup(page.text, 'html.parser')

#page.text() for text (most common)
#page.content() for byte-by-byte output
#page.json() for JSON objects
#page.raw() for the raw socket response (no thank you)

#print(soup.prettify()) #view the entire source code

#get the address information using href tag

dollar_tree_list = soup.find_all('href')


dollar_tree_list = soup.find_all(class_ = 'itemlist')
type(dollar_tree_list)
len(dollar_tree_list)

for i in dollar_tree_list:
  print(i)

#The content from this BeautifulSoup "ResultSet" can be extracted using .contents
example = dollar_tree_list[2] # a representative example
example_content = example.contents
print(example_content)

#Use .attr to find what attributes are present in the contents of this object.


#print("using attribute")
#example_content = example.contents[0]
#example_content.attrs
#example_href = example_content['href']
#print(example_href)


city_hrefs = [] # initialise empty list

for i in dollar_tree_list:
    cont = i.contents[0]
    href = cont['href']
    city_hrefs.append(href)

#  check to be sure all went well
for i in city_hrefs[:2]:
  print(i)

#page2 = requests.get(city_hrefs[2]) # again establish a representative example
#soup2 = BeautifulSoup(page2.text, 'html.parser')
#arco = soup2.find_all(type="application/ld+json")
#print(arco[1].contents[0])

locs_dict = [] # initialise empty list

for link in city_hrefs:
  locpage = requests.get(link)   # request page info
  locsoup = BeautifulSoup(locpage.text, 'html.parser')
      # parse the page's content
  locinfo = locsoup.find_all(type="application/ld+json")
      # extract specific element
  loccont = locinfo[1].contents[0]
      # get contents from the bs4 element set
  locjson = json.loads(loccont)  # convert to json
  locaddr = locjson['address'] # get address
  locs_dict.append(locaddr) # add address to list


#convert to a pandas data frame, drop the unneeded columns "@type" and "country")

locs_df = df.from_record(locs_dict)

locs_df.drop(['@type', 'addressCountry'], axis = 1, inplace = True)
locs_df.head(n = 5)

df.to_csv(locs_df, "family_dollar_ID_locations.csv", sep = ",", index = False)