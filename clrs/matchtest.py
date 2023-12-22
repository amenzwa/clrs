"""
This module contains tests for the algorithms implemented in the match module.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from unittest import TestCase

from clrs.graph import draw
from clrs.match import MatchGraph, mfHopcroftKarp

## Hopcroft-Karp maximum bipartite matching

class HopcroftKarpMFTestCase(TestCase):
  # Figure 25.2 p.710
  lt = ["l1", "l2", "l3", "l4", "l5", "l6", "l7"]
  rt = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"]
  et = [  # directed edges
    "l1-r2", "l1-r3",
    "l2-r1", "l2-r2",
    "l3-r1", "l3-r3", "l3-r4", "l3-r5", "l3-r6",
    "l4-r2", "l4-r3", "l4-r7",
    "l5-r4", "l5-r5", "l5-r6", "l5-r7",
    "l6-r3", "l6-r7",
    "l7-r5", "l7-r8", ]
  ec = {
    "l1-r2": 1, "l1-r3": 1,
    "l2-r1": 1, "l2-r2": 1,
    "l3-r1": 1, "l3-r3": 1, "l3-r4": 1, "l3-r5": 1, "l3-r6": 1,
    "l4-r2": 1, "l4-r3": 1, "l4-r7": 1,
    "l5-r4": 1, "l5-r5": 1, "l5-r6": 1, "l5-r7": 1,
    "l6-r3": 1, "l6-r7": 1,
    "l7-r5": 1, "l7-r8": 1, }
  fn = FlowGraph("dummy")

  def setUp(self) -> None:
    self.fn = FlowGraph("Hopcroft-Karp")
    self.fn.makeVEc(self.vt, self.et, self.ec)

  def tearDown(self) -> None:
    pass

  def testHopcroftKarp(self) -> None:
    print(self.fn)
    draw(self.fn, directed=True, label=f"{self.fn.tag} flow network").render(f"viz-{self.fn.tag}")
    s = self.fn.getV("s")
    t = self.fn.getV("t")
    mf = mfHopcroftKarp(self.fn, s, t)
    print(mf)
    draw(mf, directed=True, label=f"{mf.tag} Maximum Bipartite Matching").render(f"viz-{mf.tag}")
