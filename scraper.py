__author__ = "Reggy Tjitradi and Ramon with the guidance from Howard and Chris"

import requests
import argparse
from bs4 import BeautifulSoup, SoupStrainer
import sys
import re


def scraper(link):
    res = requests.get(link)
    for link in BeautifulSoup(res.text, 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            address = link.get('href')
            url = re.search(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                            str(address))
            if url:
                print('URL: ' + url.group())
    for email in BeautifulSoup(res.text, 'html.parser'):
        emails = re.search(r"([a-zA-Z]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.][a-zA-Z]+)", str(email))
        if emails:
            print('Email Address: ' + emails.group())

    for number in BeautifulSoup(res.text, 'html.parser'):
        numbers = re.search(r"1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?", str(number))
        if numbers:
            print('Phone Number: ' + numbers.group())
    for image in BeautifulSoup(res.text, 'html.parser', parse_only=SoupStrainer('img')):
        src = image.get('src')
        print('Image: ' + str(src))


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='url of page to scrape')
    return parser


def main(args):
    parser = create_parser()
    args = parser.parse_args(args)
    url = args.link
    return scraper(url)


if __name__ == '__main__':
    main(sys.argv[1:])
