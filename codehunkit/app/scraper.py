"""
Method for scraping web page
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

import urllib2

def get_content(url):
    """
    Returns page content on specified url
    """
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) tangleon.com +(mailto:hi@tangleon.com)')
        
    response = urllib2.urlopen(request)
    try:
        return response.read()
    finally:
        response.close()    