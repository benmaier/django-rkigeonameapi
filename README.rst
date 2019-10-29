RKI-GeonameAPI
==============

Django-webapp for easy access to a hierarchical geo-location database.

License
-------

This project is published under the MIT license. It uses the
`geoname-data <http://www.geonames.org/>`__ which is licensed under a
`Creative Commons Attribution 4.0
License <https://creativecommons.org/licenses/by/4.0/>`__.

Install and Deployment
----------------------

Only tested with Python 3.7 and Django 2.2. Make sure you installed the
modified version of the
`Geoname-DB <https://github.com/benmaier/GeoNames-MySQL-DataImport>`__
beforehand. This app expects an instance of MySQL 8.0.

Clone this repository.

.. code:: bash

   git clone git@github.com:benmaier/django-rkigeonameapi.git

Then install with pip

.. code:: bash

   pip install ./django-rkigeonameapi

Project settings
~~~~~~~~~~~~~~~~

Add ``rest_framework`` and ``rkigeonameapi`` to your ``INSTALLED_APPS``
setting like this

.. code:: python

   INSTALLED_APPS = [
       ...
       'rkigeonameapi',
       'rest_framework',
   ]

You can also add some settings for the rest framework. Here are the ones
we typically use:

.. code:: python

   REST_FRAMEWORK = {
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
       'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
       'PAGE_SIZE': 10,
       'DEFAULT_RENDERER_CLASSES': (
           'rest_framework.renderers.JSONRenderer',
           # The following is used to avoid time-outs in the browsable API
           # (since the automatically generated forms will try to load
           # all geonames in HTML-selects.)
           'rkigeonameapi.renderers.BrowsableAPIRendererWithoutForms',
       ),
   }

Add the urls to your ``projects/urls.py``

.. code:: python

   urlpatterns += [
       path('rkigeonameapi/', include('rkigeonameapi.urls')),
   ]

In your project, you now need to perform a migration to construct the
necessary tables in the database. Please continue reading before
actually performing the migration.

Database
~~~~~~~~

Make sure you installed the modified version of the
`Geoname-DB <https://github.com/benmaier/GeoNames-MySQL-DataImport>`__
beforehand. This app expects an instance of MySQL 8.0. Your
user/database should have the following settings:

.. code:: sql

   CREATE SCHEMA `your_db_name` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
   CREATE USER 'your_db_user'@'localhost' IDENTIFIED BY 'REPLACETHISWITHTHERIGHTPASSWORD';
   GRANT ALL PRIVILEGES ON your_db_name.* TO 'your_db_user'@'localhost';
   GRANT SELECT ON geonames.* TO 'your_db_user'@'localhost';

Given these settings, create a mysql-connection file
``your/path/to/db.cnf``

.. code:: config

   [client]
   host = localhost
   port = 3306
   user = your_db_user
   password = REPLACETHISWITHTHERIGHTPASSWORD
   database = your_db_name
   default-character-set = utf8mb4

Now, do the necessary migrations. In your **project** directory, do

.. code:: bash

   python manage.py makemigrations
   python manage.py makemigrations rkigeonameapi
   python manage.py migrate

The necessary tables in your ``your_db_name``-database should've been
created. This means we can migrate the necessary data from the original
``geonames``-database.

To this end, navigate back to your local clone of this repository

.. code:: bash

   cd /path/to/django-rkigeonameapi

And generate the sql migration file ``mymigration.sql`` with an optional
language-code argument.

.. code:: bash

   python make_geonamemigration_sql.py your/path/to/db.cnf mymigration.sql -l de

Note that this project renames the ``name`` property of all locations to
contain their most common German name by default. If you **don't** want
this you should can specify another language using the corresponding
ISO-ALPHA2 code. In case you just want to keep the english name, use
``-l en`` or something nonsensical like ``-l XXXXX`` (the script
automatically uses the English name for any location for which it cannot
find a name in the demanded language).

Afterwards, migrate your tables with

.. code:: bash

   /path/to/your/bin/mysql --defaults-file=your/path/to/db.cnf -v < mymigration.sql

Logic
-----

The Geoname-Database is an open-source dataset containing an exhaustive
list of places on earth. The database contains information about a
variety of properties and relationships of these places such as
alternative names in multiple languages, positional data, and
hierarchical relationships (e.g. to which country oder administrative
division a place belongs).

