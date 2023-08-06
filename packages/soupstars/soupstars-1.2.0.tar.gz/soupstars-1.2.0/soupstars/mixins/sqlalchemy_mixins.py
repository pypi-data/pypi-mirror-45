"""
SQLAlchemy Mixins
~~~~~~~~~~~~~~~~~

Mixins for saving parsers via SQLAlchemy 
"""

import sqlalchemy as sa


# TODO: make a base class with documentation for the OrmMixin api
class SqlalchemyMixin(object):
    """
    Use as a mixin on a Parser to save its data to a SQLAlchemy model
    """

    Model = None
    database_url = None
    _session = None

    def _check_attributes(self):
        if self.Model is None:
            raise AttributeError("Ensure the Parser has a Model attribute")
        if self.database_url is None:
            raise AttributeError("Ensure the Parser has a database_url attribute")

    def load_session(self):
        """
        Loads a SQLAlchemy session object.
        """

        self._check_attributes()
        if self._session:
            return self._session
        else:
            eng = sa.engine.create_engine(self.database_url)
            Session = sa.orm.sessionmaker(bind=eng)
            self._session = Session()
            return self._session

    def save(self):
        """
        Saves the parser to the SQLAlchemy Model defined on the class
        """

        self._check_attributes()        
        model = self.Model(**self.to_dict())
        session = self.load_session()
        session.add(model)
        session.commit()

    @property
    def query(self):
        return self.load_session().query(self.Model)
        