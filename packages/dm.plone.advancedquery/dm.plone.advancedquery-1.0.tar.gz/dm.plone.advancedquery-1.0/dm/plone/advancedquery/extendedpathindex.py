# Copyright (C) 2019 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Bubach, Germany
from zope.interface import implementer
from zope.component import adapter

from BTrees.IIBTree import IISet

from Products.ExtendedPathIndex.ExtendedPathIndex import \
     ExtendedPathIndex, string_types

from Products.AdvancedQuery.eval.adapter.query.converter import \
     _TermQuery, SafeInheritance, normalize_spec, \
     QueryIndexQueryCheck, \
     TAnd, TOr, TSet, IndexQueryConverter, conditional_adapter


pathindex_search = SafeInheritance(ExtendedPathIndex, "query_index", "search")


class PatchIndexQueryCheck(QueryIndexQueryCheck):
  def __call__(self, *objs):
    if not super(PatchIndexQueryCheck, self).__call__(*objs): return
    # we do not support `navtree`
    spec = normalize_spec(objs[1].make_spec())
    return not spec.get("navtree")

@conditional_adapter(pathindex_search, PatchIndexQueryCheck())
@adapter(ExtendedPathIndex, _TermQuery)
class PathIndexQueryConverter(IndexQueryConverter):
  def transform(self, q, context):
    idx = self.index
    spec = normalize_spec(q.make_spec())
    keys = spec["keys"]
    if not keys: return TOr()
    default_level = spec.get("level", 0)
    op = spec.get("operator", idx.useOperator)
    depth = spec.get("depth", -1)
    empty = TOr()
    def lookup1(comps, level):
      ands = []
      for i, c in reversed(list(enumerate(comps))):
        cd = idx._index.get(c)
        if cd is None: return empty
        cl = cd.get(i + level)
        if cl is None: return empty
        ands.append(TSet(cl))
      if depth >= 0:
        ors = []
        cd = idx._index.get(None)
        if cd is None: return emtpy
        s = level + len(comps) - 1
        for i in range(depth + 1):
          cl = cd.get(s + i)
          if cl is None: continue
          ors.append(TSet(cl))
        if not ors: return empty
        ands.append(TOr(*ors))
      if not ands:
        # ensure restriction to indexed objects
        ands.append(TSet(idx._unindex))
      return TAnd(*ands)
    def lookup(k):
      path, level = (k, default_level) if isinstance(k, string_types) \
                    else (k[0], int(k[1]))
      comps = [p for p in path.split("/") if p]
      if len(comps) > idx._depth + 1: return empty
      if level < 0:
        return TOr(*(
          lookup1(comps, level) for level in
          range(idx._depth + 2 - len(comps))))
      if level == 0 and depth in (0, 1):
        if not path.startswith("/"): path = "/" + path
        if depth == 0:
          did = idx._index_items.get(path)
          s = IISet((did,)) if did is not None else IISet()
        else: s = idx._index_parents.get(path, IISet())
        return TSet(s)
      if level + len(comps) > idx._depth + 1: return empty
      return lookup1(comps, level)
    return (TAnd if op == "and" else TOr)(*map(lookup, keys))
      

