"""
This module contains implementations of algorithms described in
Chapter 22 Single-Source Shortest Paths.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from functools import reduce
from queue import PriorityQueue
from typing import List, Union

from src.graph import Tree, Vertex, makeEtag, tsort
from src.mst import MSTGraph, PrimMSTGraph, PriVertex, WgtEdge

from src.util import Infinity, Option

## SSP directed, weighted graph

SSPGraph = MSTGraph  # uses WgtEdge

def init(g: SSPGraph, s: Vertex) -> None:
  # see p.609
  for u in g.getVV():
    u.par = None
    u.dis = Infinity
  s.dis = 0

def relax(e: WgtEdge) -> bool:
  # return True if v.dis is decreased, False otherwise; see pp.610,620
  u = e.u
  v = e.v
  d = u.dis + e.wgt
  if v.dis > d:
    v.par = u
    v.dis = d
    return True
  return False

def shortestPathWeight(g: SSPGraph, s: Vertex, v: Vertex) -> float:
  # see p.604
  return [g.getE(makeEtag(u.par, u)).wgt for u in path(s, v)]

## §22.1 Bellman-Ford algorithm p.612

def sspBellmanFord(g: SSPGraph, s: Vertex) -> Option[Tree]:
  # initialize
  init(g, s)
  # relax edges
  n = g.numVV()
  # noinspection PyTypeChecker
  for i in range(1, n):  # iteration i ∈ [1, n)
    for e in g.getEE(): relax(e)  # disable type inspection, because e here is certain to be WgtEdge, not Edge
  # check for negative-weight cycle
  for e in g.getEE():
    u = e.u
    v = e.v
    if v.dis > u.dis + e.wgt: return None  # found negative-weight cycle reachable from vertex s
  return getSSP(g, s)  # extract SSP p from graph g

def getSSP(g: SSPGraph, s: Union[Vertex, PriVertex]) -> Tree:
  p = Tree(f"{g.tag}¶")
  p.insV(s)
  for u in g.getVV():
    if u != s:
      p.insV(u)
    if not u.isRoot():
      etag = makeEtag(u.par, u)
      if g.hasE(etag):
        e = g.getE(etag)
        p.insE(e)
  return p

## §22.2 Single-source shortest paths in directed acyclic graphs

def sspBellmanFordDAWG(g: SSPGraph, s: Vertex) -> Option[Tree]:
  vv = tsort(g)
  # initialize
  init(g, s)
  # relax edges
  for u in vv:  # for each topologically sorted vertex
    for v in g.adj(u): relax(g.getE(makeEtag(u, v)))
  return getSSP(g, s)

## §22.3 Dijkstra's algorithm p.620

DijkstraSSPGraph = PrimMSTGraph  # uses PriVertex

def sspDijkstra(g: SSPGraph, s: PriVertex) -> Tree:
  assert(reduce(lambda acc, e: acc and e.wgt >= 0, g.getEE(), True))
  # initialize
  init(g, s)
  s.pri = s.dis
  b: VSet = {}  # vertex set of SSP
  q = PriorityQueue()
  for u in g.getVV(): q.put(u)
  # discover SSP in graph g
  while not q.empty():
    u: PriVertex = q.get()
    b[u.tag] = u
    for v in g.adj(u):
      if relax(g.getE(makeEtag(u, v))):
        v.pri = v.dis
        q.queue.sort()  # rearrange q to account for decreased v.dis
  return getSSP(g, s)
