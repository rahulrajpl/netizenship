#!/usr/bin/python3
"""
Tool to automatically check the membership of a given username
in popular websites.

Inspired by:
    https://github.com/thelinuxchoice/userrecon/blob/master/userrecon.sh

MIT License

Copyright (c) 2020 Rahul Raj
"""

import requests
from termcolor import colored
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
from pyfiglet import figlet_format
import json
import urllib.request


try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

from distutils.version import LooseVersion


def check_latest_version():
    name = 'netizenship'
    installed_version = LooseVersion(version(name))

    # fetch package metadata from PyPI
    pypi_url = f'https://pypi.org/pypi/{name}/json'
    response = urllib.request.urlopen(pypi_url).read().decode()
    latest_version = max(LooseVersion(s) for s in json.loads(response)['releases'].keys())
    print(f'Current version: {installed_version}')

    if not installed_version == latest_version:
        print(f'Version {latest_version} available. To continue using the '
              'tool, run "sudo pip3 install --upgrade netizenship"')
        exit()


def main():
    def banner(text, ch='=', length=78):
        spaced_text = ' %s ' % text
        banner = spaced_text.center(length, ch)
        print(banner)

    ascii_banner = figlet_format('Netizenship')
    print(ascii_banner)

    # Check the version status.
    check_latest_version()

    banner_text = "MIT License, Copyright (c) 2020 Rahul Raj"
    banner(banner_text)

    wiki_link = 'https://en.wikipedia.org/wiki/List_of_HTTP_status_codes'
    uname = input("Enter username: ")
    width = 15  # to pretty print
    global counter
    counter = 0  # to count no of success
    page = requests.get(wiki_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    user_agent = ('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130'
                  ' Mobile Safari/537.36')
    headers = {'user-agent': user_agent}

    def get_website_membership(site):

        def print_fail():
            print(site.rjust(width), ':', colored(state.ljust(width//2), 'red'), '(Status:', msg, ')')

        def print_success():
            print(site.rjust(width), ':', colored(state.ljust(width//2), 'green'), '(Status:', msg, ')')

        url = websites[site]
        global counter
        state = "FAIL"
        msg = '--exception--'

        if not url[:1] == 'h':
            link = 'https://'+uname+url
        else:
            link = url+uname

        try:
            if site == 'Youtube' or 'Twitter':
                response = requests.get(link)
            else:
                response = requests.get(link, headers=headers)
            tag = soup.find(id=response.status_code)
            msg = tag.find_parent('dt').text
            response.raise_for_status()

        except Exception:
            print_fail()

        else:
            res_soup = BeautifulSoup(response.content, 'html.parser')
            if site == 'Pastebin':
                if len(res_soup.find_all('h1')) == 0:
                    msg = 'broken URL'
                    print_fail()

                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()

            elif site == 'Wordpress':
                if 'doesn’t exist' or 'blocked' in res_soup:
                    msg = 'broken URL'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()

            # elif site == 'Imgur':
                # ToDo

            elif site == 'GitLab':
                if 'Sign in' in res_soup.title.text:
                    msg = 'broken URL'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
            elif site == 'HackerNews':
                if 'No such user.' in res_soup:
                    msg = 'No Such User!'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
            elif site == 'ProductHunt':
                if 'Page Not Found' in res_soup.text:
                    msg = 'No Such User!'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
            else:
                state = 'SUCCESS'
                counter += 1
                print_success()

    websites = {
        'Facebook': 'https://www.facebook.com/',
        'Twitter': 'https://twitter.com/',
        'Instagram': 'https://www.instagram.com/',
        'Youtube': 'https://www.youtube.com/user/',
        # 'Reddit': 'https://www.reddit.com/user/', To Do
        'ProductHunt': 'https://www.producthunt.com/@',
        'PInterest': 'https://www.pinterest.com/',
        'Flickr': 'https://www.flickr.com/people/',
        'Vimeo': 'https://vimeo.com/',
        'Soundcloud': 'https://soundcloud.com/',
        'Disqus': 'https://disqus.com/',
        'Medium': 'https://medium.com/@',
        'AboutMe': 'https://about.me/',
        # 'Imgur': 'https://imgur.com/user/', returns a landing page. to do
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
        # 'Deviantart': '.deviantart.com"',
        # ^ This website is either blocking/delaying the script
        'LiveJournel': '.livejournal.com',
        'Slack': '.slack.com',
    }

    p = ThreadPool(10)
    p.map(get_website_membership, list(websites.keys()))
    n_websites = len(list(websites.keys()))
    print('Summary: User {} has membership in {}/{} websites'
          .format(uname, counter, n_websites))
    banner('completed')


if __name__ == '__main__':
    main()
