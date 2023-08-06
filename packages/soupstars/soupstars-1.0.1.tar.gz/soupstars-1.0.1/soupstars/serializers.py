"""
Serializers
~~~~~~~~~~~

Serializers help convert parsers into storable objects. The functions defined in this module
are used to instruct soupstars about how to perform the serialization.
"""


def serialize(function):
    """
    Decorating a function defined on a parser with `serialize` instructs soupstars to include
    that function's return value when building its own serialization.

    >>> from soupstars import Parser, serialize
    >>> class MyParser(Parser):
    ...     @serialize
    ...     def length(self):
    ...         return len(self.response.content)
    ...
    >>> parser = MyParser('https://jsonplaceholder.typicode.com/todos/1')
    >>> first_serializer = next(parser.iter_serializer_names())
    >>> first_serializer
    'length'
    >>> first_serializer in parser.to_dict()
    True
    """

    function._soupstar_serializable = True
    return function