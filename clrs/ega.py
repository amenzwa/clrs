"""
This module contains implementations of the graph algorithms described in
Chapter 20 Elementary Graph Algorithms.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from typing import Callable, Generic, TypeVar
from queue import Queue

from clrs.graph import ECls, ESet, Edge, Graph, Tree, VCol, Vert, makeETag, parseETag
from clrs.util import DSet, Infinity, Tag

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