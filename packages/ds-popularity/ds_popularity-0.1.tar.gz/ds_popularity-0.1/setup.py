from setuptools import setup

setup(name='ds_popularity',
      version='0.1',
      description='',
      url='https://github.com/matthewashby/DS-popularity',
      author='DS',
      author_email='matt@ashby.co.uk',
      license='NA',
      packages=['googlesearch'],
      install_requires=[
        'cachetools==3.1.0',
        'google-api-python-client==1.7.8',
        'google-auth==1.6.3',
        'google-auth-httplib2==0.0.3',
        'httplib2==0.12.3',
        'pyasn1==0.4.5',
        'pyasn1-modules==0.2.5',
        'rsa==4.0',
        'six==1.12.0',
        'uritemplate==3.0.0',
      ],
      zip_safe=False)
