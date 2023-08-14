"""
This module contains tests for the algorithms implemented in the asp module.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from unittest import TestCase

from clrs.graph import draw
from clrs.asp import ASPGraph, BMtx, WMtx, aspFloydWarshall, tclosure

## Floyd-Warshall ASP

class FloydWarshallASPTestCase(TestCase):
  # Figure 23.1 p.652
  vt = ["1", "2", "3", "4", "5"]
  et = [  # directed edges
    "1-2", "1-3", "1-5",
    "2-4", "2-5",
    "3-2",
    "4-1", "4-3",
    "5-4", ]
  ew = {
    "1-2": 3, "1-3": 8, "1-5": -4,
    "2-4": 1, "2-5": 7,
    "3-2": 4,
    "4-1": 2, "4-3": -5,
    "5-4": 6, }
  g = ASPGraph("dummy")

  def setUp(self) -> None:
    self.g = ASPGraph("Floyd-Warshall")
    self.g.makeVEw(self.vt, self.et, self.ew)

  def tearDown(self) -> None:
    pass

  def testFloydWarshall(self) -> None:
    print(self.g)
    draw(self.g, directed=True, label=f"{self.g.tag} directed, weighted graph").render(f"viz-{self.g.tag}")
    dd, pp = aspFloydWarshall(self.g)
    print(f"{self.g.tag}\n  all-pairs shortest paths")
    for i in range(0, len(dd)): print(f"    {dd[i]}")
    print("  predecessor subgraph")
    for i in range(0, len(pp)): print(f"    {list(map(lambda x: x + 1, pp[i]))}")  # +1 to offset zero-based indices

## transitive closure

class TransitiveClosureTestCase(TestCase):
  # Figure 23.5 p.660
  vt = ["1", "2", "3", "4"]
  et = [  # directed edges
    "2-3", "2-4",
    "3-2",
    "4-1", "4-3", ]
  ew = {  # dummy edge weights
    "2-3": 1, "2-4": 1,
    "3-2": 1,
    "4-1": 1, "4-3": 1, }
  g = ASPGraph("dummy")

  def setUp(self) -> None:
    self.g = ASPGraph("Transitive Closure")
    self.g.makeVEw(self.vt, self.et, self.ew)

  def tearDown(self) -> None:
    pass

  def testTransitiveClosure(self) -> None:
    print(self.g)
    draw(self.g, directed=True, label=f"{self.g.tag} directed, weighted graph").render(f"viz-{self.g.tag}")
    tt = tclosure(self.g)
    print(f"{self.g.tag}\n  transitive closure")
    for i in range(0, len(tt)): print(f"    {tt[i]}")