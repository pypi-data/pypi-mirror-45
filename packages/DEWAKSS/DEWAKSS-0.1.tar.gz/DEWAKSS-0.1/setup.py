from setuptools import setup

DISTNAME = 'DEWAKSS'
VERSION = '0.1'
DESCRIPTION = "De-noising Expression by Weighted Affinity-based Kernal with Self Supervision."
# with open('README.rst') as f:
#     LONG_DESCRIPTION = f.read()
MAINTAINER = 'Andreas Tjärnberg'
MAINTAINER_EMAIL = 'andreas.tjarnberg@nyu.edu'
URL = 'https://gitlab.com/Xparx/dewakss'
DOWNLOAD_URL = ''
LICENSE = 'LGPL'


setup(name=DISTNAME,
      version=VERSION,
      description=DESCRIPTION,
      url=URL,
      author=MAINTAINER,
      author_email=MAINTAINER_EMAIL,
      license=LICENSE,
      packages=['dewakss'],
      python_requires='>=3.6',
      install_requires=[
          'scipy',
          'sklearn',
          'scanpy',
          'scvelo',
          'matplotlib',
      ],
      zip_safe=False)
