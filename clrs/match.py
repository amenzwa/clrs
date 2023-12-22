"""
This module contains implementations of maximum bipartite matching algorithms described in
Chapter 25 Matchings in Bipartite Graphs.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from clrs.util import DSet, Infinity, Tag
from clrs.graph import Edge, LstGraph, Vert, makeETag, parseETag

## matching bipartite graph

class MatchGraph(LstGraph):  # uses FlowEdge
  def __init__(self, tag: Tag):
    super().__init__(tag)

  def makeVEc(self, vt: [Tag], et: [Tag], ec: {Tag, float}) -> None:
    self.makeV(vt)
    self.makeEc(et, ec)
  def makeEc(self, et: [Tag], ec: {Tag, float}) -> None:
    for etag in et:
      [utag, vtag] = parseETag(etag)
      e = FlowEdge(self.getV(utag), self.getV(vtag), float(ec[etag]))
      self.ee[e.tag] = e

## Hopcroft-Karp algorithm p.709

def mfHopcroftKarp(fn: FlowGraph, s: Vert, t: Vert) -> FlowGraph:
  def augPath(rn: FlowGraph, s: Vert, t: Vert) -> [FlowEdge]:
    # find an augmenting path from vertex s to vertex t in residual network rn; see p.681
    vv = list(reversed(rn.pathSV(s, t)))
    return list(map(lambda uv: rn.getE(makeETag(uv[0], uv[1])), zip(vv, vv[1:])))

  # initialize
  m: ESet = {}  # matching
  # enlarge matching
  while p := mfEdmondsKarp(fn, s, t):
    # TODO
    pass
  fn.tag = f"{fn.tag}⇆"
  return fn
