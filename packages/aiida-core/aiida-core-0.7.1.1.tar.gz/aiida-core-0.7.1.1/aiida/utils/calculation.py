# -*- coding: utf-8 -*-

__copyright__ = u"Copyright (c), This file is part of the AiiDA platform. For further information please visit http://www.aiida.net/. All rights reserved."
__license__ = "MIT license, see LICENSE.txt file."
__authors__ = "The AiiDA team."
__version__ = "0.7.1.1"


def add_source_info(node, func):
    """
    Take information about a function using inspection and add it as attributes
    of a node.

    :param node: The node to add the information to.
    :param func: The function to inspect.
    """
    import inspect

    # Note: if you pass a lambda function, the name will be <lambda>; moreover
    # if you define a function f, and then do "h=f", h.__name__ will
    # still return 'f'!
    node._set_attr("function_name", func.__name__)

    # Try to get the source code
    try:
        source_code, first_line = inspect.getsourcelines(func)
        node._set_attr("source_code", "".join(source_code))
        node._set_attr("first_line_source_code", first_line)
    except (IOError, OSError):
        pass
    try:
        with open(inspect.getsourcefile(func)) as f:
            source = f.read()
        # MU: Do we really want to store the whole file?
        node._set_attr("source_file", source)
    except (IOError, OSError):
        pass
