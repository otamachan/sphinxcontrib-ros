test-code-block
================

.. code-block:: rostype

   # test comment
      # with space
   bool bool_field  #comment after field

   # test types
   bool bool_field
   int8 int8_field
   uint8 uint8_field
   int16 int16_field
   uint16 uin16_field
   int32 int32_field
   uint32 uint32_field
   int64 int64_field
   uint64 uint64_field
   float32 float32_field
   float64 float64_field
   string string_field
   time time_field
   duration duration_field

   some_package/SomeMessage some_message_field

   SomeMessageInSamePackage some_message_in_same_package_field

   Header header

   bool[] bool_field_array # variable-length
   bool[10] int8_field_array # fixed-length

   # test constants
   int32 INT32_CONSTANT=123
   int32 NEGATIVE_INT32_CONSTANT=-123
   float32 FLOAT32_CONSTANT=1.0
   float32 NEGATIVE_FLOAT32_CONSTANT=-0.31
   string FOO=foo
   string EXAMPLE="#comments" are ignored, and leading and trailing whitespace remove

   # test separation
   ---
   bool bool_field_after_separation

test-literalinclude
====================

.. literalinclude:: ../../packages/package_1/msg/Message1.msg
   :language: rosmsg

test-literalinclude-fail
=========================

.. literalinclude:: ../../packages/package_1/msg/Message1.msg_not_exist
   :language: rosmsg
