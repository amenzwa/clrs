"""
This module contains tests for the algorithms implemented in the mst module.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from unittest import TestCase

from src.graph import draw
from src.mst import MSTGraph, PrimMSTGraph, mstKruskal, mstPrim

## Kruskal's and Prim's MST algorithms

class MSTTestCase(TestCase):
  # Figure 21.4 p.592 and Figure 21.5 p.595
  vt = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
  et = [
    "a-b", "a-h",
    "b-a", "b-c", "b-h",
    "c-b", "c-d", "c-f", "c-i",
    "d-c", "d-e", "d-f",
    "e-d", "e-f",
    "f-c", "f-d", "f-e", "f-g",
    "g-f", "g-h", "g-i",
    "h-a", "h-b", "h-g", "h-i",
    "i-c", "i-g", "i-h", ]
  ew = {
    "a-b": 4, "a-h": 8,
    "b-a": 4, "b-c": 8, "b-h": 11,
    "c-b": 8, "c-d": 7, "c-f": 4, "c-i": 2,
    "d-c": 7, "d-e": 9, "d-f": 14,
    "e-d": 9, "e-f": 10,
    "f-c": 4, "f-d": 14, "f-e": 10, "f-g": 2,
    "g-f": 2, "g-h": 1, "g-i": 6,
    "h-a": 8, "h-b": 11, "h-g": 1, "h-i": 7,
    "i-c": 2, "i-g": 6, "i-h": 7, }
  g = MSTGraph("dummy")

  def setUp(self) -> None: pass

  def tearDown(self) -> None: pass

  def testKruskal(self) -> None:
    self.g = MSTGraph("MST")
    self.g.makeVEw(self.vt, self.et, self.ew)
    print(self.g)
    draw(self.g, directed=False, label=f"{self.g.tag} connected, undirected graph").render(f"viz-{self.g.tag}")
    t = mstKruskal(self.g)
    print(t)
    draw(t, directed=False, label=f"{t.tag} Kruskal Minimum Spanning Tree").render(f"viz-{t.tag}Kruskal")

  def testPrim(self) -> None:
    self.g = PrimMSTGraph("MST")
    self.g.makeVEw(self.vt, self.et, self.ew)
    # noinspection PyTypeChecker
    t = mstPrim(self.g, self.g.getV("a"))  # disable type inspection, because the vertex here is certain to be PriVertex, not Vertex
    print(t)
    draw(t, directed=False, label=f"{t.tag} Prim Minimum Spanning Tree").render(f"viz-{t.tag}Prim")
