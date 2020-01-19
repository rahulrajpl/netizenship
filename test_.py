"""This is a test script to check the landing page for broken urls
which is returning a 200 OK response.
"""

import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/user?id=sdsrgsdfg2222"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# print(soup)

# print ('----------------------')

# print((soup.find_all('div','ProfileMeta-user')))

if 'No such user.' in soup:
    print("Page Not Found")