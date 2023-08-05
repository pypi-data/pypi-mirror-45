from setuptools import setup

setup(
    name='plantpredict',
    version='0.8.7',
    description='Python 2.7 SDK for PlantPredict (https://ui.plantpredict.com).',
    url='http://github.com/storborg/funniest',
    author='Stephen Kaplan, Performance & Prediction Engineer at First Solar, Inc.',
    author_email='stephen.kaplan@firstsolar.com',
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    packages=['plantpredict'],
    install_requires=[
        'requests',
        'pandas',
        'certifi',
        'chardet',
        'idna',
        'numpy',
        'python-dateutil',
        'pytz',
        'six',
        'urllib3'
    ]
)
