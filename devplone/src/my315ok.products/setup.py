from setuptools import setup, find_packages
import os

version = '4.0'

setup(name='my315ok.products',
      version=version,
      description="A product showing system based dexterity",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='python plone',
      author='Adam tang',
      author_email='yuejun.tang@gmail.com',
      url='https://github.com/collective/my315ok.products.git',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['my315ok'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'five.globalrequest',
          'five.grok',                    
          'BeautifulSoup',
          'plone.namedfile [blobs]',
          'Products.CMFPlone',
          'plone.app.registry',          
          'plone.app.textfield',
          'plone.app.dexterity [grok]',
          'z3c.caching', 
          'plone.behavior',
          'plone.directives.form',                             
          'zope.schema',
          'zope.interface',
          'zope.component',
          'rwproperty',
          'z3c.caching', 
          'plone.multilingualbehavior',
          'plone.multilingual',                            
#          'plone.app.referenceablebehavior',
#          'plone.app.relationfield',          
          # -*- Extra requirements: -*-
      ],
       extras_require={
          'test': ['plone.app.testing',]
          },      
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      # The next two lines may be deleted after you no longer need
      # addcontent support from paster and before you distribute
      # your package.
#      setup_requires=["PasteScript"],
#      paster_plugins = ["ZopeSkel"],

      )
