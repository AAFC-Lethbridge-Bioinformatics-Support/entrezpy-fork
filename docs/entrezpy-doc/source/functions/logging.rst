.. _logging:

Logging
=======

entrezpy uses the `Python logging module
<https://docs.python.org/3/library/logging.html>`_ for logging. The base
classes do only log  the levels 'ERROR' and 'DEBUG'. The module
:mod:`entrezpy.log.logger` contains all methods related to logging. A basic
configuration of the logger is given in :mod:`entrezpy.log.conf`.

Applications using `entrezpy` can create logging calls on the class level. Each
class can set its own logger using the function
:meth:`entrezpy.log.logger.get_class_logger`. For an example take a look how the
class :class:`entrezpy.esearch.esearcher.Esearcher` sets its logger
(:numref:`logginginit`).

.. literalinclude:: ../../../../src/entrezpy/esearch/esearcher.py
  :caption: Example of creating a class level entrezpy logger.
  :linenos:
  :language: python
  :name: logginginit
  :lines: 32-35,43-48
  :emphasize-lines: 1,8


The :meth:`entrezpy.log.logger.get_class_logger` required the class as its
input.
