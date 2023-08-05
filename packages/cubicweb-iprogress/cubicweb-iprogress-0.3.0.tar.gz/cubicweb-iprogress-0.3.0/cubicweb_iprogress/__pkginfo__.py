# pylint: disable=W0622
"""cubicweb-iprogress application packaging information"""

modname = 'iprogress'
distname = 'cubicweb-iprogress'

numversion = (0, 3, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'some adapters and view for stuff progressing to reach a milestone'
web = 'http://www.cubicweb.org/project/%s' % distname
classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]

__depends__ =  {'cubicweb': '>= 3.24.0'}
__recommends__ = {}
