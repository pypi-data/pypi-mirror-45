# Copyright (C) 2019 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Bubach, Germany
from zope.interface import implementer
from zope.component import adapter

from Products.CMFPlone.CatalogTool import CatalogTool, \
     _getAuthenticatedUser, DateTime

from Products.AdvancedQuery import Eq, In
from Products.AdvancedQuery.eval.interfaces import IQueryRestrict
from Products.AdvancedQuery.eval.adapter import \
     SafeInheritance, conditional_adapter


@conditional_adapter(SafeInheritance(CatalogTool, "__call__"))
@adapter(CatalogTool)
@implementer(IQueryRestrict)
class Restrict(object):
  def __init__(self, catalog): self.catalog = catalog

  def restrict(self, q, **kw):
    cat = self.catalog
    user = _getAuthenticatedUser(cat)
    q = q & In("allowedRolesAndUsers", cat._listAllowedRolesAndUsers(user))
    show_inactive = kw.get("show_inactive", False)
    if not show_inactive and not cat.allow_inactive(kw):
      q &= Eq("effectiveRange", DateTime())
    return q

