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

def aspFloydWarshall(g: ASPGraph) -> [WMtx]:
  n = g.numVV()
  r = range(0, n)
  dd: [WMtx] = [Infinity] * (n + 1)
  dd[0] = g.ww
  for k in range(1, n + 1):
    dd[k] = [Infinity] * n
    for i in r:
      dd[k][i] = [Infinity] * n
      for j in r:
        dd[k][i][j] = min(dd[k - 1][i][j], dd[k - 1][i][k - 1] + dd[k - 1][k - 1][j])
  return dd[n]
