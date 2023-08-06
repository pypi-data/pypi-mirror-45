"""
Models
~~~~~~

The primary model provided by soupstars is the Parser class.
"""

import json

from bs4 import BeautifulSoup
import requests

from .serializers import serialize


class Parser(BeautifulSoup):
    """
    Base class for building parsers. 
    """

    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url)
        self.request = self.response.request
        super(Parser, self).__init__(self.response.content, features="html.parser")

    def _iter_serializers(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, '_soupstar_serializable') and attr != self:
                yield attr_name, attr

    def iter_serializer_names(self):
        for attr_name, attr in self._iter_serializers():
            yield attr_name

    def to_tuples(self):
        """
        Iterate over (name, value) for each identified serializer
        """

        for attr_name, attr in self._iter_serializers():
            yield attr_name, attr()

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