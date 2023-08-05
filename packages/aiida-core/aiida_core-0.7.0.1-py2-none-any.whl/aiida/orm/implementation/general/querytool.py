# -*- coding: utf-8 -*-

__copyright__ = u"Copyright (c), This file is part of the AiiDA platform. For further information please visit http://www.aiida.net/. All rights reserved."
__license__ = "MIT license, see LICENSE.txt file."
__version__ = "0.7.0.1"
__authors__ = "The AiiDA team."


class AbstractQueryTool(object):
    """
    Class to make easy queries without extensive knowledge of SQL, Django and/or
    the internal storage mechanism of AiiDA.

    .. note:: This feature is under constant development, so the name of the
      methods may change in future versions to allow for increased querying
      capabilities.

    .. todo:: missing
      features:

      * add __in filter
      * allow __in filter to accept other querytool objects to perform a single
        query
      * implement searches through the TC table
      * document the methods
      * allow to get attributes of queried data via a single query with suitable
        methods
      * add checks to verify whether filters as <=, ==, etc are valid for the
        specified data type (e.g., __gt only with numbers and dates, ...)
      * probably many other things...
    """
    # TODO SP: implement it completly.
    pass
