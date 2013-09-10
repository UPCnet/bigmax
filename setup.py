import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'pyramid',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_beaker',
    'pyramid_osiris',
    'pymongo',
    'rfc3339',
    'requests',
    'waitress',
    'pygments',
    'DateTime'
]

test_requires = ['WebTest', 'mock', ]

setup(name='bigmax',
      version='3.5',
      description='Big MAX - MAX Web Administration Interface',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pylons",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='UPCnet Content Management Team',
      author_email='victor.fernandez@upcnet.es',
      url='http://github.com/upcnet/bigmax',
      keywords='web pylons pyramid mongodb',
      packages=['bigmax'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires + test_requires,
      test_suite="bigmax.tests",
      extras_require={'test': ['WebTest', 'mock', ]},
      entry_points="""\
      [paste.app_factory]
      main = bigmax:main
      """,
      )
