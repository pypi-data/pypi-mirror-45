.. image:: https://travis-ci.org/zopefoundation/Products.TemporaryFolder.svg?branch=master
   :target: https://travis-ci.org/zopefoundation/Products.TemporaryFolder

.. image:: https://coveralls.io/repos/github/zopefoundation/Products.TemporaryFolder/badge.svg?branch=master
   :target: https://coveralls.io/github/zopefoundation/Products.TemporaryFolder?branch=master

.. image:: https://img.shields.io/pypi/v/Products.TemporaryFolder.svg
   :target: https://pypi.org/project/Products.TemporaryFolder/
   :alt: Current version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/Products.TemporaryFolder.svg
   :target: https://pypi.org/project/Products.TemporaryFolder/
   :alt: Supported Python versions

Overview
========

Zope temporary storage / folder support.

This package contains ``Products.TemporaryFolder`` and
``Products.ZODBMountPoint``.

Please note
-----------
Don't forget to add or uncomment the temporary storage database definition
in your Zope configuration so a temporary folder can get created::

  <zodb_db temporary>
      <temporarystorage>
        name Temporary database (for sessions)
      </temporarystorage>
      mount-point /temp_folder
      container-class Products.TemporaryFolder.TemporaryContainer
  </zodb_db>
