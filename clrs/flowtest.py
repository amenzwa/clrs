"""
This module contains tests for the algorithms implemented in the flow module.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from unittest import TestCase

from clrs.flow import FlowGraph, mfEdmondsKarp
from clrs.graph import draw

## Edmonds-Karp maximum flow

class EdmondsKarpMFTestCase(TestCase):
  # Figure 24.6 p.687
  vt = ["s", "v1", "v2", "v3", "v4", "t"]
  et = [  # directed edges
    "s-v1", "s-v2",
    "v1-v3",
    "v2-v1", "v2-v4",
    "v3-v2", "v3-t",
    "v4-v3", "v4-t", ]
  ec = {
    "s-v1": 16, "s-v2": 13,
    "v1-v3": 12,
    "v2-v1": 4, "v2-v4": 14,
    "v3-v2": 9, "v3-t": 20,
    "v4-v3": 7, "v4-t": 4, }
  fn = FlowGraph("dummy")

  def setUp(self) -> None:
    self.fn = FlowGraph("Edmonds-Karp")
    self.fn.makeVEc(self.vt, self.et, self.ec)

  def tearDown(self) -> None:
    pass

  def testEdmondsKarp(self) -> None:
    print(self.fn)
    draw(self.fn, directed=True, label=f"{self.fn.tag} flow network").render(f"viz-{self.fn.tag}")
    s = self.fn.getV("s")
    t = self.fn.getV("t")
    mf = mfEdmondsKarp(self.fn, s, t)
    print(mf)
    draw(mf, directed=True, label=f"{mf.tag} Maximum Flow Network").render(f"viz-{mf.tag}")