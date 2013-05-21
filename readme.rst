
=============================
 Flickr Favorites Downloader
=============================

Setup
=====

* use virtualenv

::

  pip install flickrapi requests docopt


Usage
=====

At first register an app on the flickr api: http://www.flickr.com/services/apps/create/

Add this key and secret to a file called credentials.py.

::

  KEY = "YOUR KEY TO THE FLICKR API"
  SECRET = "YOUR SECRET TO THE FLICKR API"
  STORAGE = '/path/to/where/you/want/all/data/go'
  USERID = '12345678@N01'


To get your userid run ``python favdownloader.py get_userid <username>`` or copy from flickr urls.
Update database with images using ``python favdownloader.py update``.
And download all images in local database using ``python favdownloader.py download``


References
==========

 * API documentation: http://www.flickr.com/services/api/
 * flickrapi-packege-source: https://bitbucket.org/sybren/flickrapi/overview
 * flickrapi-package-docs: http://stuvel.eu/flickrapi

