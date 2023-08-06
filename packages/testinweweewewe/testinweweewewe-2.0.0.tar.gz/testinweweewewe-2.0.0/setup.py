from setuptools import setup, find_packages

# Try to convert markdown README to rst format for PyPI.
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='testinweweewewe',
    version='2.0.0',
    description='The SMS API sends SMS messages to Australian mobile phones in a single request. This API allows you to send and receive messages. You can also query the status of a previously sent SMS message.  ## Authentication  This API uses OAuth v2 Bearer Token for its authentication.  The parameters that are needed to be sent for this type of authentication are as follows:  + `CONSUMER_KEY` - your consumer key  + `CONSUMER_SECRET` - your consumer secret',
    long_description=long_description,
    author='APIMatic SDK Generator',
    author_email='support@apimatic.io',
    url='https://apimatic.io',
    packages=find_packages(),
    install_requires=[
        'requests>=2.9.1, <3.0',
        'jsonpickle>=0.7.1, <1.0',
        'cachecontrol>=0.11.7, <1.0',
        'python-dateutil>=2.5.3, <3.0'
    ],
    tests_require=[
        'nose>=1.3.7'
    ],
    test_suite = 'nose.collector'
)