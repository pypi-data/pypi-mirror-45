############
Contributing
############

This document provides guidelines for people who want to contribute to the
`django-anysign` project.


**************
Create tickets
**************

Please use `django-anysign bugtracker`_ **before** starting some work:

* check if the bug or feature request has already been filed. It may have been
  answered too!

* else create a new ticket.

* if you plan to contribute, tell us, so that we are given an opportunity to
  give feedback as soon as possible.

* Then, in your commit messages, reference the ticket with some
  ``refs #TICKET-ID`` syntax.


******************
Use topic branches
******************

* Work in branches.

* Prefix your branch with the ticket ID corresponding to the issue. As an
  example, if you are working on ticket #23 which is about contribute
  documentation, name your branch like ``23-contribute-doc``.


***********
Fork, clone
***********

Clone `django-anysign` repository (adapt to use your own fork):

.. code:: sh

   git clone git@github.com:peopledoc/django-anysign.git
   cd django-anysign/


*************
Usual actions
*************

The `Makefile` is the reference card for usual actions in development
environment:

* Install development toolkit with `pip`_: ``make develop``.

* Run tests with `tox`_: ``make test``.

* Build documentation: ``make documentation``. It builds `Sphinx`_
  documentation in `var/docs/html/index.html`.

* Release `django-anysign` project with `zest.releaser`_: ``make release``.

* Cleanup local repository: ``make clean``, ``make distclean`` and
  ``make maintainer-clean``.

See also ``make help``.


.. rubric:: Notes & references

.. target-notes::

.. _`django-anysign bugtracker`: https://github.com/peopledoc/django-anysign/issues
.. _`rebase`: https://git-scm.com/book/en/v2/Git-Branching-Rebasing
.. _`merge-based rebase`: https://tech.people-doc.com/psycho-rebasing.html
.. _`pip`: https://pypi.org/project/pip/
.. _`tox`: https://pypi.org/project/tox/
.. _`Sphinx`: https://pypi.org/project/Sphinx/
.. _`zest.releaser`: https://pypi.org/project/zest.releaser/
