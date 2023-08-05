The API Documentation / Guide
=============================

Information on specific functions, classes, and methods.


Quickly Examples
--------

.. mdinclude:: api.md




Apps Interface
--------------



Primary
^^^^^^^

There are two factory methods for mcutk.apps, use the factory method could easily get
you want app module, rather than import each by path.

.. inheritance-diagram:: mcutk.apps
   :parts: 2

.. autofunction:: mcutk.apps.factory

.. autofunction:: mcutk.apps.appfactory



IAR workbench
^^^^^^^^^^^^^


.. automodule:: mcutk.apps.iar
    :members:
    :private-members:

    :inherited-members:


MCUXPresso IDE
^^^^^^^^^^^^^^

.. automodule:: mcutk.apps.mcux
    :members:
    :private-members:

    :inherited-members:

ARM MDK
^^^^^^^

.. automodule:: mcutk.apps.mdk
    :members:
    :private-members:

    :inherited-members:

ARM DS-MDK
^^^^^^^^^^^^^^

.. automodule:: mcutk.apps.dsmdk
    :members:
    :private-members:

    :inherited-members:

GNU ARM-GCC
^^^^^^^^^^^^^^

.. automodule:: mcutk.apps.armgcc
    :members:
    :private-members:

    :inherited-members:

Debuggers
---------

.. automodule:: mcutk.debugger
    :members:
    :inherited-members:



J-Link
^^^^^^

.. automodule:: mcutk.debugger.jlink
    :members:
    :inherited-members:


PyOCD
^^^^^^

.. automodule:: mcutk.debugger.pyocd
    :members:
    :inherited-members:



RedLink(MCUXPresso)
^^^^^^^^^^^^^^^^^^^

.. automodule:: mcutk.debugger.redlink
    :members:
    :inherited-members:


Board
------

Get board
^^^^^^^^^

.. autofunction:: mcutk.board.getboard


Base board
^^^^^^^^^^

.. autoclass:: mcutk.board.baseboard.Board
    :members:



Pserial Interface
------------------

.. automodule:: mcutk.pserial
    :members:



Git repo Interface
------------------

.. automodule:: mcutk.repo
    :members:



Util
----

.. automodule:: mcutk.util
    :members:


