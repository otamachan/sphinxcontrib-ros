Advanced
--------

sphinx.ext.intersphinx
+++++++++++++++++++++++

Add following lines to your ``conf.py``.

.. code-block:: python

     extensions += ['sphinx.ext.intersphinx']
     intersphinx_mapping = {'ros':
       ('http://otamachan.github.io/sphinxros/indigo/', None)}

