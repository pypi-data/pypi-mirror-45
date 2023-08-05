# -*- coding: utf-8 -*-
"""
Classes needed for tests.
Must be here because subclasses of 'Node' must be within aiida.orm
"""
from aiida.orm.calculation import Calculation

__copyright__ = u"Copyright (c), This file is part of the AiiDA platform. For further information please visit http://www.aiida.net/. All rights reserved."
__license__ = "MIT license, see LICENSE.txt file."
__version__ = "0.7.1.1"
__authors__ = "The AiiDA team."


class myNodeWithFields(Calculation):
    # State can be updated even after storing
    _updatable_attributes = ('state',)