This project provides a simple interface to this database which allows a
user to easily retrieve data and to edit hierarchical relationships.

Geonames
~~~~~~~~

A Geoname is a main geographical entity. It could be a populated place,
a country or something else.

API endpoints
^^^^^^^^^^^^^

Admin: http://localhost:8000/admin/geonameapi/geoname/

REST:

+-------------------+------------+------------------------------------+
| Action            | Link       | Description                        |
+===================+============+====================================+
| list/create       | http://loc | Show a JSON list of all            |
|                   | alhost:800 | Geoname-objects and add an entry   |
|                   | 0/geonamea |                                    |
|                   | pi/geoname |                                    |
|                   | /          |                                    |
+-------------------+------------+------------------------------------+
| view/update       | http://loc | Show a single Geoname-object       |
|                   | alhost:800 | associated with the primary key as |
|                   | 0/geonamea | JSON                               |
|                   | pi/geoname |                                    |
|                   | /INTID     |                                    |
+-------------------+------------+------------------------------------+
| search            | http://loc | Show all Geoname-objects whose     |
|                   | alhost:800 | ``name`` and ``englishname``       |
|                   | 0/geonamea | contain the ``SEARCHSTRING``       |
|                   | pi/geoname |                                    |
|                   | search/SEA |                                    |
|                   | RCHSTRING  |                                    |
+-------------------+------------+------------------------------------+
| exhaustive search | http://loc | Show all Geoname-objects whose     |
|                   | alhost:800 | ``alternatenames`` or              |
|                   | 0/geonamea | ``englishname`` start with the     |
|                   | pi/geoname | ``SEARCHSTRING``                   |
|                   | exhaustive |                                    |
|                   | search/SEA |                                    |
|                   | RCHSTRING  |                                    |
+-------------------+------------+------------------------------------+
| search by feature | http://loc | As above, but only show geonames   |
| code              | alhost:800 | whose feature code is in the list  |
|                   | 0/geonamea | of feature codes provided in the   |
|                   | pi/geoname | URL                                |
|                   | search/SEA |                                    |
|                   | RCHSTRING? |                                    |
|                   | fcode=ADM1 |                                    |
|                   | ,PCLI      |                                    |
+-------------------+------------+------------------------------------+
| exhaustive search | http://loc | See definitions above              |
| by feature code   | alhost:800 |                                    |
|                   | 0/geonamea |                                    |
|                   | pi/geoname |                                    |
|                   | exhaustive |                                    |
|                   | search/SEA |                                    |
|                   | RCHSTRING? |                                    |
|                   | fcode=ADM1 |                                    |
|                   | ,PCLI      |                                    |
+-------------------+------------+------------------------------------+

A Geoname can always contain multiple children (think of a US state
containing cities). Here's how you control those hierarchical
relationships

Admin: http://localhost:8000/admin/geonameapi/hierarchy/

REST:

+-------------------+------------+------------------------------------+
| Action            | Link       | Description                        |
+===================+============+====================================+
| update            | http://loc | Show (``GET``) and update          |
|                   | alhost:800 | (``PATCH``) the children of a      |
|                   | 0/geonamea | single Geoname-object              |
|                   | pi/geoname |                                    |
|                   | children/I |                                    |
|                   | NTID       |                                    |
+-------------------+------------+------------------------------------+
| view specific     | http://loc | Show all children of a single      |
|                   | alhost:800 | Geoname-object that are associated |
|                   | 0/geonamea | with any of the specified feature  |
|                   | pi/geoname | codes                              |
|                   | fcodechild |                                    |
|                   | ren/INTID? |                                    |
|                   | fcode=ADM1 |                                    |
|                   | ,ADM2      |                                    |
+-------------------+------------+------------------------------------+

Feature codes
~~~~~~~~~~~~~

Each Geoname is associated with a feature code. Here are the most
relevant ones with explanations

Admin: http://localhost:8000/admin/geonameapi/featurecode

REST:

-  list/create: http://localhost:8000/geonameapi/featurecode
-  view/update: http://localhost:8000/geonameapi/featurecode/STRINGID

