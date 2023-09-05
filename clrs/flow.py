"""
This module contains implementations of maximum flow algorithms described in
Chapter 24 Maximum Flow.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from clrs.util import Infinity, Tag
from clrs.graph import Edge, LstGraph, Vert, makeETag, parseETag
from clrs.ega import bfs

## flow edge

class FlowEdge(Edge):
  def __init__(self, u: Vert, v: Vert, cap: float = 0.0):
    super().__init__(u, v)
    self.flo: float = 0.0
    self.cap: float = cap

  def residual(self) -> float: return self.cap - self.flo

  def __str__(self) -> str: return f"{self.tag}: {self.showFlow()}"
  def show(self) -> str: return f"{self.showFlow()}"
  def showFlow(self) -> str: return f"{self.flo}{f'/{self.cap}' if self.cap > 0.0 else ''}"

## maximum flow network with flow edges

class FlowGraph(LstGraph):  # uses FlowEdge
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

## Edmonds-Karp algorithm p.686-689

def mfEdmondsKarp(fn: FlowGraph, s: Vert, t: Vert) -> FlowGraph:
  def resNet(fn: FlowGraph) -> FlowGraph:
    # extract a residual network from flow network fn; see p.677
    def edgeResCap(fn: FlowGraph, u: Vert, v: Vert) -> float:
      # compute residual capacity for edge e; see Equation 24.2 p.677
      uvtag = makeETag(u, v)
      vutag = makeETag(v, u)
      if fn.hasE(uvtag): return fn.getE(uvtag).residual()
      elif fn.hasE(vutag): return fn.getE(vutag).flo
      else: return 0.0

    rn = FlowGraph(f"{fn.tag}-")
    rn.dupVV(fn.vv)
    for u in fn.getVV():
      for v in fn.getVV():
        if fn.hasE(makeETag(u, v)) and (r := edgeResCap(fn, u, v)) > 0.0: rn.insE(FlowEdge(u, v, r))
    return rn

  def augPath(rn: FlowGraph, s: Vert, t: Vert) -> [FlowEdge]:
    # find an augmenting path from vertex s to vertex t in residual network rn; see p.681
    vv = list(reversed(rn.pathSV(s, t)))
    return list(map(lambda uv: rn.getE(makeETag(uv[0], uv[1])), zip(vv, vv[1:])))

  def pathResCap(ap: [FlowEdge]) -> float:
    # residual capacity (the minimum) of augmenting path ap; see p.681
    if len(ap) == 1: return 0.0;
    return min([e.residual() for e in ap])

  # initialize
  for e in fn.getEE(): e.flo = 0.0
  # augment flow
  while ap := augPath(bfs(resNet(fn), s), s, t):
    c = pathResCap(ap)
    for e in ap:
      if fn.hasE(e.tag):
        uv = fn.getE(e.tag)
        uv.flo += c
      else:
        vu = fn.getE(makeETag(e.v, e.u))
        vu.flo -= c
  fn.tag = f"{fn.tag}➨"
  return fn
