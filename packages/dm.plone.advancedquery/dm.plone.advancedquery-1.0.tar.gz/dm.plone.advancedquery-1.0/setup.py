from os.path import abspath, dirname, join
try:
  # try to use setuptools
  from setuptools import setup
  setupArgs = dict(
      include_package_data=True,
      namespace_packages=['dm', 'dm.plone'],
      install_requires=[
      "Products.AdvancedQuery >= 4",
      "Products.CMFPlone",
      "setuptools", # make `buildout` happy
      ],
      zip_safe=False,
      )
except ImportError:
  # use distutils
  from distutils import setup
  setupArgs = dict(
    )

cd = abspath(dirname(__file__))
pd = join(cd, 'dm', 'plone', 'advancedquery')

def pread(filename, base=pd): return open(join(base, filename)).read().rstrip()

setup(name='dm.plone.advancedquery',
      version=pread('VERSION.txt').split('\n')[0],
      description='"Products.AdvancedQuery" extensions for Plone',
      long_description=pread('README.txt'),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Framework :: Plone',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        ],
      author='Dieter Maurer',
      author_email='dieter@handshake.de',
      url='https://pypi.org/project/dm.plone.advancedquery',
      packages=['dm', 'dm.plone', 'dm.plone.advancedquery'],
      keywords='Plone AdvancedQuery search',
      license='GPL',
      **setupArgs
      )
