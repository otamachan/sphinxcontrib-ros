HowTo
------

.. contents::
   :local:

Syntax Highlighting
++++++++++++++++++++

You can highlight a ROS message file(.msg, .srv, .action) using default directives like ``code-block`` and ``literalinclude``.

Example:

  .. code-block:: rst

     .. code-block:: rostype

        Header header # header
        geometry_msgs/Vector3 acc

     .. literalinclude:: Message.msg
        :language: rostype

Result:

  .. code-block:: rostype

     Header header # header
     geometry_msgs/Vector3 acc

  .. literalinclude:: Message.msg
     :language: rostype

Dirctives
++++++++++

.. rst:directive:: .. ros:package:: package_name

   This directive is to document package information by hand.
   If you have ``package.xml``, you can use :rst:dir:`ros:autopackage` instead.
   Following fields are supported.
   They are same as `REP-127 <http://www.ros.org/reps/rep-0127.html>`_ .

   * ``version``
   * ``description``
   * ``maintainer``
   * ``license``
   * ``url``
   * ``author``
   * ``build_depend``
   * ``buildtool_depend``
   * ``build_export_depend``
   * ``buildtool_export_depend``
   * ``exec_depend``
   * ``test_depend``
   * ``doc_depend``
   * ``conflict``
   * ``replace``
   * ``export``

   Example:

     .. code-block:: rst

        .. ros:package:: my_great_package

           :version: 1.0.0
           :description: This is a great package.
           :maintainer: John Smith
           :build_depend: :ros:pkg:`catkin`

   Reulst:

     .. ros:package:: my_great_package

        :version: 1.0.0
        :description: This is a great package.
        :maintainer: John Smith
        :build_depend: :ros:pkg:`catkin`

   Following options are supported:

   ``noindex``
      If this option is added, then the package object will not show in the indices.

.. rst:directive:: .. ros:autopackage:: package_name

   This directive generates package information document from ``package.xml``.

   Example:

     .. code-block:: rst

        .. ros:autopackage:: my_great_autopackage

   Reulst:

     .. ros:autopackage:: my_great_autopackage

   Following options are supported:

   ``noindex``
      Same as ``noindex`` of :rst:dir:`ros:package`.

   ``base`` : path
      Specify the ROS root path for the package.

.. rst:directive:: .. ros:message:: package_name/MessageName

.. rst:directive:: .. ros:automessage:: package_name/MessageName

   This directive is to document package information from ``package.xml``.

   Example:

     .. code-block:: rst

        .. ros:autopackage:: my_great_autopackage

   Reulst:

     .. ros:autopackage:: my_great_autopackage

   ``noindex``
      Same as ``noindex`` of :rst:dir:`ros:package`.

   ``base`` : path
      Specify the ROS root path for the package.

   ``description`` : *start:end*, [quote]
      **TODO**

   ``field-comment`` : [up-all|up|right1|right-down|right-down-all] [quote]
      **TODO**

   ``raw`` : [head|tail]
      **TODO**

.. rst:directive:: .. ros:service:: package_name/ServiceName

.. rst:directive:: .. ros:autoservice:: package_name/ServiceName

.. rst:directive:: .. ros:action:: package_name/ActionName

.. rst:directive:: .. ros:autoaction:: package_name/ActionName

.. rst:directive:: .. ros:node:: package_name/NodeName

Roles
++++++

.. rst:role:: ros:pkg

.. rst:role:: ros:msg

.. rst:role:: ros:srv

.. rst:role:: ros:action

Configurations
+++++++++++++++

.. confval:: ros_base_path = list of str

