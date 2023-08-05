# Copyright (C) 2019 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Bubach, Germany
from contextlib import contextmanager

from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.User import system

from Products.CMFPlone.CatalogTool import CatalogTool

from Products.ExtendedPathIndex.ExtendedPathIndex import ExtendedPathIndex

from Products.AdvancedQuery import Generic, And, In, Eq
from Products.AdvancedQuery.eval.interfaces import IQueryRestrict
from Products.AdvancedQuery.eval.adapter import getSubscriptionAdapter
from Products.AdvancedQuery.tests.layer import AqTest, AqzcmlLayer, load_config

import dm.plone.advancedquery as paq
from .catalogtool import Restrict


class Layer(AqzcmlLayer):
  @classmethod
  def setUp(cls):
    load_config("configure.zcml", paq, cls.context)

  # cleanup is performed when the `AqzcmlLayer` is teared down
  #   our additional `setUp` should not interfere with other tests


class TestBase(AqTest):
  layer = Layer

ct = CatalogTool()
pi = ExtendedPathIndex("pi")
ct._catalog.indexes["pi"] = pi
paths = {}
for leaf in ("1/1 1/12/121 1/12/122 2/21/1".split()):
  comps = leaf.split("/")
  pd = paths
  for c in comps:
    if c not in pd: pd[c] = {}
    pd = pd[c]

def gen(prefix, pd):
  for c in sorted(pd):
    np = prefix + "/" + c
    yield np
    # Python 3 only
    # yield from gen(np, pd[c])
    for p in gen(np, pd[c]): yield p

class _O(object):
  def __init__(self, pi): self.pi = pi

for i, p in enumerate(gen("", paths)):
  indexed = pi.index_object(i, _O(p))


@contextmanager
def as_system():
  u = getSecurityManager().getUser()
  newSecurityManager(None, system)
  yield
  newSecurityManager(None, u)


class TestTool(TestBase):
  def test_restriction_applied(self):
    with self.assertRaises(KeyError):
      ct.evalAdvancedQuery(Generic("pi", "/1"))

  def test_restriction(self):
    restrict = getSubscriptionAdapter(ct, IQueryRestrict)
    self.assertIsInstance(restrict, Restrict.factory)
    q = Generic("pi", "/1")
    restrict = restrict.restrict
    rq = restrict(q)
    self.assertIsInstance(rq, And)
    self.assertIs(rq[0], q)
    self.assertIsInstance(rq[1], In)
    self.assertEqual(rq[1].index, "allowedRolesAndUsers")
    self.assertIsInstance(rq[2], Eq)
    self.assertEqual(rq[2].index, "effectiveRange")
    rq = restrict(q, show_inactive=True)
    self.assertEqual(len(rq), 2)
    with as_system():
      rq = restrict(q)
      self.assertEqual(len(rq), 2)

  def test_level_0_depth_0(self):
    self._check("/1", 0, 0, [0])

  def test_level_0_depth_1(self):
    # this should be
    # self._check("/1", 0, 1, [0, 1, 2])
    # but due to "https://github.com/plone/Products.ExtendedPathIndex/issues/14"
    #  the root node is missing (we behave like `ExtendedPathIndex`)
    self._check("/1", 0, 1, [1, 2])
    
  def test_level_None_depth_None(self):
    self._check("1/12", None, None, [2, 3, 4])

  def test_level_all_depth_0(self):
    self._check("1", -1, 0, [0, 1, 7])

  def test_level_in_path(self):
    self._check((("1", -1),), 0, 0, [0, 1, 7])

  def test_and(self):
    # Note: "and" is stupid for this index
    self._check(dict(query=("1", "2"), operator="and"), -1, None, [7])

  def test_or(self):
    self._check(("1", "2"), 0, 0, [0, 5])


  def _check(self, query, level, depth, should):
    qd =  query.copy() if isinstance(query, dict) else dict(query=query)
    if level is not None: qd["level"] = level
    if depth is not None: qd["depth"] = depth
    q = Generic("pi", qd)
    r = ct._unrestrictedEvalAdvancedQuery(q)
    self.assertEqual(list(r._seq), should)
