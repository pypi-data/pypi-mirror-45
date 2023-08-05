pyqalx
======

Interfaces to qalx. For more details, see `project documentation,<'http://docs.qalx.io'>`_.

Installation
------------

.. code-block:: bash

   $ pip install pyqalx



Requirements
------------
boto3
requests


Usage
-----

.. code-block:: python

   >>> from pyqalx import Qalx
   >>> qalx = Qalx()
   >>> data_item = qalx.add_item_data({"some_number":5})



