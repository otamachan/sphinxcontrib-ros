Setup
-----

Installation
+++++++++++++

Download and install from PyPI.

.. code-block:: bash

   $ pip install sphinxcontrib-ros

conf.py
++++++++

Add following lines in your ``conf.py`` file:

.. code-block:: python

   extensions = ['sphinxcontrib.ros']
   ros_base_path = ['../src']
