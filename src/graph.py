"""
This module contains graph representation and implementations of algorithms described in
Chapter 20 Elementary Graph Algorithms.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from functools import reduce
from queue import Queue
from typing import Callable, Generic, TypeVar

import graphviz as V

from src.util import Infinity, Option, Tag, Tagged, isNone

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
    self.vv: VSet = {}
    self.ee: ESet = {}
    for u in self.getVV(): u.init()
    for e in self.getEE(): e.init()

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

  def __str__(self) -> str: return self.tag + "\n" + self.showVertices() + "\n" + self.showEdges()
  def showVertices(self) -> str:
    def neighbors(u: β) -> str: return ",".join([v.tag for v in self.adj(u)])
    return "\n".join([f"  {u}\n    [{neighbors(u)}]" for u in self.getVV()])
  def showEdges(self) -> str: return "\n".join([f"  {e}" for e in self.getEE()])

  # vertex

  def insV(self, v: β) -> None: self.vv[v.tag] = v
  def delV(self, v: β) -> None: self.vv.pop(v.tag)
  def dupVV(self, vv: VSet) -> None: self.vv = {**vv}
  def getV(self, vtag: Tag) -> β: return self.vv[vtag]
  def getVV(self) -> [β]: return list(self.vv.values())
  def numVV(self) -> int: return len(self.getVV())
  def adj(self, u: β) -> [β]: return [self.getV(e.v.tag) for e in self.getEE() if e.u.tag == u.tag]
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
  def hasV(self, vtag: Tag) -> bool: return vtag in self.vv

  # edge

  def insE(self, e: ϵ) -> None: self.ee[e.tag] = e
  def delE(self, e: ϵ) -> None: self.ee.pop(e.tag)
  def dupEE(self, ee: ESet) -> None: self.ee = {**ee}
  def getE(self, etag: Tag) -> ϵ: return self.ee[etag]
  def getEE(self) -> [ϵ]: return list(self.ee.values())
  def numEE(self) -> int: return len(self.getEE())
  def hasE(self, etag: Tag) -> bool: return etag in self.ee

class Graph(VE): pass

class Tree(VE): pass

def init(g: Graph) -> None:
  for u in g.getVV():
    u.par = None
    u.dis = Infinity
    u.col = VCol.White

## §20.2 Breadth-first search p.554

def bfs(g: Graph, s: Vert) -> Graph:
  def explore() -> Graph:
    if q.empty(): return g
    u = q.get()
    for v in g.adj(u):
      if v.col == VCol.White:
        # v discovered
        v.par = u
        v.dis = u.dis + 1
        v.col = VCol.Gray
        q.put(v)
    # u finished
    u.col = VCol.Black
    return explore()

  # initialize
  init(g)
  # s discovered
  s.par = None
  s.dis = 0
  s.col = VCol.Gray
  # search g
  q = Queue()
  q.put(s)
  return explore()

def bft(g: Graph, s: Vert) -> Tree:
  g = bfs(g, s)
  t = Tree(f"{g.tag}†")
  for u in g.getVV():
    if u == s or not u.isRoot(): t.insV(u)
  for u in t.getVV():
    if not u.isRoot():
      e = g.getE(makeETag(u.par, u))
      t.insE(e)
  return t

## §20.3 Depth-first search p.563

def dfs(g: Graph) -> Graph:
  def explore(u: Vert) -> None:
    time[0] += 1
    # u discovered
    u.dis = time[0]
    u.col = VCol.Gray
    for v in g.adj(u):
      e = g.getE(makeETag(u, v))
      if v.col == VCol.Black:
        e.cls = ECls.F if u.dis < v.dis else ECls.C
      elif v.col == VCol.Gray:
        e.cls = ECls.B
      elif v.col == VCol.White:
        v.par = u
        e.cls = ECls.T
        explore(v)
    time[0] += 1
    # u finished
    u.fin = time[0]
    u.col = VCol.Black

  # initialize
  init(g)
  # search g
  time = [0]  # use array instead of a scalar to allow explore() to mutate time
  for u in g.getVV():
    if u.col == VCol.White: explore(u)
  return g

def dff(g: Graph) -> Graph:
  g = dfs(g)
  f = Graph(f"{g.tag}†")
  f.dupVV(g.vv)
  for v in f.getVV():
    if not v.isRoot():
      e = g.getE(makeETag(v.par, v))
      f.insE(e)
  return f

## §20.4 Topological sort p.573

def tsort(g: Graph) -> [Vert]:
  g = dfs(g)
  return sorted(g.getVV(), key=lambda u: u.fin, reverse=True)

## §20.5 Strongly connected components

class Comp(Vert):
  def __init__(self, tag: Tag):
    super().__init__(tag)
    self.vv: VSet = {}  # strongly connected vertices
  def init(self) -> None: self.__init__(self.tag)

  def insVV(self, vv: [Vert]) -> None:
    for u in vv: self.vv[u.tag] = u
  def getVV(self) -> [Vert]: return list(self.vv.values())

def makeCTag(vv: [Vert]) -> Tag: return "+".join([v.tag for v in vv])

def scc(g: Graph) -> Graph:
  g = dfs(g)
  r = transpose(g)
  s = sort(r, attr=lambda u: u.fin, reverse=True)  # descending sort of vertices by finish times
  s = dfs(s)
  f = dff(s)
  return contract(g, f)

def transpose(g: Graph) -> Graph:
  # reverse edges
  r = Graph(f"{g.tag}!")
  r.dupVV(g.vv)
  for e in g.getEE(): r.insE(Edge(e.v, e.u))  # flip (u, v) to (v, u)
  return r

def sort(g: Graph, attr: Callable[[Vert], int], reverse: bool = False) -> Graph:
  # sort vertices
  s = Graph(f"{g.tag}§")
  for u in sorted(g.getVV(), key=attr, reverse=reverse): s.insV(u)  # sorted vertices
  s.dupEE(g.ee)
  return s

def contract(g: Graph, f: Graph) -> Graph:
  # contract DFS g using DFF f
  def scv(u: Vert) -> [Vert]:
    aa = f.adj(u)  # vertex u's adjacent vertices in DFF f
    return [] if not aa else [v := aa[0], *scv(v)]

  c = Graph(f"{g.tag}₵")  # SCC c
  # create vertices of SCC c
  for r in [v for v in g.getVV() if v.isRoot()]:  # for each root vertex r in DFS g
    vv = [r, *scv(r)]  # strongly connected vertices rooted at vertex r
    x = Comp(makeCTag(vv))  # create component x by merging strongly connected vertices vv
    x.insVV(vv)
    c.insV(x)  # insert component x into SCC c
  # create edges of SCC c
  cc: [Comp] = c.getVV()  # components of SCC c
  for x in cc:  # for each component x in SCC c
    aa: VSet = {}  # adjacent vertices of component x in DFS g
    vv = x.getVV()  # constituent vertices of component x
    for u in vv:  # for each constituent vertex u of component x
      for v in [a for a in g.adj(u) if a not in vv]: aa[v.tag] = v  # for each (u, v) leaving component x
    for a in aa.values():  # for each adjacent vertex a of component x
      for y in [b for b in cc if b != x]:  # for every other component y in SCC c
        if a in y.getVV():  # component y is adjacent to component x
          c.insE(Edge(x, y))  # insert edge (x, y) into SCC c
  return c

## utilities

def draw(g: Graph | Tree, directed: bool, label: str = "", engine: str = "sfdp") -> V.Graph:
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
