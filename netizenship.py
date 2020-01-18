#!/usr/bin/python3
"""Tool to automatically check the membership of a given username
in popular websites. 


Inspired by: https://github.com/thelinuxchoice/userrecon/blob/master/userrecon.sh

MIT License

Copyright (c) 2020 Rahul Raj
"""

import requests
from termcolor import colored
from time import sleep
from bs4 import BeautifulSoup
import concurrent.futures
from pyfiglet import figlet_format
import eventlet

global websites
websites = {
    'Facebook': 'https://www.facebook.com/',
    'Twitter': 'https://twitter.com/',
    'Instagram': 'https://www.instagram.com/',
    'Youtube': 'https://www.youtube.com/user/',
    'Reddit': 'https://www.reddit.com/user/',
    'PInterest': 'https://www.pinterest.com/',
    'Flickr': 'https://www.flickr.com/people/',
    'Vimeo': 'https://vimeo.com/',
    'Soundcloud': 'https://soundcloud.com/',
    'Disqus': 'https://disqus.com/',
    'Medium': 'https://medium.com/',
    'AboutMe': 'https://about.me/',
    'Imgur': 'https://imgur.com/user/',
    'Flipboard': 'https://flipboard.com/',
    'Slideshare': 'https://slideshare.net/',
    'Spotify': 'https://open.spotify.com/user/',
    'Scribd': 'https://www.scribd.com/',
    'Patreon': 'https://www.patreon.com/',
    'BitBucket': 'https://bitbucket.org/',
    'GitLab': 'https://gitlab.com/',
    'Github': 'https://www.github.com/',
    'GoodReads': 'https://www.goodreads.com/',
    'Instructable': 'https://www.instructables.com/member/',
    'CodeAcademy': 'https://www.codecademy.com/',
    'Gravatar': 'https://en.gravatar.com/',
    'Pastebin': 'https://pastebin.com/u/',
    'FourSquare': 'https://foursquare.com/',
    'TripAdvisor': 'https://tripadvisor.com/members/',
    'Wikipedia': 'https://www.wikipedia.org/wiki/User:',
    'HackerNews': 'https://news.ycombinator.com/user?id=',
    'CodeMentor': 'https://www.codementor.io/',
    'Trip': 'https://www.trip.skyscanner.com/user/',
    'Blogger': '.blogspot.com',
    'Wordpress': '.wordpress.com',
    'Tumbler': '.tumblr.com',
    'Deviantart': '.deviantart.com"',
    'LiveJournel': '.livejournal.com',
    'Slack': '.slack.com',

}

def get_website_membership(site):
    global uname
    global websites
    url = websites[site]
    if not url[:1]=='h':
        link = 'https://'+uname+url
    else:
        link = url+uname
    state = "FAIL"
    
    try:
        # with eventlet.Timeout(20):
        response = requests.get(link)
        tag = soup.find(id=response.status_code)
        msg = tag.find_parent('dt').text
        response.raise_for_status()
        
    except:
        print(site.rjust(width), ':', colored(state.ljust(width//2), 'red') , '(Status:', msg, ')')
    
    else:
        state = 'SUCCESS'
        print(site.rjust(width), ':', colored(state.ljust(width//2), 'green'), '(Status:', msg, ')')


def banner(text, ch='=', length=78):
    spaced_text = ' %s ' % text
    banner = spaced_text.center(length, ch)
    print(banner)

ascii_banner = figlet_format('Netizenship')
print(ascii_banner)
banner_text = "MIT License, Copyright (c) 2020 Rahul Raj"
banner(banner_text)


status_code_html = 'https://en.wikipedia.org/wiki/List_of_HTTP_status_codes'
global uname 
uname = input("Enter the username: ")
width = 15

page = requests.get(status_code_html)
soup = BeautifulSoup(page.content, 'html.parser')

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     executor.map(get_website_membership, list(websites.keys()))

for site in list(websites.keys()):
    try:
        get_website_membership(site)
    except:
        pass