#!/usr/bin/env python

from distutils.core import setup
try:
    import py2exe
    from nsis import build_installer
except:
    build_installer = None

import discocli

setup(name='DiscoCLI',
      version=discocli.__version__,
      description='Basic Terminal CLI Framework',
      author='Joaquin Lopez',
      author_email='mrgus@disco-zombie.net',
      packages=['discocli',],
      cmdclass = {"py2exe": build_installer},
     )

