This package patches Zope's ``ZTUtils`` to enhance its ``make_query`` and
``make_hidden_input`` functions. Those functions are used to pass values across
two requests and allow the target request to get the value in approximately
the same way (e.g. in the same type) as it has been in the source request,
avoiding tedious fixups in the target request.

The standard Zope versions are quite limited. They support
(binary) strings, integers, floats and ``DateTime.DateTime`` as
elementary data types and lists and namespaces (i.e. something
with an ``items`` method) of those elemantary types for structured
values.

This package replaces Zope's ``ZTUtils.Zope.complex_marshal`` by a variant
that correctly handles unicode and tuples. In addition, empty lists
(and tuples) are retained. Tuples are marshalled as lists. This
patch makes "make_query" and "make_hidden_input" more reliable.

From version 1.1 on, the application can register extensions
to support additional elementary data types or to support
passing structured values which are more deeply nested. For details,
please see the docstrings of class ``Extension`` and the functions
``register_extension`` and ``unregister_extension``.

By default, the extension framework is used to register
an extension handling ``None`` values. Note that this changes
the behavior for ``None`` passing relative to pre 1.1 versions.
Use ``unregister_extension("none")`` to keep the old behavior.

The extension framework is used to define the function
``register_json_extension``.
It uses JSON marshalling to represent subvalues in
structured data which are too deeply nested to be handled by
basic mashalling. Should you need customization
for the JSON marshalling, take the implementation of
``register_json_extension`` as a blueprint for your own definition.


Version history
===============

2.0

   Python 3/Zope 4 compatibility

1.1

   Extension framework to optionnaly support application specific
   handling of new data types and deeper data structures

   ``None`` is (by default) passed on as the object ``None`` not as
   the string ``"None"``.

1.0

   Lets ``make_query`` and ``make_hidden_inputs``
   reliably handle unicode, tuples and empty lists.
   
