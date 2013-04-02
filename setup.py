from setuptools import setup, find_packages

version = '0.1'

setup(name='behaving',
      version=version,
      description="BDD web-app testing done right.",
      long_description=open("README.rst").read(),
      classifiers=[],
      keywords='',
      author='Yiorgis Gozadinos',
      author_email='ggozad@crypho.com',
      url='http://github.com/ggozad/behaving',
      license='GPL',

      packages=find_packages('src', exclude=['tests']),
      package_dir={'': 'src'},
      namespace_packages=['behaving'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools', 'behave', 'splinter'],
      entry_points="""
      [console_scripts]
      mailmock = behaving.mail.mock:main
      smsmock = behaving.sms.mock:main
      """
      )
