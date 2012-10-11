from setuptools import setup, find_packages

version = '0.1'

setup(name='behave.web',
      version=version,
      description="Helpers for doing BDD on web applications with behave",
      long_description=open("README.rst").read(),
      classifiers=[],
      keywords='',
      author='Yiorgis Gozadinos',
      author_email='ggozad@crypho.com',
      url='http://ggozad.com',
      license='GPL',
      packages=find_packages(exclude=['tests']),
      namespace_packages=['behave'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools', 'behave', 'splinter'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
