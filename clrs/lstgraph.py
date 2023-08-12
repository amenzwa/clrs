"""
This module contains graph representation described in
Chapter 20 Elementary Graph Algorithms.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from functools import reduce
from typing import Generic, TypeVar

import graphviz as V

from clrs.util import Infinity, Option, Tag, Tagged, isNone

## vertex

class VCol:
  White = "White"
  Gray = "Gray"
  Black = "Black"

class Vert(Tagged):
  def __init__(self, tag: Tag):
    super().__init__(tag)
    self.par: Option[Vert] = None
    self.dis = Infinity
    self.fin = -Infinity
    self.col = VCol.White
  def init(self) -> None: self.__init__(self.tag)

  def __str__(self) -> str: return f"{self.tag} {self.showParent()} {self.showTimes()}"
  def show(self) -> str: return f"{self.tag}{f' {self.showTimes()}' if self.dis != Infinity else ''}"
  def showParent(self) -> str: return "^" + self.par.tag if not self.isRoot() else "None"
  def showTimes(self) -> str: return f"{self.dis if self.dis != Infinity else ''}{f'/{self.fin}' if self.fin != -Infinity else ''}"

  def isRoot(self) -> bool: return isNone(self.par)

β = TypeVar("β")
VSet = {Tag, β}

## edge

class ECls:
  X = "X"  # don't care
  T = "T"  # tree edge
  B = "B"  # back edge
  F = "F"  # forward edge
  C = "C"  # cross edge

class Edge(Tagged):
  def __init__(self, u: Vert, v: Vert):
    super().__init__(makeETag(u, v))
    self.u = u
    self.v = v
    self.cls = ECls.X
  def init(self) -> None: self.__init__(self.u, self.v)

  def __str__(self) -> str: return f"{self.tag} {self.showClassification()}"
  def show(self) -> str: return f"{self.showClassification()}"
  def showClassification(self) -> str: return self.cls if self.cls != ECls.X else ""

  def isSelfLoop(self) -> bool: return self.u == self.v

def makeETag(u: Vert, v: Vert) -> Tag: return f"{u.tag}-{v.tag}"

def parseETag(etag: Tag) -> [Tag, Tag]: return etag.split("-")

ϵ = TypeVar("ϵ")
ESet = {Tag, ϵ}

## graph and tree

class VE(Tagged, Generic[β, ϵ]):
  def __init__(self, tag: Tag):
    super().__init__(tag)

  def makeVE(self, vt: [Tag], et: [Tag]) -> None:
    self.makeV(vt)
    self.makeE(et)
  def makeV(self, vt: [Tag]) -> None: raise Exception("todo")
  def makeE(self, et: [Tag]) -> None: raise Exception("todo")

  def __str__(self) -> str: return self.tag + "\n" + self.showVertices() + "\n" + self.showEdges()
  def showVertices(self) -> str:
    def neighbors(u: β) -> str: return ",".join([v.tag for v in self.adj(u)])
    return "\n".join([f"  {u}\n    [{neighbors(u)}]" for u in self.getVV()])
  def showEdges(self) -> str: return "\n".join([f"  {e}" for e in self.getEE()])

  # vertex

  def insV(self, v: β) -> None: raise Exception("todo")
  def delV(self, v: β) -> None: raise Exception("todo")
  def dupVV(self, vv: VSet) -> None: raise Exception("todo")
  def getV(self, vtag: Tag) -> β: raise Exception("todo")
  def getVV(self) -> [β]: raise Exception("todo")
  def numVV(self) -> int: raise Exception("todo")
  def adj(self, u: β) -> [β]: raise Exception("todo")
  def path(self, s: β, v: β) -> [β]:
    # see p.562
    if v.isRoot(): return []
    return [s] if v == s else [v, *self.path(s, v.par)]
  def isAncestor(self, u: β, v: β) -> bool:
    # check if vertex u is the ancestor of vertex v (there exists a path from u ~> v)
    def reachable(a: β) -> bool:
      # check if a can reach v
      aa = self.adj(a)  # edge a -> v
      return True if v in aa else reduce(lambda acc, b: acc or reachable(b), aa, False)  # path a ~> v
    return True if u == v else reachable(u)  # self-loop or path
  def isDescendant(self, v: β, u: β) -> bool: return self.isAncestor(u, v)
  def hasV(self, vtag: Tag) -> bool: raise Exception("todo")

  # edge

  def insE(self, e: ϵ) -> None: raise Exception("todo")
  def delE(self, e: ϵ) -> None: raise Exception("todo")
  def dupEE(self, ee: ESet) -> None: raise Exception("todo")
  def getE(self, etag: Tag) -> ϵ: raise Exception("todo")
  def getEE(self) -> [ϵ]: raise Exception("todo")
  def numEE(self) -> int: raise Exception("todo")
  def hasE(self, etag: Tag) -> bool: raise Exception("todo")

class LstVE(VE):
  def __init__(self, tag: Tag):
    super().__init__(tag)
    self.vv: VSet = {}
    self.ee: ESet = {}
    for u in self.getVV(): u.egaInit()
    for e in self.getEE(): e.egaInit()

  def makeVE(self, vt: [Tag], et: [Tag]) -> None:
    self.makeV(vt)
    self.makeE(et)
  def makeV(self, vt: [Tag]) -> None:
    for vtag in vt: self.vv[vtag] = Vert(vtag)
  def makeE(self, et: [Tag]) -> None:
    for etag in et:
      [utag, vtag] = parseETag(etag)
      e = Edge(self.getV(utag), self.getV(vtag))
      self.ee[e.tag] = e

  # vertex

  def insV(self, v: β) -> None: self.vv[v.tag] = v
  def delV(self, v: β) -> None: self.vv.pop(v.tag)
  def dupVV(self, vv: VSet) -> None: self.vv = {**vv}
  def getV(self, vtag: Tag) -> β: return self.vv[vtag]
  def getVV(self) -> [β]: return list(self.vv.values())
  def numVV(self) -> int: return len(self.getVV())
  def adj(self, u: β) -> [β]: return [self.getV(e.v.tag) for e in self.getEE() if e.u.tag == u.tag]
  def hasV(self, vtag: Tag) -> bool: return vtag in self.vv

  # edge

  def insE(self, e: ϵ) -> None: self.ee[e.tag] = e
  def delE(self, e: ϵ) -> None: self.ee.pop(e.tag)
  def dupEE(self, ee: ESet) -> None: self.ee = {**ee}
  def getE(self, etag: Tag) -> ϵ: return self.ee[etag]
  def getEE(self) -> [ϵ]: return list(self.ee.values())
  def numEE(self) -> int: return len(self.getEE())
  def hasE(self, etag: Tag) -> bool: return etag in self.ee

class MtxVE(VE): pass

class LstGraph(LstVE): pass
class MtxGraph(MtxVE): pass

class LstTree(LstVE): pass
class MtxTree(MtxVE): pass

## utilities

def draw(g: LstGraph | MtxGraph | LstTree, directed: bool, label: str = "", engine: str = "sfdp") -> V.Graph:
  # returned gv must be evaluated in the top level scope for it to render in the notebook
  gv = V.Digraph(engine=engine) if directed else V.Graph(engine=engine)
  gv.attr(label=label if label != "" else g.tag)
  for v in g.getVV(): gv.node(v.tag, label=v.show(), shape=f"{'rectangle' if v.isRoot() else 'ellipse'}")
  ed = {}  # already drawn edges
  for e in g.getEE():
    vutag = makeETag(e.v, e.u)
    if directed or vutag not in ed.keys():  # for undirected graph, avoid drawing (u, v) if (v, u) has already been drawn
      gv.edge(e.u.tag, e.v.tag, label=e.show())
      ed[e.tag] = e
  return gv
