from setuptools import setup

setup(name="pyMicrodata",
      description="pyMicrodata Libray",
      version="1.1.1",
      author="Ivan Herman",
      author_email="ivan@w3.org",
	  maintainer="Ivan Herman",
	  maintainer_email="ivan@w3.org",
      packages=['pyMicrodata', 'pyMicrodata.serializers'],
      install_requires=['rdflib', 'pyRdfa', 'html5lib'],
)

