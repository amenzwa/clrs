"""
This module contains implementations of algorithms described in
Chapter 23 All-Pairs Shortest Paths.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from copy import deepcopy

from clrs.graph import LstTree, MtxGraph, Vert, WMtx, etagOfIndices, indicesOfETag, makeETag, parseETag
from clrs.mst import WgtEdge
from clrs.ssp import DijkstraGraph, sspBellmanFord, sspDijkstra

from clrs.util import Infinity, Option, Tag, isNone

## ASP directed, weighted graph represented using adjacency matrix

class ASPGraph(MtxGraph):
  def __init__(self, tag: Tag):
    super().__init__(tag)

  def makeVEw(self, vt: [Tag], et: [Tag], ew: {Tag, float}) -> None:
    self.makeV(vt)
    self.makeEw(et, ew)
  def makeEw(self, et: [Tag], ew: {Tag, float}) -> None:
    for etag in et:
      [utag, vtag] = parseETag(etag)
      e = WgtEdge(self.getV(utag), self.getV(vtag), ew[etag])
      self.ee[e.tag] = e
      [i, j] = indicesOfETag(etag)
      self.ww[i][j] = ew[etag]

## §23.2 The Floyd-Warshall algorithm p.655

def aspFloydWarshall(g: ASPGraph) -> [WMtx, WMtx]:
  n = g.numVV()
  r = range(0, n)
  np1 = n + 1
  # initialize
  dd = [[]] * np1
  dd[0] = g.ww
  pp = [[]] * np1
  pp[0] = [[]] * n
  for i in r:
    pp[0][i] = [-Infinity] * n  # use -Infinity instead of NIL as used in CLRS; see p.659
    for j in r: pp[0][i][j] = -Infinity if i == j or g.ww[i][j] == Infinity else i
  # discover ASP in graph g
  for k in range(1, np1):
    km1 = k - 1
    dd[k] = [[]] * n
    pp[k] = [[]] * n
    for i in r:
      dd[k][i] = [Infinity] * n
      pp[k][i] = [-Infinity] * n
      for j in r:
        dd[k][i][j] = min(dd[km1][i][j], dd[km1][i][km1] + dd[km1][km1][j])
        pp[k][i][j] = pp[km1][km1][j] if dd[km1][i][j] > dd[km1][i][km1] + dd[km1][km1][j] else pp[km1][i][j]  # see Equation 23.8 p.659
  return dd[n], pp[n]

## Transitive closure of a directed graph p.659

BMtx = [[bool]]

def tclosure(g: ASPGraph) -> BMtx:
  n = g.numVV()
  r = range(0, n)
  np1 = n + 1
  # intialize
  tt = [[]] * np1
  tt[0] = [[]] * n
  for i in r:
    tt[0][i] = [[]] * n
    for j in r: tt[0][i][j] = i == j or g.hasE(etagOfIndices(i, j))
  for k in range(1, np1):
    km1 = k - 1
    tt[k] = [[]] * n
    for i in r:
      tt[k][i] = [False] * n
      for j in r: tt[k][i][j] = tt[km1][i][j] or (tt[km1][i][km1] and tt[km1][km1][j])
  return tt[n]

## §23.3 Johnson’s algorithm for sparse graphs p.662

JohnsonGraph = DijkstraGraph  # uses PriVert and WgtEdge

def aspJohnson(g: JohnsonGraph) -> [WMtx, [LstTree]]:
  # initialize
  h: JohnsonGraph = JohnsonGraph(f"{g.tag}+")  # graph h is graph g augmented with source vertex s and its out edges
  h.dupVV(g.vv)
  h.dupEE(g.ee)
  s = Vert("0")
  h.insV(s)
  for u in g.getVV():
    e = WgtEdge(s, u)
    e.wgt = 0.0
    h.insE(e)
  # check for negative-weight cycles using Bellman-Ford
  p = sspBellmanFord(h, s)
  if isNone(p): raise Exception("input graph contains a negative-weight cycle")
  # reweight graph h to eliminate negative weights on edges
  for e in h.getEE():  # for each edge in graph h
    u = h.getV(e.u.tag)
    v = h.getV(e.v.tag)
    # w^(u, v) = w(u, v) + h(u) - h(v), where h(u) = δ(s, u) and h(v) = δ(s, v); see Equation 23.10 p.663 and p.664
    e.wgt += u.dis - v.dis
  # discover ASP in graph g using Dijkstra, once for each vertex as the source
  n = g.numVV()
  r = range(0, n)
  dd = [[]] * n  # shortest distances
  tt = [LstTree] * n  # Dijkstra SSPs
  for i in r: dd[i] = [float] * n
  g.tag = f"{g.tag}ω"
  g.dupVV(h.vv)  # copy u.dis = δ(s, u)
  g.delV(s)
  for u in g.getVV():  # for each vertex in graph g
    i = int(u.tag) - 1
    # discover SSP in graph g from vertex u
    p = sspDijkstra(g, u)  # compute δ^(u, v) for all vertices v of graph g
    tt[i] = deepcopy(p)
    for v in g.getVV():
      j = int(v.tag) - 1
      dd[i][j] = u.pri + v.dis - u.dis #hv.dis - hu.dis
  return dd, tt