from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.examples.diazo',
      version=version,
      description="Example of Diazo (xdv) usage in Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "C-X-EXAMPLE.txt")).read() + "\n" + 
                       open(os.path.join("docs", "ORANGE-SUNSET-THEME.txt")).read() + "\n" + 
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.examples'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.xdv',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
