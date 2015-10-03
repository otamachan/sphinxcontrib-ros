test-package
============

.. ros:package:: package

   :version:
   :description:
      .. raw:: html

         <a href="http://www.google.com">google</a>
   :maintainer:
   :license:
      BSD
   :license:
      MIT
   :url:
   :author:
   :build_depend:
   :buildtool_depend:
   :build_export_depend:
   :buildtool_export_depend:
   :exec_depend:
   :test_depend:
   :doc_depend:
   :conflict:
   :replace:
   :export:

test-package
============

.. ros:autopackage:: package_1

test-package-with-description
=============================

.. ros:autopackage:: package_1

   Addtive Description

test-package-with-field
=======================

.. ros:autopackage:: package_2

   :field: field

test-package-not-exist
=======================

.. ros:autopackage:: package_not_exist

test-package-with-base
======================

.. ros:autopackage:: package_1_under_another_base
   :base: ../../packages/another_base

test-package-not-exists-with-base
=================================

.. ros:autopackage:: package_not_exist_under_another_base
   :base: ../../packages/another_base

index
=====

* :ref:`genindex`

