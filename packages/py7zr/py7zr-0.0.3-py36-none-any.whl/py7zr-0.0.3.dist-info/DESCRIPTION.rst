=====
py7zr
=====

.. image:: https://travis-ci.org/miurahr/py7zr.svg?branch=master
  :target: https://travis-ci.org/miurahr/py7zr

.. image:: https://coveralls.io/repos/github/miurahr/py7zr/badge.svg?branch=master
  :target: https://coveralls.io/github/miurahr/py7zr?branch=master

Pure python 7zr implementation


Dependency
==========

It uses a standard lzma module that is supported in Python3.3 and later.


Document
========

Here is a readthedocs `manual`_ document.

.. _`manual`: https://py7zr.readthedocs.io/en/latest/


Usage
=====

You can run command script py7zr like as follows;

.. code-block::

    $ py7zr l test.7z


py7zr is a library which can use in your pyhton application.
Here is a code snippet how to decompress some file in your applicaiton.

.. code-block::

    import py7zr

    def decompress(file):
        archive = py7zr.Archive(file)
        archive.extract_all(dest="/tmp")


License
=======

* Copyright (C) 2019 Hiroshi Miura
* Copyright (c) 2004-2015 by Joachim Bauch
* 7-Zip Copyright (C) 1999-2010 Igor Pavlov
* LZMA SDK Copyright (C) 1999-2010 Igor Pavlov

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA


