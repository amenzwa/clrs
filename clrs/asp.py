"""
This module contains implementations of algorithms described in
Chapter 23 All-Pairs Shortest Paths.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from clrs.graph import MtxGraph, Vert, WMtx, indicesOfETag, parseETag
from clrs.mst import WgtEdge

from clrs.util import Infinity, Tag

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
  g.dd = [[]] * np1
  g.dd[0] = g.ww
  g.pp = [[]] * np1
  g.pp[0] = [[]] * n
  for i in r:
    g.pp[0][i] = [-Infinity] * n  # use -Infinity instead of NIL as used in CLRS; see p.659
    for j in r:
      g.pp[0][i][j] = -Infinity if i == j or g.ww[i][j] == Infinity else i
  # discover ASP in graph g
  for k in range(1, np1):
    g.dd[k] = [[]] * n
    g.pp[k] = [[]] * n
    for i in r:
      g.dd[k][i] = [Infinity] * n
      g.pp[k][i] = [-Infinity] * n
      for j in r:
        km1 = k - 1
        g.dd[k][i][j] = min(g.dd[km1][i][j], g.dd[km1][i][km1] + g.dd[km1][km1][j])
        g.pp[k][i][j] = g.pp[km1][km1][j] if g.dd[km1][i][j] > g.dd[km1][i][km1] + g.dd[km1][km1][j] else g.pp[km1][i][j]  # see Equation 23.8 p.659
  return g.dd[n], g.pp[n]
