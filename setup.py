import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-rkigeonameapi',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description='An API to make relevant queries to an edited Geoname-DB instance.',
    long_description=README,
    url='https://github.com/benmaier/django-rkigeonameapi',
    author='Benjamin F. Maier',
    author_email='bfmaier@physik.hu-berlin.de',

    install_requires=[
            'django>=2.2.0',
            'djangorestframework>=3.10.3',
            'mysqlclient>=1.4.4',
            'humanfriendly>=4.18',
        ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
