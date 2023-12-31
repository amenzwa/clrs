"""
This module contains graph representation described in
Chapter 20 Elementary Graph Algorithms.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from functools import reduce
from typing import Generic, TypeVar

import graphviz as V

from clrs.util import Infinity, Option, Tag, Tagged, isNone, todo

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
  def showParent(self) -> str: return "^" + self.par.tag if not self.isRoot() else "Root"
  def showTimes(self) -> str: return f"{self.dis if self.dis != Infinity else ''}{f'/{self.fin}' if self.fin != -Infinity else ''}"

  def isRoot(self) -> bool: return isNone(self.par)

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

def indicesOfETag(etag: Tag) -> [int, int]:
  [utag, vtag] = parseETag(etag)
  return [int(utag) - 1, int(vtag) - 1]  # vtag starts at 1

def etagOfIndices(i: int, j: int): return f"{i + 1}-{j + 1}"

## graph and tree

β = TypeVar("β")
VSet = {Tag, β}  # vertex set

ϵ = TypeVar("ϵ")
ESet = {Tag, ϵ}  # edge set

class VE(Tagged, Generic[β, ϵ]):  # abstract base for graph and tree types
  def __init__(self, tag: Tag):
    super().__init__(tag)

  def makeVE(self, vt: [Tag], et: [Tag]) -> None:
    self.makeV(vt)
    self.makeE(et)
  def makeV(self, vt: [Tag]) -> None: todo()
  def makeE(self, et: [Tag]) -> None: todo()

  def __str__(self) -> str: return self.tag + "\n" + self.showVertices() + "\n" + self.showEdges()
  def showVertices(self) -> str:
    def neighbors(u: β) -> str: return ",".join([v.tag for v in self.adj(u)])
    return "\n".join([f"  {u}\n    [{neighbors(u)}]" for u in self.getVV()])
  def showEdges(self) -> str: return "\n".join([f"  {e}" for e in self.getEE()])

  # vertex

  def insV(self, v: β) -> None: todo()
  def delV(self, v: β) -> None: todo()
  def dupVV(self, vv: VSet) -> None: todo()
  def getV(self, vtag: Tag) -> β: todo()
  def getVV(self) -> [β]: todo()
  def numVV(self) -> int: todo()
  def adj(self, u: β) -> [β]: todo()
  def hasV(self, vtag: Tag) -> bool: todo()

  # edge

  def insE(self, e: ϵ) -> None: todo()
  def delE(self, e: ϵ) -> None: todo()
  def dupEE(self, ee: ESet) -> None: todo()
  def getE(self, etag: Tag) -> ϵ: todo()
  def getEE(self) -> [ϵ]: todo()
  def numEE(self) -> int: todo()
  def hasE(self, etag: Tag) -> bool: todo()

class LstVE(VE):  # adjacency list representation of graphs and trees
  def __init__(self, tag: Tag):
    super().__init__(tag)
    self.vv: VSet = {}
    self.ee: ESet = {}

  def makeV(self, vt: [Tag]) -> None:
    for vtag in vt: self.vv[vtag] = Vert(vtag)
  def makeE(self, et: [Tag]) -> None:
    for etag in et:
      [utag, vtag] = parseETag(etag)
      e = Edge(self.getV(utag), self.getV(vtag))
      self.ee[e.tag] = e

  def pathSV(self, s: β, v: β) -> [β]:
    # path from source vertex s to vertex v; see p.562
    return [s] if v.isRoot() or v == s else [v, *self.pathSV(s, v.par)]
  def isAncestor(self, u: β, v: β) -> bool:
    # check if vertex u is the ancestor of vertex v (there exists a path from u ~> v)
    def reachable(a: β) -> bool:
      # check if a can reach v
      aa = self.adj(a)  # edge a -> v
      return True if v in aa else reduce(lambda acc, b: acc or reachable(b), aa, False)  # path a ~> v
    return True if u == v else reachable(u)  # self-loop or path
  def isDescendant(self, v: β, u: β) -> bool: return self.isAncestor(u, v)

  def insV(self, v: β) -> None: self.vv[v.tag] = v
  def delV(self, v: β) -> None: self.vv.pop(v.tag)
  def dupVV(self, vv: VSet) -> None: self.vv = {**vv}
  def getV(self, vtag: Tag) -> β: return self.vv[vtag]
  def getVV(self) -> [β]: return list(self.vv.values())
  def numVV(self) -> int: return len(self.getVV())
  def adj(self, u: β) -> [β]: return [self.getV(e.v.tag) for e in self.getEE() if e.u.tag == u.tag]
  def hasV(self, vtag: Tag) -> bool: return vtag in self.vv

  def insE(self, e: ϵ) -> None: self.ee[e.tag] = e
  def delE(self, e: ϵ) -> None: self.ee.pop(e.tag)
  def dupEE(self, ee: ESet) -> None: self.ee = {**ee}
  def getE(self, etag: Tag) -> ϵ: return self.ee[etag]
  def getEE(self) -> [ϵ]: return list(self.ee.values())
  def numEE(self) -> int: return len(self.getEE())
  def hasE(self, etag: Tag) -> bool: return etag in self.ee

WMtx = [[float]]  # adjacency matrix of edge weights

class MtxVE(LstVE):  # adjacency matrix representation of graphs and trees
  def __init__(self, tag: Tag):
    super().__init__(tag)
    self.ww: WMtx = []  # edge weight matrix

  def pathASP(self, i: int, j: int) -> [int]:
    if not dd or not pp: raise Exception("shortest paths not yet computed")
    if self.pp[i][j] == -Infinity: return []
    elif i == j: return [i]
    else: return self.pathASP(i, pp[i][j])

  def makeV(self, vt: [Tag]) -> None:
    for vtag in vt: self.vv[vtag] = Vert(vtag)
    n = len(vt)
    r = range(0, n)
    # see Equation 23.1 p.647
    self.ww = [[Infinity] * n for _ in r]
    for i in r: self.ww[i][i] = 0

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
