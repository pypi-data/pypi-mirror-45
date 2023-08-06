"""
Economist
~~~~~~~~~

Extract metadata from economist index and article pages

"""

import datetime as dt

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from soupstars import Parser, serialize
from soupstars.mixins.sqlalchemy_mixins import SqlalchemyMixin

Base = declarative_base()


class WeeklyIndexPages(Base):
    """
    Example model for storing the results of the parser
    """
    __tablename__ = "economist_weekly_pages"

    base_url = sa.Column(sa.String, primary_key=True)
    article_date = sa.Column(sa.Date)
    status_code = sa.Column(sa.Integer)
    num_articles = sa.Column(sa.Integer)


class WeeklyIndexPageParser(SqlalchemyMixin, Parser):
    """
    Parse metadata from the weekly updated index pages
    """

    Model = WeeklyIndexPages
    database_url = "sqlite:///:memory:"
    
    @serialize
    def base_url(self):
        "The url used"

        return self.url

    @serialize
    def article_date(self):
        "The date of the article"

        date_string = self.parsed_url.path.split('/')[-1]
        return dt.datetime.strptime(date_string, '%Y-%m-%d').date()

    @serialize
    def status_code(self):
        "Status code of the request"

        return self.response.status_code

    @serialize
    def num_articles(self):
        "The number of articles foudn on the page"

        return len(self.find_all('span', attrs={'class': 'print-edition__link-title'}))
