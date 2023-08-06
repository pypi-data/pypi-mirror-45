from soupstars import Parser, serialize

class NytimesArticleParser(Parser):
    "Parse attributes from a NY times article"

    @serialize
    def title(self):
        return self.h1.text

    @serialize
    def author(self):
        return self.find(attrs={'itemprop': 'author creator'}).text
        