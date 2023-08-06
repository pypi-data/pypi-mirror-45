from os.path import abspath, dirname, join
try:
  # try to use setuptools
  from setuptools import setup
  setupArgs = dict(
      include_package_data=True,
      namespace_packages=['dm', 'dm.zopepatches'],
      install_requires=[
        "setuptools", # to keep `buildout` happy
      ],
      zip_safe=False,
      entry_points = dict(
        ),
      )
except ImportError:
  # use distutils
  from distutils import setup
  setupArgs = dict(
    )

cd = abspath(dirname(__file__))
pd = join(cd, 'dm', 'zopepatches', 'ztutils')

def pread(filename, base=pd): return open(join(base, filename)).read().rstrip()

setup(name='dm.zopepatches.ztutils',
      version=pread('VERSION.txt').split('\n')[0],
      description="Patches for Zope's ZTUtils in order to make 'make_query' and 'make_hidden_input* more flexible and more reliable.",
      long_description=pread('README.txt'),
      classifiers=[
#        'Development Status :: 3 - Alpha',
       'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Framework :: Zope2',
        'Framework :: Zope',
        'Framework :: Zope :: 4',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        ],
      author='Dieter Maurer',
      author_email='dieter@handshake.de',
      url='http://pypi.python.org/pypi/dm.zopepatches.ztutils',
      packages=['dm', 'dm.zopepatches', 'dm.zopepatches.ztutils'],
      keywords='application development menu web',
      license='BSD',
      **setupArgs
      )
