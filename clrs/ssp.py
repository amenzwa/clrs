"""
This module contains implementations of algorithms described in
Chapter 22 Single-Source Shortest Paths.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from functools import reduce
from queue import PriorityQueue

from clrs.graph import LstTree, Vert, makeETag
from clrs.ega import tsort
from clrs.mst import MSTGraph, PrimMSTGraph, PriVert, WgtEdge

from clrs.util import Infinity, Option

## SSP directed, weighted graph

SSPGraph = MSTGraph  # uses WgtEdge

def sspInit(g: SSPGraph, s: Vert) -> None:
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

def shortestPathWeight(g: SSPGraph, s: Vert, v: Vert) -> float:
  # see p.604
  return [g.getE(makeETag(u.par, u)).wgt for u in path(s, v)]

## §22.1 Bellman-Ford algorithm p.612

def sspBellmanFord(g: SSPGraph, s: Vert) -> Option[LstTree]:
  # initialize
  sspInit(g, s)
  # relax edges
  n = g.numVV()
  for i in range(1, n):  # iteration i ∈ [1, n)
    for e in g.getEE(): relax(e)
  # check for negative-weight cycle
  for e in g.getEE():
    u = e.u
    v = e.v
    if v.dis > u.dis + e.wgt: return None  # found negative-weight cycle reachable from vertex s
  return getSSP(g, s)  # extract SSP p from graph g

def getSSP(g: SSPGraph, s: Vert | PriVert) -> LstTree:
  p = LstTree(f"{g.tag}¶")
  p.insV(s)
  for u in g.getVV():
    if u != s:
      p.insV(u)
    if not u.isRoot():
      etag = makeETag(u.par, u)
      if g.hasE(etag):
        e = g.getE(etag)
        p.insE(e)
  return p

## §22.2 Single-source shortest paths in directed acyclic graphs

def sspBellmanFordDAWG(g: SSPGraph, s: Vert) -> Option[LstTree]:
  vv = tsort(g)
  # initialize
  sspInit(g, s)
  # relax edges
  for u in vv:  # for each topologically sorted vertex
    for v in g.adj(u): relax(g.getE(makeETag(u, v)))
  return getSSP(g, s)

## §22.3 Dijkstra's algorithm p.620

DijkstraSSPGraph = PrimMSTGraph  # uses PriVertex

def sspDijkstra(g: SSPGraph, s: PriVert) -> LstTree:
  assert(reduce(lambda acc, e: acc and e.wgt >= 0, g.getEE(), True))
  # initialize
  sspInit(g, s)
  s.pri = s.dis
  b: VSet = {}  # vertex set of SSP
  q = PriorityQueue()
  for u in g.getVV(): q.put(u)
  # discover SSP in graph g
  while not q.empty():
    u = q.get()
    b[u.tag] = u
    for v in g.adj(u):
      if relax(g.getE(makeETag(u, v))):
        v.pri = v.dis
        q.queue.sort()  # rearrange q to account for decreased v.dis
  return getSSP(g, s)
