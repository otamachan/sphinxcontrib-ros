test-package
============

.. ros:message:: package/Hoge

   :constant test: description
   :constant-type test: std_msgs/Mes
   :constant-value test: 12
   :constant int32 test1: description
   :constant-value test1: 3.4

.. ros:service:: package/Piyo

.. ros:action:: package/Action

.. ros:node:: package/node

   :pub name: description
   :pub-type name: package/Hoge

   :pub package/Hoge ~publ: hogehoge

   :pub XXX: hogehoge
   :pub-type XXX: package/Hoge

   :sub package/Hoge ~hogehoge: hogehoge2

   :sub ~ggg/aaa: hogehoge2
   :sub-type ~ggg/aaa: package/Hoge

   :srv package/Piyo ~service: yahoo
   :srv_called package/Piyo ~service: yahoo

   :action package/Action ~action: yahoo
   :action_called package/Action ~action: yahoo

   :param int8 ~param: param
   :param-default ~param: 10

   :param_set int8 ~param: param
   :param_set-default ~param: YAHOO

index
=====

* :ref:`genindex`

