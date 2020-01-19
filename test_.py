"""This is a test script to check the landing page for broken urls
which is returning a 200 OK response.
"""

import requests
from bs4 import BeautifulSoup

url = "https://www.reddit.com/user/rahulrajpl1111"
headers = {'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36'}

response = requests.(url , headers=headers   )
soup = BeautifulSoup(response.content, 'html.parser')

print(soup.prettify())
# print(response.status_code)

# print ('----------------------')

# print(soup.find_all('div',{'class':'_3VTI5BOpJO70xoBKSqz3O9'}))
# print(soup.find_all('h3'))

# if 'The person may have been banned' in soup.text:
#     print("Page Not Found")