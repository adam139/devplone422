from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='my315ok.policy',
      version=version,
      description="A plone site policy package for Plone4",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Adam tang',
      author_email='yuejun.tang@gmail.com',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['my315ok'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'Products.PloneFormGen',
          'Products.Collage',
          'plone.app.testing',
          'collective.monkeypatcher',
          'collective.collage.portlets',
          'collective.collage.ploneformgen', 
          'Products.Collage', 
          'my315ok.diazo960',
          'webcouturier.dropdownmenu',
          'my315ok.products',          
          'my315ok.portlet.flash',
          'my315ok.portlet.logo',  
          'my315ok.portlet.footer',
          'my315ok.portlet.fetchouterhtml',  
          'my315ok.portlet.rollitems', 
          'my315ok.portlet.onlineservice', 
          'my315ok.portlet.embediframe',           
          'collective.portlet.pixviewer',
          'quintagroup.seoptimizer',                                                                        
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
#      setup_requires=["PasteScript"],
#      paster_plugins=["ZopeSkel"],
      )
