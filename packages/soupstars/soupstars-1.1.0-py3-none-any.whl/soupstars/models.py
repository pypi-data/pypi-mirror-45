"""
Models
~~~~~~

The primary model provided by soupstars is the `Parser` class. It should generally be subclassed
when building your own parsers.

When you initialize a parser with a url, it automatically downloads the webpage at that url
and stores both the request and response as attributes.

>>> from soupstars import Parser
>>> class MyParser(Parser):
...     @serialize
...     def item(self):
...         return 'An item!'
>>> parser = MyParser('https://jsonplaceholder.typicode.com/todos/1')
>>> print(parser.response)
<Response [200]>
>>> print(parser.request)
<PreparedRequest [GET]>
"""

import json

from bs4 import BeautifulSoup
import requests

from .serializers import serialize


class Parser(BeautifulSoup):
    """
    Primary class for building parsers.

    :param str url: The url to parse
    """

    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url)
        self.request = self.response.request
        super(Parser, self).__init__(self.response.content, features="html.parser")

    def _iter_serializers(self):
        for attr_name in sorted(dir(self)):
            attr = getattr(self, attr_name)
            if hasattr(attr, '_soupstar_serializable') and attr != self:
                yield attr_name, attr

    def serializer_names(self):
        """
        Returns a list of the names of the functions to be serialized.
        """

        return [item[0] for item in self._iter_serializers()]

    def serializer_functions(self):
        """
        Returns a list of the functions to be serialized.
        """

        return [item[1] for item in self._iter_serializers()]

    def to_tuples(self):
        """
        Returns a list of (name, value) tuples of each function to be serialized.
        """

        return [(attr_name, attr()) for attr_name, attr in self._iter_serializers()]

    def to_dict(self):
        """
        Convert the parser to a dictionary, with keys the names of
        each serializer and values the value of each serializer
        """

        return dict(self.to_tuples())

    def to_json(self):
        """
        Convert the parser to a JSON object
        """

        return json.dumps(self.to_dict())