Continents and regions
^^^^^^^^^^^^^^^^^^^^^^

These are objectes that usually contain multiple countries

+-----------------+-------------+--------------------------------------+
| fcode           | name        | description                          |
+=================+=============+======================================+
| CONT            | continent   | continent: Europe, Africa, Asia,     |
|                 |             | North America, South America,        |
|                 |             | Oceania, Antarctica                  |
+-----------------+-------------+--------------------------------------+
| RGN             | region      | an area distinguished by one or more |
|                 |             | observable physical or cultural      |
|                 |             | characteristics                      |
+-----------------+-------------+--------------------------------------+

A region might also contain other places but this won't be of interest
in this application.

Countries
^^^^^^^^^

These are used as synonyms for countries

===== ============================
fcode name
===== ============================
PCLI  independent political entity
TERR  territory
PCLD  dependent political entity
===== ============================

Places
^^^^^^

These are used as synonyms for cities/villages/places that are neither
countries nor regions nor administrative sections.

+-----------------+-------------+--------------------------------------+
| fcode           | name        | description                          |
+=================+=============+======================================+
| PPLC            | capital of  |                                      |
|                 | a political |                                      |
|                 | entity      |                                      |
+-----------------+-------------+--------------------------------------+
| PPL             | populated   | a city, town, village, or other      |
|                 | place       | agglomeration of buildings where     |
|                 |             | people live and work                 |
+-----------------+-------------+--------------------------------------+
| PPLA            | seat of a   | seat of a first-order administrative |
|                 | first-order | division (PPLC takes precedence over |
|                 | administrat | PPLA)                                |
|                 | ive         |                                      |
|                 | division    |                                      |
+-----------------+-------------+--------------------------------------+
| PPLX            | section of  |                                      |
|                 | populated   |                                      |
|                 | place       |                                      |
+-----------------+-------------+--------------------------------------+

Administrative divisions
^^^^^^^^^^^^^^^^^^^^^^^^

These are hierarchically decreasing administrative divisions of a
country

+-----------------+-------------+--------------------------------------+
| fcode           | name        | description                          |
+=================+=============+======================================+
| ADM1            | first-order | a primary administrative division of |
|                 | administrat | a country, such as a state in the    |
|                 | ive         | United States                        |
|                 | division    |                                      |
+-----------------+-------------+--------------------------------------+
| ADM2            | second-orde | a subdivision of a first-order       |
|                 | r           | administrative division              |
|                 | administrat |                                      |
|                 | ive         |                                      |
|                 | division    |                                      |
+-----------------+-------------+--------------------------------------+
| ADM3            | third-order | a subdivision of a second-order      |
|                 | administrat | administrative division              |
|                 | ive         |                                      |
|                 | division    |                                      |
+-----------------+-------------+--------------------------------------+
| ADM4            | fourth-orde | a subdivision of a third-order       |
|                 | r           | administrative division              |
|                 | administrat |                                      |
|                 | ive         |                                      |
|                 | division    |                                      |
+-----------------+-------------+--------------------------------------+
| ADM5            | fifth-order | a subdivision of a fourth-order      |
|                 | administrat | administrative division              |
|                 | ive         |                                      |
|                 | division    |                                      |
+-----------------+-------------+--------------------------------------+

Regions
~~~~~~~

Custom regions are shortcuts for improved handling/grouping of
countries.

Admin: http://localhost:8000/admin/geonameapi/region/

REST:

-  list/create: http://localhost:8000/geonameapi/region/
-  view/update: http://localhost:8000/geonameapi/region/STRINGID

You may want to alter a region's children countries by using

-  http://localhost:8000/geonameapi/regioncountries/STRINGID

.. _countries-1:

Countries
~~~~~~~~~

The database holds specific info about countries.

Admin: http://localhost:8000/admin/geonameapi/country/

REST:

-  list/create: http://localhost:8000/geonameapi/country/
-  view/update: http://localhost:8000/geonameapi/country/STRINGID

Continents
~~~~~~~~~~

The database holds specific info about continents.

Admin: http://localhost:8000/admin/geonameapi/continent/

REST:

-  list/create: http://localhost:8000/geonameapi/continent/
-  view/update: http://localhost:8000/geonameapi/continent/STRINGID
