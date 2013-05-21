
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



References
==========

 * API documentation: http://www.flickr.com/services/api/
 * flickrapi-packege-source: https://bitbucket.org/sybren/flickrapi/overview
 * flickrapi-package-docs: http://stuvel.eu/flickrapi

