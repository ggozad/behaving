from setuptools import setup, find_packages

version = '1.5.3'

setup(name='behaving',
      version=version,
      description="Behavior-Driven-Development testing for multi-user web/mail/sms apps",
      long_description=open("README.rst").read(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Topic :: Software Development :: Testing",
          "Topic :: Software Development :: Libraries",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Software Development :: Quality Assurance",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
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
      install_requires=['parse', 'behave', 'splinter'],
      tests_require=['mr.developer', 'zc.buildout'],
      entry_points="""
      [console_scripts]
      mailmock = behaving.mail.mock:main
      smsmock = behaving.sms.mock:main
      gcmmock = behaving.notifications.gcm.mock:main
      """
      )
