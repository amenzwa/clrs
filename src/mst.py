"""
This module contains implementations of algorithms described in
Chapter 21 Minimum Spanning Trees.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from queue import PriorityQueue
from typing import Dict, List

from src.graph import ESet, Edge, Graph, Tree, Vertex, makeEtag
from src.util import DSet, Infinity, Tag

## weighted edge

class WgtEdge(Edge):
  def __init__(self, u: Vertex, v: Vertex, wgt: float = Infinity):
    super().__init__(u, v)
    self.wgt: float = wgt

  def __str__(self) -> str: return f"{self.tag}: {self.showWeight()}"
  def show(self) -> str: return f"{self.showWeight()}"
  def showWeight(self) -> str: return str(self.wgt) if self.wgt != Infinity else ""

## MST connected, undirected graph with weighted edges

class MSTGraph(Graph):
  def __init__(self, tag: Tag):
    super().__init__(tag)

  def makeVEw(self, vs: List[Tag], es: Dict[Tag, List[Tag]], ew: Dict[Tag, float]) -> None:
    self.makeV(vs)
    self.makeEw(es, ew)
  def makeEw(self, es: Dict[Tag, List[Tag]], ew: Dict[Tag, float]) -> None:
    for utag, vtags in es.items():
      for vtag in vtags:
        u = self.getV(utag)
        v = self.getV(vtag)
        e = WgtEdge(u, v, ew[makeEtag(u, v)])
        self.ee[e.tag] = e

## Kruskal's MST

def mstKruskal(g: MSTGraph) -> Tree:
  # initialize
  a: ESet = {}  # edge set of MST
  ds = DSet(attr=lambda e: e.wgt)  # forests disjoint set
  for u in g.getVV(): ds.makeSet(u)
  # discover MST in graph g
  for e in sorted(g.getEE(), key=lambda e: e.wgt):  # edges ascending sorted by their weights
    if ds.findSet(e.u) != ds.findSet(e.v):
      a[e.tag] = e
      ds.union(e.u, e.v)
  # extract MST t from graph g using tree edge set a
  t = Tree(f"{g.tag}†")
  for e in a.values():
    t.insE(e)
    t.insV(e.u)
    t.insV(e.v)
  return t

## prioritized vertex

class PriVertex(Vertex):
  def __init__(self, tag: Tag):
    super().__init__(tag)
    self.pri: float = Infinity

  def __str__(self) -> str: return f"{super().__str__()} {self.priority()}"
  def priority(self) -> str: return f"{self.pri if self.pri != Infinity else ''}"

  def __lt__(self, v: "PriVertex") -> bool: return self.pri < v.pri  # needed by PriorityQueue

## Prim MST graph with prioritized vertices

class PrimMSTGraph(MSTGraph):
  def __init__(self, tag: Tag):
    super().__init__(tag)

  def makeV(self, vs: List[Tag]) -> None:
    for vtag in vs: self.vv[vtag] = PriVertex(vtag)

## Prim's MST

def mstPrim(g: MSTGraph, r: PriVertex) -> Tree:
  # initialize
  for u in g.getVV():
    u.par = None
    u.pri = Infinity
  r.pri = 0
  q = PriorityQueue()
  for u in g.getVV(): q.put(u)
  # discover MST in graph g
  while not q.empty():
    u = q.get()
    for v in g.adj(u):
      # noinspection PyTypeChecker
      e: WgtEdge = g.getE(makeEtag(u, v))  # disable type inspection, because e here is certain to be WgtEdge, not Edge
      if v in q.queue and e.wgt < v.pri:
        v.par = u
        v.pri = e.wgt
        q.queue.sort()  # rearrange q to account for decreased v.pri
  # extract MST t from graph g using tree vertices vv
  t = Tree(f"{g.tag}†")
  for v in g.getVV():
    t.insV(v)
    if not v.isRoot(): t.insE(g.getE(makeEtag(v, v.par)))  # see p.596
  return t
