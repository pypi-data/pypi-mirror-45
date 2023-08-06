import json

from bs4 import BeautifulSoup
import requests


def serialize(function):
    function._soupstar_serializable = True
    return function


class Parser(BeautifulSoup):
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url)
        self.request = self.response.request
        super().__init__(self.response.content, features="html.parser")

    def _iter_serializers(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, '_soupstar_serializable') and attr != self:
                yield attr_name, attr

    def to_tuples(self):
        for attr_name, attr in self._iter_serializers():
            yield attr_name, attr()

    def to_dict(self):
        return dict(self.to_tuples())

    def to_json(self):
        return json.dumps(self.to_dict())