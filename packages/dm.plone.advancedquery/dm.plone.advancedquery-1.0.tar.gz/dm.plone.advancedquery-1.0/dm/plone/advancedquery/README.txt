Small package to allow the use of ``Products.AdvancedQuery`` (version 4+)
in Plone 5.2+.

It provides a (required) adapter for Plone's ``CatalogTool``
and an (optional) adapter for Plone's ``ExtendedPathIndex``.

You must ensure that its ``configure.zcml`` is "executed" at startup.
This usually is ensured by extending the ``buildout`` definition
``zcml`` with ``dm.plone.advancedquery``.
