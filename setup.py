from setuptools import setup, find_packages

version = '1.0rc1'

setup(name='behaving',
      version=version,
      description="Behavior-Driven-Development testing for multi-user web/mail/sms apps",
      long_description=open("README.rst").read() + open("CHANGES.txt").read(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
      ],
      keywords='BDD Behavior-Driven-Development testing',
      author='Yiorgis Gozadinos',
      author_email='ggozad@crypho.com',
      url='http://github.com/ggozad/behaving',
      license='GPL',
      packages=find_packages('src', exclude=['tests']),
      package_dir={'': 'src'},
      namespace_packages=['behaving'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools', 'parse', 'behave', 'splinter', 'Appium-Python-Client'],
      entry_points="""
      [console_scripts]
      mailmock = behaving.mail.mock:main
      smsmock = behaving.sms.mock:main
      """
      )
