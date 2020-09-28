.. _logging:

Logging
=======

entrezpy uses the `Python logging module
<https://docs.python.org/3/library/logging.html>`_ for logging. The base
classes do only log  the levels 'ERROR' and 'DEBUG'. The module
:mod:`entrezpy.log.logger` contains all methods related to logging. A basic
configuration of the logger is given in :mod:`entrezpy.log.conf`.

Applications using `entrezpy` can set the level of logging as shown in
(:numref:`loglevelset`). Logging calls can be made in classes inheriting
entrezpy classes as shown in (:numref:`logginginit`). The
:meth:`entrezpy.log.logger.get_class_logger` required the class as its input.


Add logging to applications using ``entrezpy``
==============================================

Importing the logging module and set the level.

.. code-block:: python
  :caption: Setting the logging level for an application using the ``entrezpy``
            library
  :linenos:
  :name: loglevelset

  import entrezpy.log.logger

  entrezpy.log.logger.set_level('DEBUG')

  def main():
    """
    your application using entrezpy
    """

Add logging to a class inheriting a ``entrezpy`` base class
===========================================================


.. literalinclude:: ../../../../src/entrezpy/esearch/esearcher.py
  :caption: Example of creating a class level entrezpy logger.
  :linenos:
  :language: python
  :name: logginginit
  :lines: 32-35,43-48
  :emphasize-lines: 1,8
