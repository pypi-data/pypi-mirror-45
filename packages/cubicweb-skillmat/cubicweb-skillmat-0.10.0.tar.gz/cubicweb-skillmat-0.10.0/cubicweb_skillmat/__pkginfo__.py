# pylint: disable-msg=W0622
"""cubicweb-skillmat application packaging information"""

modname = 'skillmat'
distname = 'cubicweb-skillmat'

numversion = (0, 10, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
description = 'skill matrix component for the CubicWeb framework'
author = 'Logilab'
author_email = 'contact@logilab.fr'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {'cubicweb': '>= 3.24.0',
               'cubicweb-folder': None,
               'cubicweb-comment': None}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]
