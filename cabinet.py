# -*- coding: utf-8 -*-

"""
This module implements a command-line utility to scrape Sainsbury's Ripe
Fruits web pages for certain information.

The module is presented as a demonstration of web scraping using Python tools 
and the kinds of coding practices that would be needed for a larger, more
complex application.

The module is limited in scope as the navigation of the pages only matches the
html tags and class names used on the Sainsbury's site, however it is built
with multiple functions that could be modified to match a different page
format or to extract different data from the Sainsbury's pages.

To run the application type
python cabinet.py <url>
at the command line, replacing <url> with the url for the target page.

The results are printed in JSON format so you could pipe them to a file
or through another application.
"""

import re
import sys

import json
import requests
import bs4

def extract_price(text):
    """ extract the price information from the given text which is expected to
    be the contents of a pricePerUnit tag. This has the price preceded by
    a £ symbol and followed by several <abbr> tags.
    
    This uses a re to find the digits in the text. The re is anchored by the
    requirement for at least 1 digit. The decimal point (or decimal comma) and 
    digits after the point may be omitted to give some flexibility in case
    the site changes the format slightly.
    
    Returns the price as a float.
    """
    match = re.search(u'(\d{1,2}[,\.]*\d{0,2})',text)
    if match :
        res = float(match.group())
    else :
        print >> sys.stderr, 'Unable to find the price in', text
        res = 0.0
    return res

def get_web_page(url):
    """ Get the web page corresponding to the given url and return a requests
    object containing the page.
    Raise error if the page cannot be retrieved.
    """
    res=requests.get(url)
    if res.status_code != 200 :
        print >> sys.stderr, 'Could not load web page %s. Received status code %d' % (url,res.status_code)
        res.raise_for_status()
    return res

def get_outer_tags(htmlText):
    """ This returns a list of class=productInner tags from the given
    text which is expected to be the html of the web page.
    The class=productInner tag contains a productInfo tag with the title and href
    to the linked html and a class=pricePerUnit tag with the pricing.
    """
    soup = bs4.BeautifulSoup(htmlText,'html5lib')
    return soup.find_all(class_=u'productInner')

def extract_description(soup):
    """Given the soup extract the product description from it. The description
    is in a div class=productDataItemHeader, but there are multiples of these
    in the document so select the one with string of Description.
    The description text is in a div with class=productText as a sibling of the
    productDataItemHeader tag.
    """
    tags = soup.find_all(class_=u'productDataItemHeader')
    descripionTags = [ t for t in tags if u'Description' in t.string ]
    # There might be multiple matching tags but we just use the first
    descriptionTag = descripionTags[0].find_next_sibling(class_=u'productText')
    description = descriptionTag.text.strip()
    return description


def scrape_page(text):
    """ Scrape the given page returning a list of dicts where each dict
    has the results of the items found on the page.
    """
    res=[]
    for tag in get_outer_tags(text) :
        pageDict = {}
        pageDict['unit_price'] = extract_price(tag.find(class_='pricePerUnit').text)
        # The class=productInfo tag contains an <a> tag with the href and title string.
        innerTag = tag.find(class_=u'productInfo')
        pageDict['title'] = innerTag.a.text.strip()
        url = innerTag.a[u'href']
        # Follow the link to get the info from the linked html
        page = get_web_page(url)
        soup = bs4.BeautifulSoup(page.text,'html5lib')
        pageDict['description'] = extract_description(soup)
        pageDict['size'] = '%5.1fKb' % (len(page.text)/1024.0)

        res.append(pageDict)
    return res

usage = \
"""
You must provide a URL as the single command line argument, for example,
cabinet.py http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/5_products.html

The results will be printed to stdout so you can pipe them to a file 
or another programme.
"""

def scrape(argv) :
    """ Top level function to take the command line argument and call.
    scrape_page. This exists to allow scrape_page to be reused without it
    depending on the command line or to allow scrape_page to be called 
    with a sequence of different pages.
    """
    if len(argv) == 1 or 'help' in argv[1] or 'http' not in argv[1]:
        print >> sys.stderr, usage
        res = usage
    else :
        page = get_web_page(argv[1])
        results = scrape_page( page.text )
        total = sum( [d['unit_price'] for d in results ] )
        res = json.dumps({'results':results, 'total':total}, sort_keys=True, indent=4)
        print res
    return res # for unit test

if __name__ == '__main__' :
    scrape(sys.argv)
    
    
    