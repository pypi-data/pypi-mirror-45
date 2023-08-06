"""
NYTimes
~~~~~~~

Extract article links and article metadata from nytimes.com

"""

import re
import sys

from soupstars import Parser, serialize


if sys.version_info.major >= 3:
    import urllib
    urlparse = urllib.parse.urlparse
else:
    import urlparse
    urlparse = urlparse.urlparse


class NytimesArticleParser(Parser):
    """
    Parse attributes from a NY times article.
    
    >>> from soupstars.examples.nytimes import NytimesArticleParser

    """

    @serialize
    def title(self):
        """
        The title of the article.
        """

        return self.h1.text

    @serialize
    def author(self):
        """
        The author(s) of the article.
        """

        return self.find(attrs={'itemprop': 'author creator'}).text
        

class NytimesLinkParser(Parser):
    """
    Parse the links from a NY times webpage.

    :param str url: The webpage to parse

    >>> from soupstars.examples.nytimes import NytimesLinkParser
    """

    host = "www.nytimes.com"
    article_link_regex = re.compile(r'^/\d{4}/\d{2}/\d{2}/')

    def valid_nytimes_link(self, parsed_url):
        return parsed_url.netloc == self.host

    def valid_article_link(self, parsed_url):
        return re.match(self.article_link_regex, parsed_url.path) is not None

    def format_nytimes_link(self, parsed_url):
        return "{scheme}://{netloc}{path}".format(scheme=parsed_url.scheme,
                                                  netloc=parsed_url.netloc,
                                                  path=parsed_url.path)

    def nytimes_links(self):
        result = set()
        for tag in self.find_all('a'):
            url = tag.get('href', '')
            parsed_url = urlparse(url)
            if self.valid_nytimes_link(parsed_url):
                result.add(url)
        else:
            return list(result)
    
    @serialize
    def article_links(self):
        """
        A list of links that point to NYTimes articles
        """

        result = set()
        for url in self.nytimes_links():
            parsed_url = urlparse(url)
            if self.valid_article_link(parsed_url):
                result.add(self.format_nytimes_link(parsed_url))
        else:
            return result
            
    @serialize
    def non_article_links(self):
        """
        A list of links that points to NYTimes pages that are not articles.
        """
        
        result = set()
        for url in self.nytimes_links():
            parsed_url = urlparse(url)
            if not self.valid_article_link(parsed_url):
                result.add(self.format_nytimes_link(parsed_url))
        else:
            return result