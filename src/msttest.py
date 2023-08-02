"""
This module contains tests for the algorithms implemented in the mst module.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from unittest import TestCase

from src.graph import draw
from src.mst import MSTGraph, PrimMSTGraph, mstKruskal, mstPrim

## Kruskal's MST algorithm

class KruskalMSTTestCase(TestCase):
  vs = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
  es = {
    "a": ["b", "h"],
    "b": ["a", "c", "h"],
    "c": ["b", "d", "f", "i"],
    "d": ["c", "e", "f"],
    "e": ["d", "f"],
    "f": ["c", "d", "e", "g"],
    "g": ["f", "h", "i"],
    "h": ["a", "b", "g", "i"],
    "i": ["c", "g", "h"],
  }
  ew = {
    "a-b": 4,
    "a-h": 8,
    "b-a": 4,
    "b-c": 8,
    "b-h": 11,
    "c-b": 8,
    "c-d": 7,
    "c-f": 4,
    "c-i": 2,
    "d-c": 7,
    "d-e": 9,
    "d-f": 14,
    "e-d": 9,
    "e-f": 10,
    "f-c": 4,
    "f-d": 14,
    "f-e": 10,
    "f-g": 2,
    "g-f": 2,
    "g-h": 1,
    "g-i": 6,
    "h-a": 8,
    "h-b": 11,
    "h-g": 1,
    "h-i": 7,
    "i-c": 2,
    "i-g": 6,
    "i-h": 7,
  }
  g = MSTGraph("dummy")

  def setUp(self) -> None:
    self.g = MSTGraph("Kruskal")
    self.g.makeVEw(self.vs, self.es, self.ew)

  def tearDown(self) -> None:
    pass

  def testBFS(self) -> None:
    print(self.g)
    draw(self.g, directed=False, label=f"{self.g.tag} connected, undirected graph").render(f"viz-{self.g.tag}")
    t = mstKruskal(self.g)
    print(t)
    draw(t, directed=False, label=f"{t.tag} Minimum Spanning Tree").render(f"viz-{t.tag}")

## Prim's MST algorithm

class PrimMSTTestCase(TestCase):
  vs = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
  es = {
    "a": ["b", "h"],
    "b": ["a", "c", "h"],
    "c": ["b", "d", "f", "i"],
    "d": ["c", "e", "f"],
    "e": ["d", "f"],
    "f": ["c", "d", "e", "g"],
    "g": ["f", "h", "i"],
    "h": ["a", "b", "g", "i"],
    "i": ["c", "g", "h"],
  }
  ew = {
    "a-b": 4,
    "a-h": 8,
    "b-a": 4,
    "b-c": 8,
    "b-h": 11,
    "c-b": 8,
    "c-d": 7,
    "c-f": 4,
    "c-i": 2,
    "d-c": 7,
    "d-e": 9,
    "d-f": 14,
    "e-d": 9,
    "e-f": 10,
    "f-c": 4,
    "f-d": 14,
    "f-e": 10,
    "f-g": 2,
    "g-f": 2,
    "g-h": 1,
    "g-i": 6,
    "h-a": 8,
    "h-b": 11,
    "h-g": 1,
    "h-i": 7,
    "i-c": 2,
    "i-g": 6,
    "i-h": 7,
  }
  g = MSTGraph("dummy")

  def setUp(self) -> None:
    self.g = PrimMSTGraph("Prim")
    self.g.makeVEw(self.vs, self.es, self.ew)

  def tearDown(self) -> None:
    pass

  def testBFS(self) -> None:
    # noinspection PyTypeChecker
    t = mstPrim(self.g, self.g.getV("a"))  # disable type inspection, because the vertex here is certain to be PriVertex, not Vertex
    print(t)
    draw(t, directed=False, label=f"{t.tag} Minimum Spanning Tree").render(f"viz-{t.tag}")
