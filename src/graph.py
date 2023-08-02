"""
This module contains graph representation and implementations of algorithms described in
Chapter 20 Elementary Graph Algorithms.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from functools import reduce
from queue import Queue
from typing import Callable, Dict, List, Union

import graphviz as V

from src.util import Infinity, Option, Tag, Tagged, isNone

## vertex

class VColor:
  White = "White"
  Gray = "Gray"
  Black = "Black"

class Vertex(Tagged):
  def __init__(self, tag: Tag):
    super().__init__(tag)
    self.par: Option[Vertex] = None
    self.dis = Infinity
    self.fin = -Infinity
    self.col = VColor.White
  def init(self) -> None: self.__init__(self.tag)

  def __str__(self) -> str: return f"{self.tag}: {self.showParent()} {self.showTimes()}"
  def show(self) -> str: return f"{self.tag}{f': {self.showTimes()}' if self.dis != Infinity else ''}"
  def showParent(self) -> str: return "^" + self.par.tag if not self.isRoot() else "None"
  def showTimes(self) -> str: return f"{self.dis if self.dis != Infinity else ''}{f'/{self.fin}' if self.fin != -Infinity else ''}"

  def isRoot(self) -> bool: return isNone(self.par)

VSet = Dict[Tag, Vertex]

## edge

class EClass:
  X = "X"  # don't care
  T = "T"  # tree edge
  B = "B"  # back edge
  F = "F"  # forward edge
  C = "C"  # cross edge

class Edge(Tagged):
  def __init__(self, u: Vertex, v: Vertex):
    super().__init__(makeEtag(u, v))
    self.u = u
    self.v = v
    self.cls = EClass.X
  def init(self) -> None: self.__init__(self.u, self.v)

  def __str__(self) -> str: return f"{self.tag}: {self.showClassification()}"
  def show(self) -> str: return f"{self.showClassification()}"
  def showClassification(self) -> str: return self.cls if self.cls != EClass.X else ""

  def isSelfLoop(self) -> bool: return self.u == self.v

def makeEtag(u: Vertex, v: Vertex) -> Tag: return f"{u.tag}-{v.tag}"

ESet = Dict[Tag, Edge]

## graph and tree

class VE(Tagged):
  def __init__(self, tag: Tag):
    super().__init__(tag)
    self.vv: VSet = {}
    self.ee: ESet = {}
  def init(self) -> None:
    for u in self.getVV(): u.init()
    for e in self.getEE(): e.init()

  def makeVE(self, vs: List[Tag], es: Dict[Tag, List[Tag]]) -> None:
    self.makeV(vs)
    self.makeE(es)
  def makeV(self, vs: List[Tag]) -> None:
    for vtag in vs: self.vv[vtag] = Vertex(vtag)
  def makeE(self, es: Dict[Tag, List[Tag]]) -> None:
    for uid, vtags in es.items():
      for vtag in vtags:
        e = Edge(self.getV(uid), self.getV(vtag))
        self.ee[e.tag] = e

  def __str__(self) -> str:
    return self.tag + "\n" + self.showVertices() + "\n" + self.showEdges()
  def showVertices(self) -> str:
    def neighbors(u: Vertex) -> str: return ",".join([v.tag for v in self.adj(u)])
    return "\n".join([f"  {u}\n    [{neighbors(u)}]" for u in self.getVV()])
  def showEdges(self) -> str:
    return "\n".join([f"  {e}" for e in self.getEE()])

  # vertex

  def insV(self, v: Vertex) -> None:
    self.vv[v.tag] = v
  def delV(self, v: Vertex) -> None:
    self.vv.pop(v.tag)
  def dupVV(self, vv: VSet) -> None:
    self.vv = {**vv}
  def getV(self, vtag: Tag) -> Vertex:
    return self.vv[vtag]
  def getVV(self) -> List[Vertex]:
    return list(self.vv.values())
  def numVV(self) -> int:
    return len(self.getVV())
  def adj(self, u: Vertex) -> List[Vertex]:
    return [self.getV(e.v.tag) for e in self.getEE() if e.u.tag == u.tag]
  def path(self, s: Vertex, v: Vertex) -> List[Vertex]:
    # see p.562
    if v.isRoot(): return []
    return [s] if v == s else [v, *self.path(s, v.par)]
  def isAncestor(self, u: Vertex, v: Vertex) -> bool:
    # check if vertex u is the ancestor of vertex v (there exists a path from u ~> v)
    def reachable(a: Vertex) -> bool:
      # check if a can reach v
      aa = self.adj(a)  # edge a -> v
      return True if v in aa else reduce(lambda acc, b: acc or reachable(b), aa, False)  # path a ~> v
    return True if u == v else reachable(u)  # self-loop or path
  def isDescendant(self, v: Vertex, u: Vertex) -> bool:
    return self.isAncestor(u, v)
  def hasV(self, vtag: Tag) -> bool:
    return vtag in self.vv

  # edge

  def insE(self, e: Edge) -> None:
    self.ee[e.tag] = e
  def delE(self, e: Edge) -> None:
    self.ee.pop(e.tag)
  def dupEE(self, ee: ESet) -> None:
    self.ee = {**ee}
  def getE(self, eid: Tag) -> Edge:
    return self.ee[eid]
  def getEE(self) -> List[Edge]:
    return list(self.ee.values())
  def numEE(self) -> int:
    return len(self.getEE())
  def hasE(self, etag: Tag) -> bool:
    return etag in self.ee

class Graph(VE): pass

class Tree(VE): pass

def init(g: Graph) -> None:
  for u in g.getVV():
    u.par = None
    u.dis = Infinity
    u.col = VColor.White

## §20.2 Breadth-first search p.554

def bfs(g: Graph, s: Vertex) -> Graph:
  def explore() -> Graph:
    if q.empty(): return g
    u = q.get()
    for v in g.adj(u):
      if v.col == VColor.White:
        # v discovered
        v.par = u
        v.dis = u.dis + 1
        v.col = VColor.Gray
        q.put(v)
    # u finished
    u.col = VColor.Black
    return explore()

  # initialize
  init(g)
  # s discovered
  s.par = None
  s.dis = 0
  s.col = VColor.Gray
  # search g
  q = Queue()
  q.put(s)
  return explore()

def bft(g: Graph, s: Vertex) -> Tree:
  g = bfs(g, s)
  t = Tree(f"{g.tag}†")
  for u in g.getVV():
    if u == s or not u.isRoot(): t.insV(u)
  for u in t.getVV():
    if not u.isRoot():
      e = g.getE(makeEtag(u.par, u))
      t.insE(e)
  return t

## §20.3 Depth-first search p.563

def dfs(g: Graph) -> Graph:
  def explore(u: Vertex) -> None:
    time[0] += 1
    # u discovered
    u.dis = time[0]
    u.col = VColor.Gray
    for v in g.adj(u):
      e = g.getE(makeEtag(u, v))
      if v.col == VColor.Black:
        e.cls = EClass.F if u.dis < v.dis else EClass.C
      elif v.col == VColor.Gray:
        e.cls = EClass.B
      elif v.col == VColor.White:
        v.par = u
        e.cls = EClass.T
        explore(v)
    time[0] += 1
    # u finished
    u.fin = time[0]
    u.col = VColor.Black

  # initialize
  init(g)
  # search g
  time = [0]  # use array instead of a scalar to allow explore() to mutate time
  for u in g.getVV():
    if u.col == VColor.White: explore(u)
  return g

def dff(g: Graph) -> Graph:
  g = dfs(g)
  f = Graph(f"{g.tag}†")
  f.dupVV(g.vv)
  for v in f.getVV():
    if not v.isRoot():
      e = g.getE(makeEtag(v.par, v))
      f.insE(e)
  return f

## §20.4 Topological sort p.573

def tsort(g: Graph) -> List[Vertex]:
  g = dfs(g)
  return sorted(g.getVV(), key=lambda u: u.fin, reverse=True)

## §20.5 Strongly connected components

class Component(Vertex):
  def __init__(self, tag: Tag):
    super().__init__(tag)
    self.vv: VSet = {}  # strongly connected vertices
  def init(self) -> None: self.__init__(self.tag)

  def insVV(self, vv: List[Vertex]) -> None:
    for u in vv: self.vv[u.tag] = u
  def getVV(self) -> List[Vertex]: return list(self.vv.values())

def makeCid(vv: List[Vertex]) -> Tag: return "+".join([v.tag for v in vv])

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

def sort(g: Graph, attr: Callable[[Vertex], int], reverse: bool = False) -> Graph:
  # sort vertices
  s = Graph(f"{g.tag}§")
  for u in sorted(g.getVV(), key=attr, reverse=reverse): s.insV(u)  # sorted vertices
  s.dupEE(g.ee)
  return s

def contract(g: Graph, f: Graph) -> Graph:
  # contract DFS g using DFF f
  def scv(u: Vertex) -> List[Vertex]:
    aa = f.adj(u)  # vertex u's adjacent vertices in DFF f
    return [] if not aa else [v := aa[0], *scv(v)]

  c = Graph(f"{g.tag}₵")  # SCC c
  # create vertices of SCC c
  for r in [v for v in g.getVV() if v.isRoot()]:  # for each root vertex r in DFS g
    vv = [r, *scv(r)]  # strongly connected vertices rooted at vertex r
    x = Component(makeCid(vv))  # create component x by merging strongly connected vertices vv
    x.insVV(vv)
    c.insV(x)  # insert component x into SCC c
  # create edges of SCC c
  # noinspection PyTypeChecker
  cc: List[Component] = c.getVV()  # components of SCC c; disable type inspection, because cc here is certain to be List[Component], not List[Vertex]
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

def draw(g: Union[Graph, Tree], directed: bool, label: str = "", engine: str = "sfdp") -> V.Graph:
  # returned gv must be evaluated in the top level scope for it to render in the notebook
  gv = V.Digraph(engine=engine) if directed else V.Graph(engine=engine)
  gv.attr(label=label if label != "" else g.tag)
  for v in g.getVV(): gv.node(v.tag, label=v.show(), shape=f"{'rectangle' if v.isRoot() else 'ellipse'}")
  ed = {}  # already drawn edges
  for e in g.getEE():
    vutag = makeEtag(e.v, e.u)
    if directed or vutag not in ed.keys():  # for undirected graph, avoid drawing (u, v) if (v, u) has already been drawn
      gv.edge(e.u.tag, e.v.tag, label=e.show())
      ed[e.tag] = e
  return gv
